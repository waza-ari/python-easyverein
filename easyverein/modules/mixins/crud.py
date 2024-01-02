"""
This module provides general CRUD operations for all endpoints.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

from easyverein.core.protocol import IsEVClientProtocol

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)
UpdateModelType = TypeVar("UpdateModelType", bound=BaseModel)


class CRUDMixin(Generic[ModelType, CreateModelType, UpdateModelType]):
    def get(
        self: IsEVClientProtocol, query: str = None, limit: int = 10
    ) -> list[ModelType]:
        """
        Fetches specified objects from the EV API

        Args:
            query (str, optional): Query to use with API. Defaults to None. Refer to the EV API help for more
                                    information on how to use queries
            limit (int, optional): Defines how many resources to return. Defaults to 10.
        """
        self.logger.info(f"Fetching selected {self.endpoint_name} objects from API")

        url = self.c.get_url(f"/{self.endpoint_name}", {"limit": limit, "query": query})

        return self.c.fetch(url, self.return_type)

    def get_all(
        self: IsEVClientProtocol, query: str = None, limit_per_page: int = 10
    ) -> list[ModelType]:
        """
        Fetches all objects from the EV API, abstracting away the need to handle pagination.

        Will fetch all pages of objects and return a single list.

        Args:
            query (str, optional): Query to use with API. Defaults to None. Refer to the EV API help for more
                                    information on how to use queries
            limit_per_page (int, optional): Defines how many resources to return. Defaults to 10.
        """
        self.logger.info(f"Fetching selected {self.endpoint_name} objects from API")

        url = self.c.get_url(
            f"/{self.endpoint_name}", {"limit": limit_per_page, "query": query}
        )

        return self.c.fetch_paginated(url, self.return_type, limit_per_page)

    def get_by_id(
        self: IsEVClientProtocol, obj_id: int, query: str = None
    ) -> ModelType:
        """
        Fetches a single object from the API.

        Args:
            obj_id (int): Id of the object to be retrieved
            query (str, optional): Query to use with API. Defaults to None. Refer to the EV API help for more
                                    information on how to use queries
        """
        self.logger.info(
            f"Fetching {self.endpoint_name} object with id %s from API", obj_id
        )

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}", {"query": query})

        return self.c.fetch_one(url, self.return_type)

    def create(self: IsEVClientProtocol, obj: CreateModelType) -> ModelType:
        """
        Creates an object of specified type and returns the created object

        Args:
            obj (CreateModelType): Object to be created
        """
        self.logger.info(f"Creating object of type {self.endpoint_name}")

        url = self.c.get_url(f"/{self.endpoint_name}/")

        return self.c.create(url, obj, self.return_type)

    def update(
        self: IsEVClientProtocol, obj_id: int, obj: UpdateModelType
    ) -> ModelType:
        """
        Updates (patches) a certain object and returns the updated object.

        Args:
            obj_id (int): ID of the invoice to update
            obj (UpdateModelType): Pydantic Model holding data to update the model
        """
        self.logger.info(
            f"Updating object of type {self.endpoint_name} with id {obj_id} %s"
        )

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}")

        return self.c.update(url, obj, self.return_type)

    def delete(
        self: IsEVClientProtocol,
        obj: ModelType,
        delete_from_recycle_bin: bool = False,
    ):
        """
        Deletes an object. Can optionally purge the object and delete it from the recycle bin,
        but only if supported by the API for this particular endpoint.

        Available endpoints at the time of writing:

        - member
        - contact-details
        - event
        - task
        - protocol
        - booking
        - invoice
        - location
        - inventory-object
        - lending
        - protocol-element
        - protocol-element-comment
        - voting
        - billing-account
        - member-group
        - contact-details-group
        - calendar
        - task-group
        - inventory-object-group
        - chairman-level
        - custom-field-collection
        - custom-field

        Args:
            obj (ModelType): Object to delete
            delete_from_recycle_bin (bool, optional): Whether to delete the invoice
                also from the recycle bin. Defaults to False.
        """
        self.logger.info(
            f"Deleting object of type {self.endpoint_name} with id {obj.id}"
        )

        url = self.c.get_url(f"/{self.endpoint_name}/{obj.id}")

        self.c.delete(url)

        if delete_from_recycle_bin:
            self.logger.info(
                f"Deleting object of type {self.endpoint_name} with id {obj.id} from wastebasket"
            )
            self.purge(obj.id)
