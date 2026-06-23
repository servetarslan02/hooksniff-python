"""Stream resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class StreamResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list_channels(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/stream/channels")

    def create_channel(self, name: str, description: str = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/stream/channels", body)

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/stream/channels/{channel_id}")

    def delete_channel(self, channel_id: str) -> None:
        self.http.request("DELETE", f"/v1/stream/channels/{channel_id}")

    def list_messages(self, channel_id: str) -> List[Dict[str, Any]]:
        return self.http.request("GET", f"/v1/stream/channels/{channel_id}/messages")

    def publish(self, channel_id: str, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/stream/publish", {
            "channel_id": channel_id, "event": event, "data": data
        })

    def list_subscriptions(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/stream/subscriptions")

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/stream/subscriptions/{subscription_id}")

    def disconnect_subscription(self, subscription_id: str) -> None:
        self.http.request("DELETE", f"/v1/stream/subscriptions/{subscription_id}")
