from typing import Generic, TypeVar

from pydantic import BaseModel

from ...core.protocol import IsEVClientProtocol

ModelType = TypeVar("ModelType", bound=BaseModel)


class RecycleBinMixin(Generic[ModelType]):
    def get_deleted(self: IsEVClientProtocol) -> tuple[list[ModelType], int]:
        """
        Fetches all deleted resources from the recycle bin and returns a list.
        """
        self.logger.info(
            f"Fetching all deleted objects of type {self.endpoint_name} from API"
        )
        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/")
        return self.c.fetch(url, self.return_type)

    # def restore(self: IsEVClientProtocol, item_id: int):
    #     """
    #     Restores a given item from the recycle bin
    #     """
    #     self.logger.info("Restoring item from recycle bin")
    #
    #     url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}/")
    #
    #     return self.c.handle_response(
    #         self.c.do_request("patch", url), expected_status_code=200
    #     )

    def purge(self: IsEVClientProtocol, item: ModelType | int):
        """
        Finally deletes a given item from the recycle bin. This is irreversible and cannot be undone.

        This function can take either an object instance or a numerical id as argument.

        Args:
            item: The id or object that should be deleted.
        """
        item_id = item if isinstance(item, int) else item.id

        self.logger.info(
            f"Purging object of type {self.endpoint_name} and id {item_id} from recycle bin"
        )
        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}")
        return self.c.delete(url)
