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
