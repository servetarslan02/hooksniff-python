"""Platform resources: SSO, Custom domains, Environments."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class SsoResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def get_config(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/sso/config")


class CustomDomainResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/custom-domains")


class EnvironmentResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/environments")
