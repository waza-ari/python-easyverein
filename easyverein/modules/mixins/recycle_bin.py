from ...core.protocol import IsEVClientProtocol


def recycle_bin_mixin(model_class):
    class RecycleBinMixin:
        def get_deleted(self: IsEVClientProtocol) -> list[model_class]:
            """
            Fetches all deleted invoices from the API
            """
            self.logger.info("Fetching all deleted invoices from API")

            url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/")

            return self.c.fetch(url, model_class)

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
            self.logger.info("Purging recycle bin")

            url = self.c.get_url(f"/wastebasket/{self.endpoint_name}/{item_id}/")

            return self.c.delete(url)

    return RecycleBinMixin
