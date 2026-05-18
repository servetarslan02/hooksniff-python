"""Applications — Manage applications (group endpoints)."""

import typing as t
from .common import ApiBase


class ApplicationAsync(ApiBase):
    async def list(self) -> t.List[dict]:
        """List all applications."""
        response = await self._request_asyncio(method="get", path="/v1/applications", path_params={})
        data = response.json()
        return data if isinstance(data, list) else data.get("data", data)

    async def create(self, name: str, description: t.Optional[str] = None) -> dict:
        """Create a new application."""
        import json
        body: dict = {"name": name}
        if description:
            body["description"] = description
        response = await self._request_asyncio(method="post", path="/v1/applications", path_params={}, json_body=json.dumps(body))
        return response.json()

    async def get(self, application_id: str) -> dict:
        """Get an application by ID."""
        response = await self._request_asyncio(method="get", path="/v1/applications/{id}", path_params={"id": application_id})
        return response.json()

    async def update(self, application_id: str, name: t.Optional[str] = None, description: t.Optional[str] = None, is_active: t.Optional[bool] = None) -> dict:
        """Update an application."""
        import json
        body: dict = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if is_active is not None:
            body["is_active"] = is_active
        response = await self._request_asyncio(method="put", path="/v1/applications/{id}", path_params={"id": application_id}, json_body=json.dumps(body))
        return response.json()

    async def delete(self, application_id: str) -> None:
        """Delete an application."""
        await self._request_asyncio(method="delete", path="/v1/applications/{id}", path_params={"id": application_id})


class Application(ApiBase):
    def list(self) -> t.List[dict]:
        """List all applications."""
        response = self._request_sync(method="get", path="/v1/applications", path_params={})
        data = response.json()
        return data if isinstance(data, list) else data.get("data", data)

    def create(self, name: str, description: t.Optional[str] = None) -> dict:
        """Create a new application."""
        import json
        body: dict = {"name": name}
        if description:
            body["description"] = description
        response = self._request_sync(method="post", path="/v1/applications", path_params={}, json_body=json.dumps(body))
        return response.json()

    def get(self, application_id: str) -> dict:
        """Get an application by ID."""
        response = self._request_sync(method="get", path="/v1/applications/{id}", path_params={"id": application_id})
        return response.json()

    def update(self, application_id: str, name: t.Optional[str] = None, description: t.Optional[str] = None, is_active: t.Optional[bool] = None) -> dict:
        """Update an application."""
        import json
        body: dict = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if is_active is not None:
            body["is_active"] = is_active
        response = self._request_sync(method="put", path="/v1/applications/{id}", path_params={"id": application_id}, json_body=json.dumps(body))
        return response.json()

    def delete(self, application_id: str) -> None:
        """Delete an application."""
        self._request_sync(method="delete", path="/v1/applications/{id}", path_params={"id": application_id})
