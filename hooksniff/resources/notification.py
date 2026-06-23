"""Notification resource."""

from typing import Any, Dict
from ..http_client import HttpClient


class NotificationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self, per_page: int = 20) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/notifications?per_page={per_page}")

    def get_unread_count(self) -> Dict[str, Any]:
        response = self.http.request("GET", "/v1/notifications/unread-count")
        return {"count": response.get("unread_count", 0)}

    def mark_read(self, notification_id: str) -> None:
        self.http.request("POST", f"/v1/notifications/{notification_id}/read")

    def mark_all_read(self) -> None:
        self.http.request("POST", "/v1/notifications/read-all")
