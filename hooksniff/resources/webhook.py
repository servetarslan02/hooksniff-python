"""Webhook resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient, PaginatedList


class WebhookResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def send(self, endpoint_id: str, event: str, data: Dict[str, Any], idempotency_key: str = None) -> Dict[str, Any]:
        body = {"endpoint_id": endpoint_id, "event": event, "data": data}
        options = {"idempotency_key": idempotency_key} if idempotency_key else None
        return self.http.request("POST", "/v1/webhooks", body, options)

    def send_batch(self, webhooks: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/webhooks/batch", {"webhooks": webhooks})

    def list(self, per_page: int = 50, endpoint_id: str = None, status: str = None) -> PaginatedList:
        params: Dict[str, str] = {}
        if endpoint_id:
            params["endpoint_id"] = endpoint_id
        if status:
            params["status"] = status
        return PaginatedList(self.http, "/v1/webhooks", params=params, per_page=per_page)

    def get(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/webhooks/{webhook_id}")

    def replay(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/webhooks/{webhook_id}/replay")

    def batch_replay(self, webhook_ids: List[str]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/webhooks/batch-replay", {"webhook_ids": webhook_ids})
