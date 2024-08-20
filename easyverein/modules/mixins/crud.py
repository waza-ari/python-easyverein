"""
This module provides general CRUD operations for all endpoints.
"""

from typing import Callable, Generic, TypeVar

from pydantic import BaseModel

from easyverein.core.protocol import EVClientProtocol

from .helper import get_id, parse_models

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)
UpdateModelType = TypeVar("UpdateModelType", bound=BaseModel)
FilterType = TypeVar("FilterType", bound=BaseModel)


class CRUDMixin(Generic[ModelType, CreateModelType, UpdateModelType, FilterType]):
    def get(
        self: EVClientProtocol[ModelType],
        query: str = "",
        search: FilterType | None = None,
        limit: int = 10,
        page: int = 1,
    ) -> tuple[list[ModelType], int]:
        """
        Fetches a single page of a given page size. The page size is defined by the `limit` parameter
        with an API sided upper limit of 100.

        Returns a tuple, where the first element is the returned objects and the second is the total count.

        Args:
            query: Query to use with API. Refer to the EV API help for more information on how to use queries
            search: Filter to use with API. Refer to the EV API help for more information on how to use filters
            limit: Defines how many resources to return.
            page: Deinfines which page to return. Defaults to 1, which is the first page.
        """
        self.logger.info(f"Fetching selected {self.endpoint_name} objects from API")

        url_params = {"limit": limit, "query": query, "page": page}
        if search:
            url_params |= search.model_dump(exclude_unset=True, exclude_defaults=True, by_alias=True)

        self.logger.debug(f"Computed URL params for this request: {url_params}")

        url = self.c.get_url(f"/{self.endpoint_name}", url_params)
        response = self.c.fetch(url)
        parsed_objects = parse_models(response.result, self.return_type)
        assert isinstance(parsed_objects, list)
        return parsed_objects, response.count or 0

    def get_all(
        self: EVClientProtocol[ModelType],
        query: str = "",
        search: FilterType | None = None,
        limit_per_page: int = 10,
    ) -> list[ModelType]:
        """
        Convenient method that fetches all objects from the EV API, abstracting away the need to handle pagination.

        Will fetch all pages of objects and return a single list. The default has been chosen to match the limit
        of the API. It is advisable to set a higher limit to avoid many API calls. The maximum page size is 100.

        Args:
            query: Query to use with API. Defaults to None. Refer to the EV API help for more
                                    information on how to use queries
            search: Filter to use with API. Refer to the EV API help for more information on how to use filters
            limit_per_page: Defines how many resources to return. Defaults to 10.
        """
        self.logger.info(f"Fetching selected {self.endpoint_name} objects from API")

        url_params = {"limit": limit_per_page, "query": query}
        if search:
            url_params |= search.model_dump(exclude_unset=True, exclude_defaults=True, by_alias=True)

        url = self.c.get_url(f"/{self.endpoint_name}", url_params)
        response = self.c.fetch_paginated(url, limit_per_page)
        parsed_objects = parse_models(response.result, self.return_type)
        assert isinstance(parsed_objects, list)
        return parsed_objects

    def get_by_id(self: EVClientProtocol[ModelType], obj_id: int, query: str = "") -> ModelType:
        """
        Fetches a single object identified by its primary id.

        Args:
            obj_id: Id of the object to be retrieved
            query: Query to use with API. Defaults to None. Refer to the EV API help for more
                                    information on how to use queries
        """
        self.logger.info(f"Fetching {self.endpoint_name} object with id {obj_id} from API")

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}", {"query": query})
        response = self.c.fetch_one(url)
        parsed_object = parse_models(response.result, self.return_type)
        assert isinstance(parsed_object, self.return_type)
        return parsed_object

    def create(self: EVClientProtocol[ModelType], data: CreateModelType) -> ModelType:
        """
        Creates an object of specified type and returns the created object.
        The POST method of the respective endpoint is used to create a new resource and the API
        result is parsed, validated and returned as Pydantic object.

        **Example**:

        This example uses the `custom-field` endpoint, but any other endpoint can be used similarly.

        ```py
        from easyverein import EasyvereinAPI

        ev_client = EasyvereinAPI("your_api_key")

        custom_field = ev.custom_field.create(
            CustomFieldCreate(name="Test-Field", kind="e", settings_type="t")
        )
        ```

        Args:
            data: Object to be created
        """
        self.logger.info(f"Creating object of type {self.endpoint_name}")

        url = self.c.get_url(f"/{self.endpoint_name}/")
        response = self.c.create(url, data)
        assert isinstance(response.result, dict)
        parsed_object = parse_models(response.result, self.return_type)
        assert isinstance(parsed_object, self.return_type)
        return parsed_object

    def update(self: EVClientProtocol[ModelType], target: ModelType | int, data: UpdateModelType) -> ModelType:
        """
        Updates (PATCHes) a certain object and returns the updated object. Accepts either an object
        or its id as first argument.

        Args:
            target: Model instance to update or id of the model to update
            data: Pydantic Model holding data to update the model
        """

        obj_id = get_id(target)

        self.logger.info(f"Updating object of type {self.endpoint_name} with id {obj_id}")

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}")
        response = self.c.update(url, data)
        assert isinstance(response.result, dict)
        parsed_object = parse_models(response.result, self.return_type)
        assert isinstance(parsed_object, self.return_type)
        return parsed_object

    def delete(
        self: EVClientProtocol[ModelType],
        target: ModelType | int,
        delete_from_recycle_bin: bool = False,
    ) -> None:
        """
        Deletes an object from the database and returns nothing. Can either take the object itself
        or the id of the object as argument.

        Note that the EV API soft-deletes some objects by default. These objects are not fully
        deleted but instead placed in a recycle bin (official API calls this "wastebasket").

        This library does provide methods to interact with soft deleted objects (see below), but you
        may also instruct the `delete` method to immediately purge the object. This will result in two
        API calls (first soft-delete the object, then remove it from recycle bin). This is only supported
        for some endpoints:

        - member
        - member-group
        - contact-details
        - invoice
        - custom-field

        Args:
            target: Object to delete
            delete_from_recycle_bin: Whether to delete the invoice
                also from the recycle bin. Defaults to False.
        """

        obj_id = get_id(target)

        self.logger.info(f"Deleting object of type {self.endpoint_name} with id {obj_id}")

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}")

        self.c.delete(url)

        if delete_from_recycle_bin and hasattr(self, "purge"):
            self.logger.info(f"Deleting object of type {self.endpoint_name} with id {obj_id} from wastebasket")
            purge: Callable = getattr(self, "purge")
            purge(obj_id)
