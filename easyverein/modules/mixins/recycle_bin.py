from typing import Generic, TypeVar

from pydantic import BaseModel

from ...core.protocol import IsEVClientProtocol

ModelType = TypeVar("ModelType", bound=BaseModel)


class RecycleBinMixin(Generic[ModelType]):
    def get_deleted(self: IsEVClientProtocol) -> list[ModelType]:
        """
        Fetches all deleted invoices from the API
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

    def purge(self: IsEVClientProtocol, item_id: int):
        """
        Purges a given item from recycle bin
        """
        self.logger.info(
            f"Purging object of type {self.endpoint_name} and id {item_id} from recycle bin"
        )
        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}")
        return self.c.delete(url)
