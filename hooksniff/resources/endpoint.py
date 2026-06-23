"""Endpoint resource."""

from typing import Any, Dict
from ..http_client import HttpClient, PaginatedList


class EndpointResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def create(self, url: str, application_id: str, description: str = None, **kwargs) -> Dict[str, Any]:
        body: Dict[str, Any] = {"url": url, "application_id": application_id}
        if description:
            body["description"] = description
        body.update(kwargs)
        return self.http.request("POST", "/v1/endpoints", body)

    def list(self, per_page: int = 50) -> PaginatedList:
        return PaginatedList(self.http, "/v1/endpoints", per_page=per_page)

    def get(self, endpoint_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/endpoints/{endpoint_id}")

    def update(self, endpoint_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/endpoints/{endpoint_id}", kwargs)

    def delete(self, endpoint_id: str) -> None:
        self.http.request("DELETE", f"/v1/endpoints/{endpoint_id}")

    def rotate_secret(self, endpoint_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/endpoints/{endpoint_id}/rotate-secret")
