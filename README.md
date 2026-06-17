# HookSniff Python SDK

Official Python SDK for [HookSniff](https://hooksniff.vercel.app) — the webhook infrastructure for developers.

## Installation

```bash
pip install hooksniff
```

## Quick Start

```python
from hooksniff import HookSniff

hs = HookSniff("hr_live_...")

# Create an application
app = hs.application.create(name="My App")

# Create an endpoint
ep = hs.endpoint.create(
    url="https://app.com/webhook",
    application_id=app["id"],
    description="Order notifications",
)

# Send a webhook
delivery = hs.webhook.send(
    endpoint_id=ep["id"],
    event="order.created",
    data={"order_id": "12345", "amount": 99.99},
)

print(delivery["id"])  # "msg_..."
```

## Features

- **Simple API** — 2 lines to send a webhook
- **Auto-pagination** — Iterate through all resources automatically
- **Auto-retry** — Exponential backoff on 429/5xx errors
- **Idempotency** — Built-in idempotency key support
- **Webhook verification** — Verify incoming webhooks (Standard Webhooks compliant)
- **Error handling** — Typed exceptions
- **27+ Resources** — Application, Endpoint, Webhook, Billing, Cortex, Teams, and more

## Usage

### Applications

```python
# Create
app = hs.application.create(name="My App", description="My application")

# List with auto-pagination
for app in hs.application.list():
    print(app["name"])

# Get
app = hs.application.get("app_123")

# Update
app = hs.application.update("app_123", name="New Name")

# Delete
hs.application.delete("app_123")
```

### Endpoints

```python
# Create
ep = hs.endpoint.create(
    url="https://app.com/webhook",
    application_id="app_123",
    description="Order notifications",
)

# List with auto-pagination
for ep in hs.endpoint.list():
    print(ep["url"])

# Get
ep = hs.endpoint.get("ep_123")

# Update
ep = hs.endpoint.update("ep_123", url="https://new-url.com/webhook")

# Delete
hs.endpoint.delete("ep_123")

# Rotate signing secret
secret = hs.endpoint.rotate_secret("ep_123")
print(secret["signing_secret"])  # "whsec_..."
```

### Webhooks

```python
# Send a webhook
delivery = hs.webhook.send(
    endpoint_id="ep_123",
    event="order.created",
    data={"order_id": "12345", "amount": 99.99},
)

# Send with idempotency key
delivery = hs.webhook.send(
    endpoint_id="ep_123",
    event="order.created",
    data={},
    idempotency_key="unique-key-123",
)

# Send batch
result = hs.webhook.send_batch([
    {"endpoint_id": "ep_123", "event": "order.created", "data": {"id": "1"}},
    {"endpoint_id": "ep_123", "event": "order.created", "data": {"id": "2"}},
])

# List deliveries with auto-pagination
for d in hs.webhook.list(per_page=10):
    print(d["status"])

# Get delivery
delivery = hs.webhook.get("msg_123")

# Replay delivery
delivery = hs.webhook.replay("msg_123")
```

### Webhook Verification

```python
from hooksniff import Webhook, WebhookVerificationError

wh = Webhook("whsec_...")

# In your Flask/FastAPI handler:
def handle_webhook(request):
    try:
        event = wh.verify(request.body, request.headers)
        print(event)
        return "OK", 200
    except WebhookVerificationError:
        return "Invalid signature", 401
```

### Error Handling

```python
from hooksniff import AuthenticationError, NotFoundError, RateLimitError

try:
    hs.endpoint.get("invalid_id")
except NotFoundError:
    print("Endpoint not found")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

### All Resources

```python
# API Keys
hs.api_key.list()
hs.api_key.create(name="Production Key")
hs.api_key.delete("key_123")

# Analytics
hs.analytics.deliveries(range="24h")
hs.analytics.success_rate(range="7d")

# Billing
hs.billing.subscription()
hs.billing.upgrade(plan="pro")
hs.billing.portal()

# Teams
hs.team.list()
hs.team.create(name="Engineering")

# Cortex AI
hs.cortex.insights()
hs.cortex.anomalies(endpoint_id="ep_123")
hs.cortex.predict("ep_123")
hs.cortex.auto_heal("ep_123")

# Notifications
hs.notification.list()
hs.notification.get_unread_count()
hs.notification.mark_read("notif_123")
hs.notification.mark_all_read()

# Templates
hs.template.list()
hs.template.get("tmpl_123")

# Schemas
hs.schema.list()
hs.schema.create(name="Order Schema", schema={...})
hs.schema.validate("schema_123", {"order_id": "123"})

# Alerts
hs.alert.list()
hs.alert.create(name="...", condition="failure_rate", threshold=10, channels=["email"])

# Connectors
hs.connector.list()
hs.connector.list_configs()

# Stream
hs.stream.list_channels()
hs.stream.publish(channel_id="ch_123", event="test", data={...})

# Background Tasks
hs.background_task.list()
hs.background_task.get("task_123")

# Integrations
hs.integration.list()

# Service Tokens
hs.service_token.list()

# Operational Webhooks
hs.operational_webhook.list()

# Search
hs.search.deliveries("order.created")

# Health
hs.health.check()
hs.health.outbound_ips()

# User
hs.me()
```

## Configuration

```python
hs = HookSniff(
    "hr_live_...",
    base_url="https://your-instance.com",  # Custom API URL
    timeout=30,                             # Request timeout (seconds)
    retries=3,                              # Max retries on 5xx/429
    headers={"X-Custom": "value"},          # Custom headers
)
```

## Requirements

- Python 3.8+

## License

MIT — see [LICENSE](LICENSE) for details.
