"""Schema resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class SchemaResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/schemas")
        return response if isinstance(response, list) else response.get("schemas", [])

    def create(self, name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/schemas", {"name": name, "schema": schema})

    def get(self, schema_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/schemas/{schema_id}")

    def delete(self, schema_id: str) -> None:
        self.http.request("DELETE", f"/v1/schemas/{schema_id}")

    def validate(self, schema_id: str, data: Any) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/schemas/{schema_id}/validate", {"data": data})
