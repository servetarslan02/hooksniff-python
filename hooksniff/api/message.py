# Adapted for HookSniff API
# HookSniff uses /v1/webhooks for message/delivery operations
import typing as t
from dataclasses import dataclass
from datetime import datetime

from ..models import (
    MessageIn,
    MessageOut,
)
from .common import ApiBase, BaseOptions, serialize_params
from .pagination import ListResponse, build_list_response


@dataclass
class MessageListOptions(BaseOptions):
    limit: t.Optional[int] = None
    page: t.Optional[int] = None
    iterator: t.Optional[str] = None
    status: t.Optional[str] = None
    endpoint_id: t.Optional[str] = None
    event_type: t.Optional[str] = None

    def _query_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "limit": self.limit,
                "page": self.page,
                "iterator": self.iterator,
                "status": self.status,
                "endpoint_id": self.endpoint_id,
                "event_type": self.event_type,
            }
        )


@dataclass
class MessageCreateOptions(BaseOptions):
    idempotency_key: t.Optional[str] = None

    def _header_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "idempotency-key": self.idempotency_key,
            }
        )


def message_in_raw(
    event_type: str, payload: str, content_type: t.Optional[str] = None
) -> MessageIn:
    """
    Creates a `MessageIn` with a raw string payload.

    Args:
        event_type (str): The event type's name Example: `user.signup`.
        payload (str): Serialized message payload.
        content_type (str?): The value to use for the Content-Type header.
    """
    transformations_params: t.Dict[str, t.Any] = {
        "rawPayload": payload,
    }
    if content_type is not None:
        transformations_params["headers"] = {"content-type": content_type}

    return MessageIn(
        event_type=event_type,
        payload={},
        transformations_params=transformations_params,
    )


class MessageAsync(ApiBase):
    async def list(
        self, options: MessageListOptions = MessageListOptions()
    ) -> ListResponse[MessageOut]:
        """List webhook deliveries with pagination support.

        Returns:
            ListResponse[MessageOut] — iterate with `for msg in response:` or
            use `response.next()` for manual pagination.
        """
        response = await self._request_asyncio(
            method="get",
            path="/v1/webhooks",
            query_params=options._query_params(),
            header_params=options._header_params(),
        )

        def _fetch_sync(iterator: str) -> ListResponse[MessageOut]:
            opts = MessageListOptions(limit=options.limit, iterator=iterator)
            resp = self._request_sync(
                method="get",
                path="/v1/webhooks",
                query_params=opts._query_params(),
                header_params=opts._header_params(),
            )
            return build_list_response(
                resp.json(), MessageOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async
            )

        async def _fetch_async(iterator: str) -> ListResponse[MessageOut]:
            opts = MessageListOptions(limit=options.limit, iterator=iterator)
            resp = await self._request_asyncio(
                method="get",
                path="/v1/webhooks",
                query_params=opts._query_params(),
                header_params=opts._header_params(),
            )
            return build_list_response(
                resp.json(), MessageOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async
            )

        return build_list_response(
            response.json(), MessageOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async
        )

    async def create(
        self,
        endpoint_id: str,
        event: str,
        data: dict,
        options: MessageCreateOptions = MessageCreateOptions(),
    ) -> MessageOut:
        """Send a webhook.

        Args:
            endpoint_id: The target endpoint ID
            event: Event type (e.g. "order.created")
            data: Webhook payload
        """
        body = {
            "endpoint_id": endpoint_id,
            "event": event,
            "data": data,
        }
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/webhooks",
            header_params=options._header_params(),
            json_body=json.dumps(body),
        )
        return MessageOut.model_validate(response.json())

    async def get(self, delivery_id: str) -> MessageOut:
        """Get a delivery by ID."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/webhooks/{id}",
            path_params={"id": delivery_id},
        )
        return MessageOut.model_validate(response.json())

    async def replay(self, delivery_id: str) -> MessageOut:
        """Replay a webhook delivery."""
        response = await self._request_asyncio(
            method="post",
            path="/v1/webhooks/{id}/replay",
            path_params={"id": delivery_id},
        )
        return MessageOut.model_validate(response.json())

    async def batch(self, webhooks: t.List[dict]) -> dict:
        """Send multiple webhooks in batch.

        Args:
            webhooks: List of {endpoint_id, event, data} dicts
        """
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/webhooks/batch",
            json_body=json.dumps({"webhooks": webhooks}),
        )
        return response.json()

    async def get_attempts(self, delivery_id: str) -> t.List[dict]:
        """Get delivery attempts for a delivery."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/webhooks/{id}/attempts",
            path_params={"id": delivery_id},
        )
        data = response.json()
        if isinstance(data, list):
            return data
        return data.get("data", data)


class Message(ApiBase):
    def list(
        self, options: MessageListOptions = MessageListOptions()
    ) -> ListResponse[MessageOut]:
        """List webhook deliveries with pagination support.

        Returns:
            ListResponse[MessageOut] — iterate with `for msg in response:` or
            use `response.next()` for manual pagination.
        """
        response = self._request_sync(
            method="get",
            path="/v1/webhooks",
            query_params=options._query_params(),
            header_params=options._header_params(),
        )

        def _fetch_sync(iterator: str) -> ListResponse[MessageOut]:
            opts = MessageListOptions(limit=options.limit, iterator=iterator)
            resp = self._request_sync(
                method="get",
                path="/v1/webhooks",
                query_params=opts._query_params(),
                header_params=opts._header_params(),
            )
            return build_list_response(resp.json(), MessageOut, fetch_fn=_fetch_sync)

        return build_list_response(
            response.json(), MessageOut, fetch_fn=_fetch_sync
        )

    def create(
        self,
        endpoint_id: str,
        event: str,
        data: dict,
        options: MessageCreateOptions = MessageCreateOptions(),
    ) -> MessageOut:
        """Send a webhook.

        Args:
            endpoint_id: The target endpoint ID
            event: Event type (e.g. "order.created")
            data: Webhook payload
        """
        body = {
            "endpoint_id": endpoint_id,
            "event": event,
            "data": data,
        }
        import json
        response = self._request_sync(
            method="post",
            path="/v1/webhooks",
            header_params=options._header_params(),
            json_body=json.dumps(body),
        )
        return MessageOut.model_validate(response.json())

    def get(self, delivery_id: str) -> MessageOut:
        """Get a delivery by ID."""
        response = self._request_sync(
            method="get",
            path="/v1/webhooks/{id}",
            path_params={"id": delivery_id},
        )
        return MessageOut.model_validate(response.json())

    def replay(self, delivery_id: str) -> MessageOut:
        """Replay a webhook delivery."""
        response = self._request_sync(
            method="post",
            path="/v1/webhooks/{id}/replay",
            path_params={"id": delivery_id},
        )
        return MessageOut.model_validate(response.json())

    def batch(self, webhooks: t.List[dict]) -> dict:
        """Send multiple webhooks in batch."""
        import json
        response = self._request_sync(
            method="post",
            path="/v1/webhooks/batch",
            json_body=json.dumps({"webhooks": webhooks}),
        )
        return response.json()

    def get_attempts(self, delivery_id: str) -> t.List[dict]:
        """Get delivery attempts for a delivery."""
        response = self._request_sync(
            method="get",
            path="/v1/webhooks/{id}/attempts",
            path_params={"id": delivery_id},
        )
        data = response.json()
        if isinstance(data, list):
            return data
        return data.get("data", data)
