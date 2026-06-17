from typing import Any, Dict, List, Optional
from .http_client import HttpClient, PaginatedList


class ApplicationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def create(self, name: str, description: str = None) -> Dict[str, Any]:
        body = {"name": name}
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


class EndpointResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def create(self, url: str, application_id: str, description: str = None, **kwargs) -> Dict[str, Any]:
        body = {"url": url, "application_id": application_id}
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


class WebhookResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def send(self, endpoint_id: str, event: str, data: Dict[str, Any], idempotency_key: str = None) -> Dict[str, Any]:
        body = {"endpoint_id": endpoint_id, "event": event, "data": data}
        options = {"idempotency_key": idempotency_key} if idempotency_key else None
        return self.http.request("POST", "/v1/webhooks", body, options)

    def send_batch(self, webhooks: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/webhooks/batch", {"webhooks": webhooks})

    def list(self, per_page: int = 50, endpoint_id: str = None, status: str = None) -> PaginatedList:
        params = {}
        if endpoint_id:
            params["endpoint_id"] = endpoint_id
        if status:
            params["status"] = status
        return PaginatedList(self.http, "/v1/webhooks", params=params, per_page=per_page)

    def get(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/webhooks/{webhook_id}")

    def replay(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/v1/webhooks/{webhook_id}/replay")


class ApiKeyResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/api-keys")

    def create(self, name: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/api-keys", {"name": name})

    def delete(self, api_key_id: str) -> None:
        self.http.request("DELETE", f"/v1/api-keys/{api_key_id}")


class AnalyticsResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def deliveries(self, range: str = "24h") -> Any:
        return self.http.request("GET", f"/v1/analytics/deliveries?range={range}")

    def success_rate(self, range: str = "24h") -> Any:
        return self.http.request("GET", f"/v1/analytics/success-rate?range={range}")


class SearchResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def deliveries(self, query: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/search?q={query}&page={page}&per_page={per_page}")


class HealthResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def check(self) -> Dict[str, Any]:
        return self.http.request("GET", "/health")

    def outbound_ips(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/outbound-ips")


class BillingResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def subscription(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/billing/subscription")

    def upgrade(self, plan: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/billing/upgrade", {"plan": plan})

    def portal(self) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/billing/portal")


class NotificationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self, per_page: int = 20) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/notifications?per_page={per_page}")

    def get_unread_count(self) -> Dict[str, Any]:
        response = self.http.request("GET", "/v1/notifications/unread-count")
        return {"count": response.get("unread_count", 0)}

    def mark_read(self, notification_id: str) -> None:
        self.http.request("POST", f"/v1/notifications/{notification_id}/read")

    def mark_all_read(self) -> None:
        self.http.request("POST", "/v1/notifications/read-all")


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


class TeamResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/teams")

    def create(self, name: str, description: str = None) -> Dict[str, Any]:
        body = {"name": name}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/teams", body)

    def get(self, team_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/teams/{team_id}")

    def delete(self, team_id: str) -> None:
        self.http.request("DELETE", f"/v1/teams/{team_id}")


class AlertResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/alerts")
        return response if isinstance(response, list) else response.get("alerts", [])

    def create(self, name: str, condition: str, threshold: int, channels: List[str]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/alerts", {
            "name": name, "condition": condition, "threshold": threshold, "channels": channels
        })

    def get(self, alert_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/alerts/{alert_id}")

    def delete(self, alert_id: str) -> None:
        self.http.request("DELETE", f"/v1/alerts/{alert_id}")


class TemplateResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        response = self.http.request("GET", "/v1/templates")
        return response if isinstance(response, list) else response.get("templates", [])

    def get(self, template_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/templates/{template_id}")


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


class StreamResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list_channels(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/stream/channels")

    def create_channel(self, name: str, description: str = None) -> Dict[str, Any]:
        body = {"name": name}
        if description:
            body["description"] = description
        return self.http.request("POST", "/v1/stream/channels", body)

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/stream/channels/{channel_id}")

    def delete_channel(self, channel_id: str) -> None:
        self.http.request("DELETE", f"/v1/stream/channels/{channel_id}")

    def publish(self, channel_id: str, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/stream/publish", {
            "channel_id": channel_id, "event": event, "data": data
        })

    def list_subscriptions(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/stream/subscriptions")


class BackgroundTaskResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/background-tasks")

    def get(self, task_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/background-tasks/{task_id}")

    def cancel(self, task_id: str) -> None:
        self.http.request("POST", f"/v1/background-tasks/{task_id}/cancel")


class IntegrationResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/integrations")

    def get(self, integration_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/integrations/{integration_id}")

    def delete(self, integration_id: str) -> None:
        self.http.request("DELETE", f"/v1/integrations/{integration_id}")


class ServiceTokenResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/service-tokens")

    def create(self, name: str) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/service-tokens", {"name": name})

    def delete(self, token_id: str) -> None:
        self.http.request("DELETE", f"/v1/service-tokens/{token_id}")


class OperationalWebhookResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/operational-webhooks")

    def create(self, url: str, events: List[str]) -> Dict[str, Any]:
        return self.http.request("POST", "/v1/operational-webhooks", {"url": url, "events": events})

    def get(self, webhook_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/v1/operational-webhooks/{webhook_id}")

    def delete(self, webhook_id: str) -> None:
        self.http.request("DELETE", f"/v1/operational-webhooks/{webhook_id}")


class RateLimitResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> List[Dict[str, Any]]:
        return self.http.request("GET", "/v1/rate-limits")


class AuditResource:
    def __init__(self, http: HttpClient):
        self.http = http

    def list(self) -> Dict[str, Any]:
        return self.http.request("GET", "/v1/audit-log")


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
