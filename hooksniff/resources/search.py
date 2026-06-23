"""Search resource."""

from typing import Any, Dict
from ..http_client import HttpClient


class SearchResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def deliveries(self, query: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/search?q={query}&page={page}&per_page={per_page}")
