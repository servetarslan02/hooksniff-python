"""Team resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class TeamResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/teams")

    def create(self, name: str, description: str = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/teams", body)

    def get(self, team_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/teams/{team_id}")

    def delete(self, team_id: str) -> None:
        self.http.request("DELETE", f"/v1/teams/{team_id}")

    def list_members(self, team_id: str) -> List[Dict[str, Any]]:
        return self.http.request("GET", f"/v1/teams/{team_id}/members")

    def invite_member(self, team_id: str, email: str, role: str = "viewer") -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/teams/{team_id}/members", {"email": email, "role": role})

    def remove_member(self, team_id: str, member_id: str) -> None:
        self.http.request("DELETE", f"/v1/teams/{team_id}/members/{member_id}")
