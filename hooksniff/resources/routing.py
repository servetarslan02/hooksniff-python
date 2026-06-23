"""Routing resources: Rate limits, Audit log."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class RateLimitResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/rate-limits")


class AuditResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/audit-log")
