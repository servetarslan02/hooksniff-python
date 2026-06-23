"""Advanced resources: Background tasks, Integrations, Service tokens, Operational webhooks."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class BackgroundTaskResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/background-tasks")

    def get(self, task_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/background-tasks/{task_id}")

    def cancel(self, task_id: str) -> None:
        self.http.request("POST", f"/v1/background-tasks/{task_id}/cancel")


class IntegrationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/integrations")

    def get(self, integration_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/integrations/{integration_id}")

    def delete(self, integration_id: str) -> None:
        self.http.request("DELETE", f"/v1/integrations/{integration_id}")

    def rotate_key(self, integration_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/integrations/{integration_id}/rotate-key")


class ServiceTokenResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/service-tokens")

    def create(self, name: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/service-tokens", {"name": name})

    def delete(self, token_id: str) -> None:
        self.http.request("DELETE", f"/v1/service-tokens/{token_id}")


class OperationalWebhookResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/operational-webhooks")

    def create(self, url: str, events: List[str]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/operational-webhooks", {"url": url, "events": events})

    def get(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/operational-webhooks/{webhook_id}")

    def delete(self, webhook_id: str) -> None:
        self.http.request("DELETE", f"/v1/operational-webhooks/{webhook_id}")
