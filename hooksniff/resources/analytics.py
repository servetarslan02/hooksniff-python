"""Analytics resource."""

from typing import Any
from ..http_client import HttpClient


class AnalyticsResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def deliveries(self, range: str = "24h") -> Any:
        return self.http.request("GET", f"/v1/analytics/deliveries?range={range}")

    def success_rate(self, range: str = "24h") -> Any:
        return self.http.request("GET", f"/v1/analytics/success-rate?range={range}")

    def latency(self, range: str = "24h") -> Any:
        return self.http.request("GET", f"/v1/analytics/latency?range={range}")
