"""API Key resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class ApiKeyResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/api-keys")

    def create(self, name: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/api-keys", {"name": name})

    def delete(self, api_key_id: str) -> None:
        self.http.request("DELETE", f"/v1/api-keys/{api_key_id}")

    def rotate(self, api_key_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/api-keys/{api_key_id}/rotate")
