"""
Pagination Helper for HookSniff SDK.

Provides automatic cursor-based pagination for list() methods.
Supports both sync and async iteration.

Usage (sync):
    # Auto-paginate through all items
    for msg in client.message.list():
        print(msg)

    # Manual pagination
    page = client.message.list()
    for msg in page.data:
        print(msg)
    if not page.done:
        next_page = page.next()

Usage (async):
    async for msg in client.message.async_list():
        print(msg)
"""

import typing as t
from dataclasses import dataclass

T = t.TypeVar("T")


@dataclass
class ListResponse(t.Generic[T]):
    """
    Paginated list response from HookSniff API.

    Attributes:
        data: List of items in current page
        done: Whether there are more pages
        iterator: Cursor for next page (None if done)
        prev_iterator: Cursor for previous page
    """

    data: t.List[T]
    done: bool
    iterator: t.Optional[str] = None
    prev_iterator: t.Optional[str] = None

    # Internal: store the fetch function for next()
    _fetch_fn: t.Optional[t.Callable] = None
    _fetch_async_fn: t.Optional[t.Callable] = None
    _model_class: t.Optional[t.Type] = None
    _path: t.Optional[str] = None
    _query_params: t.Optional[t.Dict[str, str]] = None
    _header_params: t.Optional[t.Dict[str, str]] = None

    def __iter__(self):
        """Iterate through ALL items across all pages (auto-paginate)."""
        page = self
        while True:
            for item in page.data:
                yield item
            if page.done or not page.iterator:
                break
            page = page.next()

    def __len__(self):
        """Return number of items in current page."""
        return len(self.data)

    def __bool__(self):
        """Return True if there are items."""
        return len(self.data) > 0

    def next(self) -> "ListResponse[T]":
        """
        Fetch the next page.

        Returns:
            ListResponse with next page of items

        Raises:
            RuntimeError: If no more pages or fetch function not set
        """
        if self.done or not self.iterator:
            raise RuntimeError("No more pages")
        if self._fetch_fn is None:
            raise RuntimeError("Pagination not configured for this response")
        return self._fetch_fn(self.iterator)

    async def next_async(self) -> "ListResponse[T]":
        """
        Fetch the next page (async).

        Returns:
            ListResponse with next page of items

        Raises:
            RuntimeError: If no more pages or fetch function not set
        """
        if self.done or not self.iterator:
            raise RuntimeError("No more pages")
        if self._fetch_async_fn is None:
            raise RuntimeError("Pagination not configured for this response")
        return await self._fetch_async_fn(self.iterator)


class AsyncListResponse(t.Generic[T]):
    """
    Async version of ListResponse for async iteration.

    Usage:
        async for msg in client.message.async_list():
            print(msg)
    """

    def __init__(self, sync_response: ListResponse[T]):
        self._sync = sync_response

    @property
    def data(self) -> t.List[T]:
        return self._sync.data

    @property
    def done(self) -> bool:
        return self._sync.done

    @property
    def iterator(self) -> t.Optional[str]:
        return self._sync.iterator

    def __aiter__(self):
        """Async iterate through ALL items across all pages."""
        self._current = self._sync
        self._index = 0
        return self

    async def __anext__(self) -> T:
        """Get next item, auto-fetching next page if needed."""
        while True:
            if self._index < len(self._current.data):
                item = self._current.data[self._index]
                self._index += 1
                return item
            if self._current.done or not self._current.iterator:
                raise StopAsyncIteration
            self._current = await self._current.next_async()
            self._index = 0

    async def next(self) -> "AsyncListResponse[T]":
        """Fetch next page (async)."""
        next_sync = await self._sync.next_async()
        return AsyncListResponse(next_sync)


def build_list_response(
    response_data: dict,
    model_class: t.Type[T],
    fetch_fn: t.Optional[t.Callable] = None,
    fetch_async_fn: t.Optional[t.Callable] = None,
) -> ListResponse[T]:
    """
    Build a ListResponse from API response data.

    Handles multiple response formats:
    - {"data": [...], "done": bool, "iterator": "..."}
    - {"deliveries": [...]}
    - [...] (plain array)

    Args:
        response_data: Raw JSON response from API
        model_class: Pydantic model class to validate items
        fetch_fn: Sync function to fetch next page (takes iterator string)
        fetch_async_fn: Async function to fetch next page

    Returns:
        ListResponse with parsed items
    """
    # Handle different response formats
    if isinstance(response_data, list):
        items = [model_class.model_validate(item) for item in response_data]
        return ListResponse(
            data=items,
            done=True,  # Plain array = no pagination
            iterator=None,
            _fetch_fn=fetch_fn,
            _fetch_async_fn=fetch_async_fn,
            _model_class=model_class,
        )

    # Extract items from response
    for key in ("data", "deliveries", "items"):
        if key in response_data and isinstance(response_data[key], list):
            raw_items = response_data[key]
            break
    else:
        raw_items = response_data

    if isinstance(raw_items, dict):
        # Fallback: wrap single object in list
        raw_items = [raw_items]

    items = [model_class.model_validate(item) for item in raw_items]

    # Extract pagination info
    done = response_data.get("done", True)
    iterator = response_data.get("iterator")
    prev_iterator = response_data.get("prev_iterator")

    # If done is not explicitly set, infer from iterator
    if "done" not in response_data:
        done = iterator is None

    return ListResponse(
        data=items,
        done=done,
        iterator=iterator,
        prev_iterator=prev_iterator,
        _fetch_fn=fetch_fn,
        _fetch_async_fn=fetch_async_fn,
        _model_class=model_class,
    )
