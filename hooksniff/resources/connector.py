"""Connector resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class ConnectorResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/connectors")

    def get(self, connector_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/connectors/{connector_id}")

    def list_configs(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/connectors/configs")

    def create_config(self, connector_id: str, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/connectors/configs", {
            "connector_id": connector_id, "name": name, "config": config
        })

    def get_config(self, config_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/connectors/configs/{config_id}")

    def update_config(self, config_id: str, **kwargs) -> Dict[str, Any]:
        return self.http.request("PUT", f"/v1/connectors/configs/{config_id}", kwargs)

    def delete_config(self, config_id: str) -> None:
        self.http.request("DELETE", f"/v1/connectors/configs/{config_id}")
