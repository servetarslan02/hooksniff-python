"""Template resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class TemplateResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/templates")
        return response if isinstance(response, list) else response.get("templates", [])

    def create(self, name: str, content: str, description: str = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name, "content": content}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/templates", body)

    def get(self, template_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/templates/{template_id}")

    def update(self, template_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/templates/{template_id}", kwargs)

    def delete(self, template_id: str) -> None:
        self.http.request("DELETE", f"/v1/templates/{template_id}")
