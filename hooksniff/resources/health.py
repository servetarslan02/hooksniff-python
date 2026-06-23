"""Health resource."""

from typing import Any, Dict
from ..http_client import HttpClient


class HealthResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def check(self) -> Dict[str, Any]:
        return self.http.request("GET", "/health")

    def outbound_ips(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/outbound-ips")
