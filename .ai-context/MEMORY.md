# hooksniff-python SDK — Hafıza

> Son güncelleme: 2026-05-18 23:01 GMT+8

## SDK Durumu
- Versiyon: **1.2.0** (PyPI'de yüklü)
- API yolları: ✅ HookSniff'e uyumlu (`/v1/...`)
- Model'ler: ✅ Gerçek API response'larıyla doğrulandı
- Test: ✅ Demo hesapla test edildi

## Yapılan Düzeltmeler (v1.2.0)
1. Tüm API yolları `/api/v1/app/{app_id}/...` → `/v1/...` olarak değiştirildi
2. `app_id` parametresi kaldırıldı (JWT auth)
3. 16 API modülü düzeltildi
4. 22 yeni model dosyası eklendi
5. Svix modelleri HookSniff modelleriyle değiştirildi
6. `application_id` field'ı EndpointOut'a eklendi

## Gerçek API Doğrulama (2026-05-18)
- Login: ✅ `/v1/auth/login` çalışıyor
- Endpoints: ✅ `/v1/endpoints` → `[{id, url, is_active, application_id, ...}]`
- Webhooks: ✅ `/v1/webhooks` → `{deliveries: [...], total, page, per_page}`
- Status: ✅ `/v1/status` → `{overall_status: "operational"}`

## Kurulum
```bash
pip install hooksniff==1.2.0
```

## Kullanım
```python
from hooksniff import HookSniff
hs = HookSniff("hooksniff_xxx")
endpoints = hs.endpoint.list()
hs.message.create("ep_xxx", "order.created", {"order_id": "1"})
```

## Gerçek API Test Sonuçları (2026-05-18 23:08)

### ✅ Çalışan (32/35)
| Modül | Endpoint | HTTP |
|-------|----------|------|
| auth.get_me | /v1/auth/me | 200 |
| auth.export | /v1/auth/export | 200 |
| endpoint.list | /v1/endpoints | 200 |
| endpoint.get | /v1/endpoints/{id} | 200 |
| endpoint.update | /v1/endpoints/{id} PUT | 200 |
| endpoint.rotate_secret | /v1/endpoints/{id}/rotate-secret | 200 |
| webhooks.list | /v1/webhooks | 200 |
| webhooks.get | /v1/webhooks/{id} | 200 |
| webhooks.attempts | /v1/webhooks/{id}/attempts | 200 |
| webhooks.replay | /v1/webhooks/{id}/replay | 200 |
| background_task.list | /v1/background-tasks | 200 |
| environment.list | /v1/environments | 200 |
| operational_webhook.list | /v1/operational-webhooks | 200 |
| message_poller.poll | /v1/message-poller/poll | 200 |
| connector.list | /v1/connectors | 200 |
| integration.list | /v1/integrations | 200 |
| stream.channels | /v1/stream/channels | 200 |
| stream.subscriptions | /v1/stream/subscriptions | 200 |
| event_type.list | /v1/events | 200 |
| statistics.get | /v1/stats | 200 |
| api_keys.list | /v1/api-keys | 200 |
| analytics.* | /v1/analytics/* | 200 |
| search | /v1/search | 200 |
| inbound.configs | /v1/inbound/configs | 200 |
| templates.list | /v1/templates | 200 |
| schemas.list | /v1/schemas | 200 |
| teams.list | /v1/teams | 200 |
| notifications.list | /v1/notifications | 200 |
| billing.* | /v1/billing/* | 200 |
| alerts.list | /v1/alerts | 200 |
| endpoint_health.list | /v1/endpoint-health | 200 |
| service_tokens.list | /v1/service-tasks | 200 |

### ⚠️ Düzeltilenler
- endpoint.create: `application_id` gerekiyor (API'de zorunlu, OpenAPI spec'te yok)
- endpoint.update: read-only field'lar (`failure_streak`, `avg_response_ms`) gönderilmez

### ❌ Sunucu Tarafı Sorun
- webhooks.create: HTTP 500 (DATABASE_ERROR) — SDK formatı doğru, sunucu hatası
