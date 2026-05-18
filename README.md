# HookSniff Python SDK

<p align="center">
  <a href="https://pypi.org/project/hooksniff/"><img src="https://img.shields.io/pypi/v/hooksniff.svg" alt="PyPI"></a>
  <a href="https://github.com/servetarslan02/hooksniff-python"><img src="https://img.shields.io/github/license/servetarslan02/hooksniff-python" alt="License"></a>
</p>

Python SDK for the [HookSniff](https://hooksniff.vercel.app) webhook delivery platform.

## Installation

```bash
pip install hooksniff
```

## Quick Start

```python
from hooksniff import HookSniff

# API anahtarınızı https://hooksniff.vercel.app adresinden alın
hs = HookSniff("hooksniff_xxx")

# Endpoint'leri listele
endpoints = hs.endpoint.list()

# Yeni endpoint oluştur
endpoint = hs.endpoint.create(
    EndpointIn(url="https://example.com/webhook", description="My endpoint")
)

# Webhook gönder
delivery = hs.message.create(
    endpoint_id="ep_xxx",
    event="order.created",
    data={"order_id": "123", "amount": 99.99}
)

# Teslimat denemelerini gör
attempts = hs.message_attempt.list_by_delivery(delivery.id)
```

## Authentication

```python
from hooksniff.api.authentication import Authentication

auth = hs.authentication

# Giriş yap
result = auth.login("user@example.com", "password123")
token = result["token"]

# Kayıt ol
result = auth.register("user@example.com", "password123", name="Servet")

# Profilimi gör
me = auth.get_me()

# 2FA etkinleştir
qr = auth.enable_2fa("password123")
```

## Endpoints

```python
from hooksniff.models import EndpointIn, EndpointUpdate, EndpointPatch

# Listele
endpoints = hs.endpoint.list()

# Oluştur
ep = hs.endpoint.create(EndpointIn(
    url="https://example.com/webhook",
    description="Order notifications",
    event_filter=["order.*"],
    routing_strategy="round-robin"
))

# Güncelle
ep = hs.endpoint.update(ep.id, EndpointUpdate(
    url="https://new-url.com/webhook",
    description="Updated endpoint"
))

# Kısmi güncelleme
ep = hs.endpoint.patch(ep.id, EndpointPatch(description="Patched"))

# Sil
hs.endpoint.delete(ep.id)

# Secret rotate
hs.endpoint.rotate_secret(ep.id)
```

## Webhooks

```python
from hooksniff.models import MessageIn

# Tek webhook gönder
delivery = hs.message.create(
    endpoint_id="ep_xxx",
    event="order.created",
    data={"order_id": "123"}
)

# Toplu gönder
result = hs.message.batch([
    {"endpoint_id": "ep_xxx", "event": "order.created", "data": {"order_id": "1"}},
    {"endpoint_id": "ep_xxx", "event": "order.shipped", "data": {"order_id": "2"}},
])

# Teslimat listesi
deliveries = hs.message.list()

# Tekrar gönder
hs.message.replay("del_xxx")
```

## Other Resources

```python
# Background tasks
tasks = hs.background_task.list()
task = hs.background_task.get("task_xxx")

# Environments
envs = hs.environment.list()
env = hs.environment.create(EnvironmentIn(name="production"))

# Connectors
connectors = hs.connector.list()

# Integrations
integrations = hs.integration.list()

# Streaming
channels = hs.stream.list_channels()

# Statistics
stats = hs.statistics.get_account_stats()
```

## Webhook Verification

```python
from hooksniff import Webhook

wh = Webhook("whsec_xxx")

# Gelen webhook'u doğrula
try:
    payload = wh.verify(raw_body, headers)
    print("Valid webhook:", payload)
except Exception:
    print("Invalid signature!")
```

## Async Support

```python
from hooksniff import HookSniffAsync

hs = HookSniffAsync("hooksniff_xxx")
endpoints = await hs.endpoint.list()
```

## Error Handling

```python
from hooksniff import (
    HookSniffError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
)

try:
    hs.endpoint.get("nonexistent")
except NotFoundError:
    print("Endpoint bulunamadı")
except RateLimitError as e:
    print(f"Rate limit aşıldı, {e.retry_after}s bekle")
except UnauthorizedError:
    print("Geçersiz API anahtarı")
except HookSniffError as e:
    print(f"Hata: {e.status_code} - {e}")
```

## Links

- [Dashboard](https://hooksniff.vercel.app)
- [Documentation](https://hooksniff.vercel.app/docs)
- [API Reference](https://hooksniff.vercel.app/docs)
- [GitHub](https://github.com/servetarslan02/hooksniff-python)
- [PyPI](https://pypi.org/project/hooksniff/)

## License

MIT
