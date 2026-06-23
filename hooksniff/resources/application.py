"""Application resource."""

from typing import Any, Dict
from ..http_client import HttpClient, PaginatedList


class ApplicationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def create(self, name: str, description: str = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/applications", body)

    def list(self, per_page: int = 50) -> PaginatedList:
        return PaginatedList(self.http, "/v1/applications", per_page=per_page)

    def get(self, application_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/applications/{application_id}")

    def update(self, application_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/applications/{application_id}", kwargs)

    def delete(self, application_id: str) -> None:
        self.http.request("DELETE", f"/v1/applications/{application_id}")
