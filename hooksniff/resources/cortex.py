"""Cortex AI resource."""

from typing import Any, Dict, List
from ..http_client import HttpClient


class CortexResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def insights(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/cortex/insights")
        if isinstance(response, dict) and "insights" in response:
            raw = response["insights"]
            result = []
            for row in raw:
                if isinstance(row, list) and len(row) >= 10:
                    result.append({
                        "id": row[0],
                        "customer_id": row[1],
                        "type": row[2],
                        "title": row[3],
                        "description": row[4],
                        "severity": row[5],
                        "metadata": row[7] if len(row) > 7 else {},
                        "created_at": row[9] if len(row) > 9 else None,
                    })
                else:
                    result.append(row)
            return result
        return response if isinstance(response, list) else []

    def anomalies(self, endpoint_id: str = None) -> List[Dict[str, Any]]:
        path = "/v1/cortex/anomalies"
        if endpoint_id:
            path += f"?endpoint_id={endpoint_id}"
        return self.http.request("GET", path)

    def predict(self, endpoint_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/cortex/predict/{endpoint_id}")

    def auto_heal(self, endpoint_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/cortex/auto-heal/{endpoint_id}")
