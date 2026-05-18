"""
Tests for pagination helper.

Verifies:
1. ListResponse works with plain arrays
2. ListResponse works with cursor-based pagination
3. Auto-paginate iterates through all pages
4. next() fetches next page correctly
5. Backward compatibility (len, bool, iter)
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from hooksniff.api.pagination import ListResponse, AsyncListResponse, build_list_response
from hooksniff.models.message_out import MessageOut


# --- Test Data ---

def make_message(id: str, event: str = "test.event") -> dict:
    return {
        "id": id,
        "event": event,
        "endpoint_id": "ep_456",
        "status": "success",
        "created_at": "2026-05-19T00:00:00Z",
    }


PAGE_1_RESPONSE = {
    "data": [make_message("msg_1"), make_message("msg_2")],
    "done": False,
    "iterator": "cursor_page_2",
}

PAGE_2_RESPONSE = {
    "data": [make_message("msg_3"), make_message("msg_4")],
    "done": False,
    "iterator": "cursor_page_3",
}

PAGE_3_RESPONSE = {
    "data": [make_message("msg_5")],
    "done": True,
    "iterator": None,
}

PLAIN_ARRAY_RESPONSE = [
    make_message("msg_1"),
    make_message("msg_2"),
    make_message("msg_3"),
]


# --- Tests ---

class TestListResponse:
    """Test ListResponse with cursor-based pagination."""

    def test_plain_array_returns_done(self):
        """Plain array response should have done=True."""
        resp = build_list_response(PLAIN_ARRAY_RESPONSE, MessageOut)
        assert resp.done is True
        assert len(resp.data) == 3
        assert resp.iterator is None

    def test_cursor_pagination_first_page(self):
        """First page should have done=False and iterator."""
        resp = build_list_response(PAGE_1_RESPONSE, MessageOut)
        assert resp.done is False
        assert resp.iterator == "cursor_page_2"
        assert len(resp.data) == 2
        assert resp.data[0].id == "msg_1"

    def test_cursor_pagination_last_page(self):
        """Last page should have done=True and no iterator."""
        resp = build_list_response(PAGE_3_RESPONSE, MessageOut)
        assert resp.done is True
        assert resp.iterator is None
        assert len(resp.data) == 1

    def test_next_fetches_next_page(self):
        """next() should call fetch_fn with iterator."""
        def mock_fetch(iterator: str) -> ListResponse[MessageOut]:
            assert iterator == "cursor_page_2"
            return build_list_response(PAGE_3_RESPONSE, MessageOut, fetch_fn=mock_fetch)

        page1 = build_list_response(PAGE_1_RESPONSE, MessageOut, fetch_fn=mock_fetch)
        page2 = page1.next()
        assert page2.done is True
        assert len(page2.data) == 1
        assert page2.data[0].id == "msg_5"

    def test_next_raises_on_done(self):
        """next() should raise RuntimeError when done."""
        resp = build_list_response(PAGE_3_RESPONSE, MessageOut)
        with pytest.raises(RuntimeError, match="No more pages"):
            resp.next()

    def test_auto_paginate_iterates_all(self):
        """Iterating should go through all pages automatically."""
        call_count = [0]

        def mock_fetch(iterator: str) -> ListResponse[MessageOut]:
            call_count[0] += 1
            if iterator == "cursor_page_2":
                return build_list_response(
                    PAGE_2_RESPONSE, MessageOut, fetch_fn=mock_fetch
                )
            elif iterator == "cursor_page_3":
                return build_list_response(
                    PAGE_3_RESPONSE, MessageOut, fetch_fn=mock_fetch
                )
            raise ValueError(f"Unexpected iterator: {iterator}")

        page1 = build_list_response(PAGE_1_RESPONSE, MessageOut, fetch_fn=mock_fetch)
        all_items = list(page1)

        assert len(all_items) == 5
        assert [item.id for item in all_items] == [
            "msg_1", "msg_2", "msg_3", "msg_4", "msg_5"
        ]
        assert call_count[0] == 2  # Fetched page 2 and page 3

    def test_bool_true_when_items(self):
        """bool(response) should be True when there are items."""
        resp = build_list_response(PAGE_1_RESPONSE, MessageOut)
        assert bool(resp) is True

    def test_bool_false_when_empty(self):
        """bool(response) should be False when data is empty."""
        empty_response = {"data": [], "done": True, "iterator": None}
        resp = build_list_response(empty_response, MessageOut)
        assert bool(resp) is False

    def test_len_returns_page_count(self):
        """len(response) should return number of items in current page."""
        resp = build_list_response(PAGE_1_RESPONSE, MessageOut)
        assert len(resp) == 2

    def test_deliveries_key_format(self):
        """Should handle 'deliveries' key instead of 'data'."""
        deliveries_response = {
            "deliveries": [make_message("msg_1")],
            "done": True,
        }
        resp = build_list_response(deliveries_response, MessageOut)
        assert len(resp.data) == 1
        assert resp.done is True

    def test_build_response_stores_model_class(self):
        """build_list_response should store model class for later use."""
        resp = build_list_response(PAGE_1_RESPONSE, MessageOut)
        assert resp._model_class == MessageOut


class TestAsyncListResponse:
    """Test AsyncListResponse wrapper."""

    @pytest.mark.asyncio
    async def test_async_iteration(self):
        """Async iteration should go through all items."""
        call_count = [0]

        def mock_fetch(iterator: str) -> ListResponse[MessageOut]:
            call_count[0] += 1
            if iterator == "cursor_page_2":
                return build_list_response(
                    PAGE_2_RESPONSE, MessageOut,
                    fetch_fn=mock_fetch, fetch_async_fn=mock_fetch_async,
                )
            elif iterator == "cursor_page_3":
                return build_list_response(
                    PAGE_3_RESPONSE, MessageOut,
                    fetch_fn=mock_fetch, fetch_async_fn=mock_fetch_async,
                )
            raise ValueError(f"Unexpected iterator: {iterator}")

        async def mock_fetch_async(iterator: str) -> ListResponse[MessageOut]:
            return mock_fetch(iterator)

        page1 = build_list_response(
            PAGE_1_RESPONSE, MessageOut,
            fetch_fn=mock_fetch,
            fetch_async_fn=mock_fetch_async,
        )
        async_resp = AsyncListResponse(page1)

        all_items = []
        async for item in async_resp:
            all_items.append(item)

        assert len(all_items) == 5
        assert [item.id for item in all_items] == [
            "msg_1", "msg_2", "msg_3", "msg_4", "msg_5"
        ]

    def test_data_property(self):
        """AsyncListResponse.data should return sync data."""
        page = build_list_response(PAGE_1_RESPONSE, MessageOut)
        async_resp = AsyncListResponse(page)
        assert len(async_resp.data) == 2

    def test_done_property(self):
        """AsyncListResponse.done should return sync done."""
        page = build_list_response(PAGE_1_RESPONSE, MessageOut)
        async_resp = AsyncListResponse(page)
        assert async_resp.done is False


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_data_list(self):
        """Empty data list should work."""
        empty_response = {"data": [], "done": True}
        resp = build_list_response(empty_response, MessageOut)
        assert len(resp.data) == 0
        assert resp.done is True

    def test_single_item_response(self):
        """Single item should work."""
        single_response = {"data": [make_message("msg_1")], "done": True}
        resp = build_list_response(single_response, MessageOut)
        assert len(resp.data) == 1
        assert resp.data[0].id == "msg_1"

    def test_nested_data_formats(self):
        """Should handle different response formats."""
        # Format 1: {data: [...]}
        format1 = {"data": [make_message("msg_1")]}
        resp1 = build_list_response(format1, MessageOut)
        assert len(resp1.data) == 1

        # Format 2: {deliveries: [...]}
        format2 = {"deliveries": [make_message("msg_2")]}
        resp2 = build_list_response(format2, MessageOut)
        assert len(resp2.data) == 1

        # Format 3: [...]
        format3 = [make_message("msg_3")]
        resp3 = build_list_response(format3, MessageOut)
        assert len(resp3.data) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
