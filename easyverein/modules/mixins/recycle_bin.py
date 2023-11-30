from ...core.protocol import IsEVClientProtocol


def recycle_bin_mixin(endpoint_name: str, model_class):
    def get_deleted(self: IsEVClientProtocol) -> list[model_class]:
        """
        Fetches all deleted invoices from the API
        """
        self.logger.info("Fetching all deleted invoices from API")

        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/")

        return self.c.handle_response(self.c.fetch_api_paginated(url), model_class)

    def restore(self: IsEVClientProtocol, item_id: int):
        """
        Restores a given item from the recycle bin
        """
        self.logger.info("Restoring item from recycle bin")

        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}/")

        return self.c.handle_response(
            self.c.do_request("patch", url), expected_status_code=200
        )

    def purge(self: IsEVClientProtocol, item_id: int):
        """
        Purges a given item from recycle bin
        """
        self.logger.info("Purging recycle bin")

        url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}/")

        return self.c.handle_response(
            self.c.do_request("delete", url), expected_status_code=204
        )

    class RecycleBinMixin:
        pass

    setattr(RecycleBinMixin, f"get_deleted_{endpoint_name}s", get_deleted)
    setattr(RecycleBinMixin, f"restore_{endpoint_name}", restore)
    setattr(RecycleBinMixin, f"purge_{endpoint_name}", purge)

    return RecycleBinMixin
