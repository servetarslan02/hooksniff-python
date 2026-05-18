# This file is adapted for HookSniff API
# HookSniff uses /v1/... paths (not /v1/... HookSniff paths)
# The authenticated user is determined by the JWT token, no app_id needed.
import typing as t
from dataclasses import dataclass
from datetime import datetime

from ..models import (
    EndpointIn,
    EndpointOut,
    EndpointPatch,
    EndpointUpdate,
)
from .common import ApiBase, BaseOptions, serialize_params


@dataclass
class EndpointListOptions(BaseOptions):
    limit: t.Optional[int] = None
    """Limit the number of returned items"""
    page: t.Optional[int] = None
    """Page number for pagination"""

    def _query_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "limit": self.limit,
                "page": self.page,
            }
        )


@dataclass
class EndpointCreateOptions(BaseOptions):
    idempotency_key: t.Optional[str] = None

    def _header_params(self) -> t.Dict[str, str]:
        return serialize_params(
            {
                "idempotency-key": self.idempotency_key,
            }
        )


class EndpointAsync(ApiBase):
    async def list(
        self, options: EndpointListOptions = EndpointListOptions()
    ) -> t.List[EndpointOut]:
        """List all endpoints for the authenticated user."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/endpoints",
            query_params=options._query_params(),
            header_params=options._header_params(),
        )
        data = response.json()
        # HookSniff returns a plain array or {data: [...], total, has_more}
        if isinstance(data, list):
            return [EndpointOut.model_validate(item) for item in data]
        return [EndpointOut.model_validate(item) for item in data.get("data", data)]

    async def create(
        self,
        endpoint_in: EndpointIn,
        options: EndpointCreateOptions = EndpointCreateOptions(),
    ) -> EndpointOut:
        """Create a new endpoint."""
        response = await self._request_asyncio(
            method="post",
            path="/v1/endpoints",
            header_params=options._header_params(),
            json_body=endpoint_in.model_dump_json(exclude_unset=True, by_alias=True),
        )
        return EndpointOut.model_validate(response.json())

    async def get(self, endpoint_id: str) -> EndpointOut:
        """Get an endpoint by ID."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
        )
        return EndpointOut.model_validate(response.json())

    async def update(
        self, endpoint_id: str, endpoint_update: EndpointUpdate
    ) -> EndpointOut:
        """Update an endpoint."""
        response = await self._request_asyncio(
            method="put",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
            json_body=endpoint_update.model_dump_json(
                exclude_unset=True, by_alias=True
            ),
        )
        return EndpointOut.model_validate(response.json())

    async def delete(self, endpoint_id: str) -> None:
        """Delete an endpoint."""
        await self._request_asyncio(
            method="delete",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
        )

    async def patch(
        self, endpoint_id: str, endpoint_patch: EndpointPatch
    ) -> EndpointOut:
        """Partially update an endpoint."""
        response = await self._request_asyncio(
            method="patch",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
            json_body=endpoint_patch.model_dump_json(exclude_unset=True, by_alias=True),
        )
        return EndpointOut.model_validate(response.json())

    async def rotate_secret(self, endpoint_id: str) -> dict:
        """Rotate the endpoint's signing secret."""
        response = await self._request_asyncio(
            method="post",
            path="/v1/endpoints/{endpoint_id}/rotate-secret",
            path_params={"endpoint_id": endpoint_id},
        )
        return response.json()

    async def get_stats(
        self,
        endpoint_id: str,
        *,
        since: t.Optional[datetime] = None,
        until: t.Optional[datetime] = None,
    ) -> dict:
        """Get basic statistics for the endpoint."""
        params = serialize_params({"since": since, "until": until})
        response = await self._request_asyncio(
            method="get",
            path="/v1/endpoints/{endpoint_id}/stats",
            path_params={"endpoint_id": endpoint_id},
            query_params=params,
        )
        return response.json()


class Endpoint(ApiBase):
    def list(
        self, options: EndpointListOptions = EndpointListOptions()
    ) -> t.List[EndpointOut]:
        """List all endpoints for the authenticated user."""
        response = self._request_sync(
            method="get",
            path="/v1/endpoints",
            query_params=options._query_params(),
            header_params=options._header_params(),
        )
        data = response.json()
        if isinstance(data, list):
            return [EndpointOut.model_validate(item) for item in data]
        return [EndpointOut.model_validate(item) for item in data.get("data", data)]

    def create(
        self,
        endpoint_in: EndpointIn,
        options: EndpointCreateOptions = EndpointCreateOptions(),
    ) -> EndpointOut:
        """Create a new endpoint."""
        response = self._request_sync(
            method="post",
            path="/v1/endpoints",
            header_params=options._header_params(),
            json_body=endpoint_in.model_dump_json(exclude_unset=True, by_alias=True),
        )
        return EndpointOut.model_validate(response.json())

    def get(self, endpoint_id: str) -> EndpointOut:
        """Get an endpoint by ID."""
        response = self._request_sync(
            method="get",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
        )
        return EndpointOut.model_validate(response.json())

    def update(
        self, endpoint_id: str, endpoint_update: EndpointUpdate
    ) -> EndpointOut:
        """Update an endpoint."""
        response = self._request_sync(
            method="put",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
            json_body=endpoint_update.model_dump_json(
                exclude_unset=True, by_alias=True
            ),
        )
        return EndpointOut.model_validate(response.json())

    def delete(self, endpoint_id: str) -> None:
        """Delete an endpoint."""
        self._request_sync(
            method="delete",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
        )

    def patch(
        self, endpoint_id: str, endpoint_patch: EndpointPatch
    ) -> EndpointOut:
        """Partially update an endpoint."""
        response = self._request_sync(
            method="patch",
            path="/v1/endpoints/{endpoint_id}",
            path_params={"endpoint_id": endpoint_id},
            json_body=endpoint_patch.model_dump_json(exclude_unset=True, by_alias=True),
        )
        return EndpointOut.model_validate(response.json())

    def rotate_secret(self, endpoint_id: str) -> dict:
        """Rotate the endpoint's signing secret."""
        response = self._request_sync(
            method="post",
            path="/v1/endpoints/{endpoint_id}/rotate-secret",
            path_params={"endpoint_id": endpoint_id},
        )
        return response.json()

    def get_stats(
        self,
        endpoint_id: str,
        *,
        since: t.Optional[datetime] = None,
        until: t.Optional[datetime] = None,
    ) -> dict:
        """Get basic statistics for the endpoint."""
        params = serialize_params({"since": since, "until": until})
        response = self._request_sync(
            method="get",
            path="/v1/endpoints/{endpoint_id}/stats",
            path_params={"endpoint_id": endpoint_id},
            query_params=params,
        )
        return response.json()
