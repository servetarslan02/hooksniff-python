import typing as t
from ..models import OperationalWebhookEndpointOut, OperationalWebhookEndpointIn, OperationalWebhookDeliveryOut
from .common import ApiBase
from .pagination import ListResponse, build_list_response


class OperationalWebhookAsync(ApiBase):
    async def list(self) -> ListResponse[OperationalWebhookEndpointOut]:
        """List operational webhook endpoints with pagination support."""
        response = await self._request_asyncio(method="get", path="/v1/operational-webhooks", path_params={})

        def _fetch_sync(iterator: str) -> ListResponse[OperationalWebhookEndpointOut]:
            resp = self._request_sync(method="get", path="/v1/operational-webhooks", query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookEndpointOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        async def _fetch_async(iterator: str) -> ListResponse[OperationalWebhookEndpointOut]:
            resp = await self._request_asyncio(method="get", path="/v1/operational-webhooks", query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookEndpointOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        return build_list_response(response.json(), OperationalWebhookEndpointOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

    async def create(self, body: OperationalWebhookEndpointIn) -> OperationalWebhookEndpointOut:
        response = await self._request_asyncio(method="post", path="/v1/operational-webhooks", path_params={}, json_body=body.model_dump_json(exclude_unset=True, by_alias=True))
        return OperationalWebhookEndpointOut.model_validate(response.json())

    async def get(self, endpoint_id: str) -> OperationalWebhookEndpointOut:
        response = await self._request_asyncio(method="get", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id})
        return OperationalWebhookEndpointOut.model_validate(response.json())

    async def update(self, endpoint_id: str, body: OperationalWebhookEndpointIn) -> OperationalWebhookEndpointOut:
        response = await self._request_asyncio(method="put", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id}, json_body=body.model_dump_json(exclude_unset=True, by_alias=True))
        return OperationalWebhookEndpointOut.model_validate(response.json())

    async def delete(self, endpoint_id: str) -> None:
        await self._request_asyncio(method="delete", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id})

    async def list_deliveries(self, endpoint_id: str) -> ListResponse[OperationalWebhookDeliveryOut]:
        """List deliveries with pagination support."""
        response = await self._request_asyncio(method="get", path="/v1/operational-webhooks/{id}/deliveries", path_params={"id": endpoint_id})

        def _fetch_sync(iterator: str) -> ListResponse[OperationalWebhookDeliveryOut]:
            resp = self._request_sync(method="get", path="/v1/operational-webhooks/{id}/deliveries", path_params={"id": endpoint_id}, query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookDeliveryOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        async def _fetch_async(iterator: str) -> ListResponse[OperationalWebhookDeliveryOut]:
            resp = await self._request_asyncio(method="get", path="/v1/operational-webhooks/{id}/deliveries", path_params={"id": endpoint_id}, query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookDeliveryOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        return build_list_response(response.json(), OperationalWebhookDeliveryOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)


class OperationalWebhook(ApiBase):
    def list(self) -> ListResponse[OperationalWebhookEndpointOut]:
        """List operational webhook endpoints with pagination support."""
        response = self._request_sync(method="get", path="/v1/operational-webhooks", path_params={})

        def _fetch_sync(iterator: str) -> ListResponse[OperationalWebhookEndpointOut]:
            resp = self._request_sync(method="get", path="/v1/operational-webhooks", query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookEndpointOut, fetch_fn=_fetch_sync)

        return build_list_response(response.json(), OperationalWebhookEndpointOut, fetch_fn=_fetch_sync)

    def create(self, body: OperationalWebhookEndpointIn) -> OperationalWebhookEndpointOut:
        response = self._request_sync(method="post", path="/v1/operational-webhooks", path_params={}, json_body=body.model_dump_json(exclude_unset=True, by_alias=True))
        return OperationalWebhookEndpointOut.model_validate(response.json())

    def get(self, endpoint_id: str) -> OperationalWebhookEndpointOut:
        response = self._request_sync(method="get", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id})
        return OperationalWebhookEndpointOut.model_validate(response.json())

    def update(self, endpoint_id: str, body: OperationalWebhookEndpointIn) -> OperationalWebhookEndpointOut:
        response = self._request_sync(method="put", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id}, json_body=body.model_dump_json(exclude_unset=True, by_alias=True))
        return OperationalWebhookEndpointOut.model_validate(response.json())

    def delete(self, endpoint_id: str) -> None:
        self._request_sync(method="delete", path="/v1/operational-webhooks/{id}", path_params={"id": endpoint_id})

    def list_deliveries(self, endpoint_id: str) -> ListResponse[OperationalWebhookDeliveryOut]:
        """List deliveries with pagination support."""
        response = self._request_sync(method="get", path="/v1/operational-webhooks/{id}/deliveries", path_params={"id": endpoint_id})

        def _fetch_sync(iterator: str) -> ListResponse[OperationalWebhookDeliveryOut]:
            resp = self._request_sync(method="get", path="/v1/operational-webhooks/{id}/deliveries", path_params={"id": endpoint_id}, query_params={"iterator": iterator})
            return build_list_response(resp.json(), OperationalWebhookDeliveryOut, fetch_fn=_fetch_sync)

        return build_list_response(response.json(), OperationalWebhookDeliveryOut, fetch_fn=_fetch_sync)
