# Adapted for HookSniff API
# HookSniff uses /v1/webhooks/{id}/attempts for attempt operations
import typing as t
from dataclasses import dataclass
from datetime import datetime

from .. import models
from ..models import (
    MessageAttemptOut,
)
from .common import ApiBase, BaseOptions, serialize_params


@dataclass
class MessageAttemptListOptions(BaseOptions):
    limit: t.Optional[int] = None
    page: t.Optional[int] = None
    status: t.Optional[str] = None

    def _query_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "limit": self.limit,
                "page": self.page,
                "status": self.status,
            }
        )


@dataclass
class MessageAttemptResendOptions(BaseOptions):
    idempotency_key: t.Optional[str] = None

    def _header_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "idempotency-key": self.idempotency_key,
            }
        )


class MessageAttemptAsync(ApiBase):
    async def list_by_delivery(
        self,
        delivery_id: str,
        options: MessageAttemptListOptions = MessageAttemptListOptions(),
    ) -> t.List[MessageAttemptOut]:
        """List attempts for a delivery."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/webhooks/{id}/attempts",
            path_params={"id": delivery_id},
            query_params=options._query_params(),
            header_params=options._header_params(),
        )
        data = response.json()
        if isinstance(data, list):
            return [MessageAttemptOut.model_validate(item) for item in data]
        return [MessageAttemptOut.model_validate(item) for item in data.get("data", data)]

    async def get(
        self,
        delivery_id: str,
        attempt_id: str,
    ) -> MessageAttemptOut:
        """Get a specific attempt."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/webhooks/{id}/attempts/{attempt_id}",
            path_params={"id": delivery_id, "attempt_id": attempt_id},
        )
        return MessageAttemptOut.model_validate(response.json())

    async def resend(
        self,
        delivery_id: str,
        endpoint_id: str,
        options: MessageAttemptResendOptions = MessageAttemptResendOptions(),
    ) -> dict:
        """Resend a message to the specified endpoint."""
        response = await self._request_asyncio(
            method="post",
            path="/v1/webhooks/{id}/endpoint/{endpoint_id}/resend",
            path_params={"id": delivery_id, "endpoint_id": endpoint_id},
            header_params=options._header_params(),
        )
        return response.json()


class MessageAttempt(ApiBase):
    def list_by_delivery(
        self,
        delivery_id: str,
        options: MessageAttemptListOptions = MessageAttemptListOptions(),
    ) -> t.List[MessageAttemptOut]:
        """List attempts for a delivery."""
        response = self._request_sync(
            method="get",
            path="/v1/webhooks/{id}/attempts",
            path_params={"id": delivery_id},
            query_params=options._query_params(),
            header_params=options._header_params(),
        )
        data = response.json()
        if isinstance(data, list):
            return [MessageAttemptOut.model_validate(item) for item in data]
        return [MessageAttemptOut.model_validate(item) for item in data.get("data", data)]

    def get(
        self,
        delivery_id: str,
        attempt_id: str,
    ) -> MessageAttemptOut:
        """Get a specific attempt."""
        response = self._request_sync(
            method="get",
            path="/v1/webhooks/{id}/attempts/{attempt_id}",
            path_params={"id": delivery_id, "attempt_id": attempt_id},
        )
        return MessageAttemptOut.model_validate(response.json())

    def resend(
        self,
        delivery_id: str,
        endpoint_id: str,
        options: MessageAttemptResendOptions = MessageAttemptResendOptions(),
    ) -> dict:
        """Resend a message to the specified endpoint."""
        response = self._request_sync(
            method="post",
            path="/v1/webhooks/{id}/endpoint/{endpoint_id}/resend",
            path_params={"id": delivery_id, "endpoint_id": endpoint_id},
            header_params=options._header_params(),
        )
        return response.json()
