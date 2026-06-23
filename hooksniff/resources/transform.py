"""Transform resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class TransformResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self, endpoint_id: str) -> List[Dict[str, Any]]:
        return self.http.request("GET", f"/v1/endpoints/{endpoint_id}/transforms")

    def create(self, endpoint_id: str, name: str, code: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/endpoints/{endpoint_id}/transforms", {"name": name, "code": code})

    def get(self, endpoint_id: str, transform_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/endpoints/{endpoint_id}/transforms/{transform_id}")

    def update(self, endpoint_id: str, transform_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/endpoints/{endpoint_id}/transforms/{transform_id}", kwargs)

    def delete(self, endpoint_id: str, transform_id: str) -> None:
        self.http.request("DELETE", f"/v1/endpoints/{endpoint_id}/transforms/{transform_id}")
