"""Billing resource."""

from typing import Any, Dict
from ..http_client import HttpClient


class BillingResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def subscription(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/billing/subscription")

    def upgrade(self, plan: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/billing/upgrade", {"plan": plan})

    def portal(self) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/billing/portal")

    def usage(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/billing/usage")

    def invoices(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/billing/invoices")
