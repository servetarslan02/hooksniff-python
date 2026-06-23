"""Broadcast resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class BroadcastResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/broadcasts")

    def create(self, title: str, message: str, scheduled_at: str = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"title": title, "message": message}
        if scheduled_at:
            body["scheduled_at"] = scheduled_at
        return self.http.request("POST", "/v1/broadcasts", body)

    def get(self, broadcast_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/broadcasts/{broadcast_id}")

    def delete(self, broadcast_id: str) -> None:
        self.http.request("DELETE", f"/v1/broadcasts/{broadcast_id}")

    def send(self, broadcast_id: str) -> None:
        self.http.request("POST", f"/v1/broadcasts/{broadcast_id}/send")
