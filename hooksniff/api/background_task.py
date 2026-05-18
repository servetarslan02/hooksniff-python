import typing as t

from .. import models
from ..models import BackgroundTaskOut
from .common import ApiBase
from .pagination import ListResponse, build_list_response


class BackgroundTaskAsync(ApiBase):
    async def list(self) -> ListResponse[BackgroundTaskOut]:
        """List all background tasks with pagination support."""
        response = await self._request_asyncio(
            method="get", path="/v1/background-tasks", path_params={},
        )

        def _fetch_sync(iterator: str) -> ListResponse[BackgroundTaskOut]:
            resp = self._request_sync(
                method="get", path="/v1/background-tasks",
                query_params={"iterator": iterator},
            )
            return build_list_response(resp.json(), BackgroundTaskOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        async def _fetch_async(iterator: str) -> ListResponse[BackgroundTaskOut]:
            resp = await self._request_asyncio(
                method="get", path="/v1/background-tasks",
                query_params={"iterator": iterator},
            )
            return build_list_response(resp.json(), BackgroundTaskOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

        return build_list_response(response.json(), BackgroundTaskOut, fetch_fn=_fetch_sync, fetch_async_fn=_fetch_async)

    async def get(self, task_id: str) -> BackgroundTaskOut:
        """Get a background task by ID."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/background-tasks/{task_id}",
            path_params={"task_id": task_id},
        )
        return BackgroundTaskOut.model_validate(response.json())

    async def cancel(self, task_id: str) -> BackgroundTaskOut:
        """Cancel a pending or running background task."""
        response = await self._request_asyncio(
            method="put",
            path="/v1/background-tasks/{task_id}",
            path_params={"task_id": task_id},
        )
        return BackgroundTaskOut.model_validate(response.json())


class BackgroundTask(ApiBase):
    def list(self) -> ListResponse[BackgroundTaskOut]:
        """List all background tasks with pagination support."""
        response = self._request_sync(
            method="get", path="/v1/background-tasks", path_params={},
        )

        def _fetch_sync(iterator: str) -> ListResponse[BackgroundTaskOut]:
            resp = self._request_sync(
                method="get", path="/v1/background-tasks",
                query_params={"iterator": iterator},
            )
            return build_list_response(resp.json(), BackgroundTaskOut, fetch_fn=_fetch_sync)

        return build_list_response(response.json(), BackgroundTaskOut, fetch_fn=_fetch_sync)

    def get(self, task_id: str) -> BackgroundTaskOut:
        """Get a background task by ID."""
        response = self._request_sync(
            method="get",
            path="/v1/background-tasks/{task_id}",
            path_params={"task_id": task_id},
        )
        return BackgroundTaskOut.model_validate(response.json())

    def cancel(self, task_id: str) -> BackgroundTaskOut:
        """Cancel a pending or running background task."""
        response = self._request_sync(
            method="put",
            path="/v1/background-tasks/{task_id}",
            path_params={"task_id": task_id},
        )
        return BackgroundTaskOut.model_validate(response.json())
