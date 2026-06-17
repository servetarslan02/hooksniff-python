"""
HookSniff Python SDK client.

Usage:
    from hooksniff import HookSniff

    hs = HookSniff("hr_live_...")

    # Create application
    app = hs.application.create(name="My App")

    # Create endpoint
    ep = hs.endpoint.create(url="https://app.com/webhook", application_id=app["id"])

    # Send webhook
    delivery = hs.webhook.send(endpoint_id=ep["id"], event="order.created", data={"id": "123"})

    # Auto-pagination
    for ep in hs.endpoint.list():
        print(ep["url"])
"""

from typing import Any, Dict
from .http_client import HttpClient
from .resources import (
    ApplicationResource,
    EndpointResource,
    WebhookResource,
    ApiKeyResource,
    AnalyticsResource,
    SearchResource,
    HealthResource,
    BillingResource,
    NotificationResource,
    CortexResource,
    TeamResource,
    AlertResource,
    TemplateResource,
    SchemaResource,
    ConnectorResource,
    StreamResource,
    BackgroundTaskResource,
    IntegrationResource,
    ServiceTokenResource,
    OperationalWebhookResource,
    RateLimitResource,
    AuditResource,
    SsoResource,
    CustomDomainResource,
    EnvironmentResource,
)


class HookSniff:
    """
    HookSniff SDK client.

    Args:
        api_key: Your HookSniff API key (hr_live_* or hr_test_*)
        base_url: Custom API URL (optional)
        timeout: Request timeout in seconds (default: 30)
        retries: Max retries on 5xx/429 (default: 3)

    Example:
        hs = HookSniff("hr_live_...")
        app = hs.application.create(name="My App")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        timeout: int = None,
        retries: int = None,
        headers: Dict[str, str] = None,
    ):
        self.http = HttpClient(api_key, base_url, timeout, retries, headers)

        # Resources
        self.application = ApplicationResource(self.http)
        self.endpoint = EndpointResource(self.http)
        self.webhook = WebhookResource(self.http)
        self.api_key = ApiKeyResource(self.http)
        self.analytics = AnalyticsResource(self.http)
        self.search = SearchResource(self.http)
        self.health = HealthResource(self.http)
        self.billing = BillingResource(self.http)
        self.notification = NotificationResource(self.http)
        self.cortex = CortexResource(self.http)
        self.team = TeamResource(self.http)
        self.alert = AlertResource(self.http)
        self.template = TemplateResource(self.http)
        self.schema = SchemaResource(self.http)
        self.connector = ConnectorResource(self.http)
        self.stream = StreamResource(self.http)
        self.background_task = BackgroundTaskResource(self.http)
        self.integration = IntegrationResource(self.http)
        self.service_token = ServiceTokenResource(self.http)
        self.operational_webhook = OperationalWebhookResource(self.http)
        self.rate_limit = RateLimitResource(self.http)
        self.audit = AuditResource(self.http)
        self.sso = SsoResource(self.http)
        self.custom_domain = CustomDomainResource(self.http)
        self.environment = EnvironmentResource(self.http)

    def me(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self.http.request("GET", "/v1/auth/me")
