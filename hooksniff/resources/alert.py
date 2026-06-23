"""Alert resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class AlertResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/alerts")
        return response if isinstance(response, list) else response.get("alerts", [])

    def create(self, name: str, condition: str, threshold: int, channels: List[str]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/alerts", {
            "name": name, "condition": condition, "threshold": threshold, "channels": channels
        })

    def get(self, alert_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/alerts/{alert_id}")

    def update(self, alert_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/alerts/{alert_id}", kwargs)

    def delete(self, alert_id: str) -> None:
        self.http.request("DELETE", f"/v1/alerts/{alert_id}")

    def list_events(self, alert_id: str) -> List[Dict[str, Any]]:
        return self.http.request("GET", f"/v1/alerts/{alert_id}/events")
