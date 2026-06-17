"""
HookSniff Python SDK - Live User Test
Run: HOOKSNIFF_API_KEY=*** python test_live.py
"""

import os
import sys
sys.path.insert(0, ".")

from hooksniff import HookSniff, Webhook, WebhookVerificationError, AuthenticationError, NotFoundError

API_KEY = os.environ.get("HOOKSNIFF_API_KEY")
if not API_KEY:
    print("Set HOOKSNIFF_API_KEY")
    sys.exit(1)

hs = HookSniff(API_KEY)
passed = 0
failed = 0

def t(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  ✅ {name}")
        passed += 1
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        failed += 1

print("🪝 HookSniff Python SDK - Live User Test\n")

# 1. Login
print("1. LOGIN")
def test_me():
    user = hs.me()
    assert "id" in user, "No id"
    print(f"     → {user['email']} ({user['plan']})")
t("Who am I?", test_me)

# 2. Create app
print("\n2. CREATE APP")
app_id = None
def test_create_app():
    global app_id
    app = hs.application.create(name=f"Python Test {os.getpid()}")
    assert "id" in app, "No id"
    app_id = app["id"]
    print(f"     → {app_id}")
t("Create application", test_create_app)

# 3. Create endpoint
print("\n3. CREATE ENDPOINT")
ep_id = None
def test_create_endpoint():
    global ep_id
    ep = hs.endpoint.create(url="https://httpbin.org/post", application_id=app_id, description="Test")
    assert "id" in ep, "No id"
    ep_id = ep["id"]
    print(f"     → {ep_id}")
t("Create endpoint", test_create_endpoint)

# 4. Get secret
print("\n4. GET SIGNING SECRET")
secret_value = None
def test_rotate_secret():
    global secret_value
    secret = hs.endpoint.rotate_secret(ep_id)
    assert "signing_secret" in secret, "No secret"
    secret_value = secret["signing_secret"]
    print(f"     → {secret_value[:25]}...")
t("Rotate secret", test_rotate_secret)

# 5. Send webhook
print("\n5. SEND WEBHOOK")
delivery_id = None
def test_send():
    global delivery_id
    d = hs.webhook.send(endpoint_id=ep_id, event="order.created", data={"order_id": "123", "amount": 99.99})
    assert "id" in d, "No id"
    delivery_id = d["id"]
    print(f"     → {d['id']} ({d['status']})")
t("Send webhook", test_send)

# 6. Idempotency
print("\n6. IDEMPOTENCY")
def test_idempotency():
    d = hs.webhook.send(endpoint_id=ep_id, event="test", data={"x": 1}, idempotency_key=f"idem-{os.getpid()}")
    assert "id" in d, "No id"
    print(f"     → {d['id']}")
t("Send with idempotency", test_idempotency)

# 7. List deliveries
print("\n7. LIST DELIVERIES")
def test_list_deliveries():
    deliveries = hs.webhook.list(per_page=5).all()
    assert isinstance(deliveries, list), "Not list"
    print(f"     → {len(deliveries)} deliveries")
t("List deliveries", test_list_deliveries)

# 8. Get delivery
print("\n8. GET DELIVERY")
def test_get_delivery():
    d = hs.webhook.get(delivery_id)
    assert d["id"] == delivery_id, "ID mismatch"
    print(f"     → {d['id']} | {d['status']}")
t("Get delivery", test_get_delivery)

# 9. Replay
print("\n9. REPLAY")
def test_replay():
    d = hs.webhook.replay(delivery_id)
    assert "id" in d, "No id"
    print(f"     → {d['id']}")
t("Replay", test_replay)

# 10. List apps
print("\n10. LIST APPS")
def test_list_apps():
    apps = hs.application.list().all()
    assert isinstance(apps, list), "Not list"
    print(f"     → {len(apps)} apps")
t("List apps", test_list_apps)

# 11. List endpoints
print("\n11. LIST ENDPOINTS")
def test_list_endpoints():
    eps = hs.endpoint.list().all()
    assert isinstance(eps, list), "Not list"
    print(f"     → {len(eps)} endpoints")
t("List endpoints", test_list_endpoints)

# 12. API Keys
print("\n12. API KEYS")
def test_api_keys():
    keys = hs.api_key.list()
    assert isinstance(keys, list), "Not list"
    print(f"     → {len(keys)} keys")
t("List keys", test_api_keys)

def test_create_key():
    k = hs.api_key.create(name="Python Test Key")
    assert "key" in k, "No key"
    print(f"     → {k['key'][:25]}...")
t("Create key", test_create_key)

# 13. Search
print("\n13. SEARCH")
def test_search():
    r = hs.search.deliveries("order")
    assert "deliveries" in r, "No deliveries"
    print(f"     → {len(r['deliveries'])} results")
t("Search", test_search)

# 14. Analytics
print("\n14. ANALYTICS")
def test_analytics():
    hs.analytics.deliveries(range="24h")
t("Analytics", test_analytics)

# 15. Billing
print("\n15. BILLING")
def test_billing():
    sub = hs.billing.subscription()
    assert "plan" in sub, "No plan"
    print(f"     → {sub['plan']} | {sub['status']}")
t("Subscription", test_billing)

# 16. Health
print("\n16. HEALTH")
def test_health():
    h = hs.health.check()
    assert h["status"] == "healthy", f"Status: {h['status']}"
    print(f"     → {h['status']} (DB: {h['database']['latency_ms']}ms)")
t("Health check", test_health)

def test_outbound_ips():
    r = hs.health.outbound_ips()
    assert "ips" in r, "No ips"
    print(f"     → {len(r['ips'])} IPs")
t("Outbound IPs", test_outbound_ips)

# 17. Cortex
print("\n17. CORTEX")
def test_cortex():
    insights = hs.cortex.insights()
    assert isinstance(insights, list), "Not list"
    print(f"     → {len(insights)} insights")
t("Insights", test_cortex)

# 18. Notifications
print("\n18. NOTIFICATIONS")
def test_notifications():
    r = hs.notification.list()
    assert "notifications" in r, "No notifications"
    print(f"     → {len(r['notifications'])} notifications")
t("List notifications", test_notifications)

def test_unread():
    r = hs.notification.get_unread_count()
    assert "count" in r, "No count"
    print(f"     → {r['count']} unread")
t("Unread count", test_unread)

# 19. Templates
print("\n19. TEMPLATES")
def test_templates():
    t_list = hs.template.list()
    assert isinstance(t_list, list), "Not list"
    print(f"     → {len(t_list)} templates")
t("List templates", test_templates)

# 20. Schemas
print("\n20. SCHEMAS")
def test_schemas():
    s_list = hs.schema.list()
    assert isinstance(s_list, list), "Not list"
    print(f"     → {len(s_list)} schemas")
t("List schemas", test_schemas)

# 21. Alerts
print("\n21. ALERTS")
def test_alerts():
    a_list = hs.alert.list()
    assert isinstance(a_list, list), "Not list"
    print(f"     → {len(a_list)} alerts")
t("List alerts", test_alerts)

# 22. Teams
print("\n22. TEAMS")
def test_teams():
    t_list = hs.team.list()
    assert isinstance(t_list, list), "Not list"
    print(f"     → {len(t_list)} teams")
t("List teams", test_teams)

# 23. Connectors
print("\n23. CONNECTORS")
def test_connectors():
    c_list = hs.connector.list()
    assert isinstance(c_list, list), "Not list"
    print(f"     → {len(c_list)} connectors")
t("List connectors", test_connectors)

def test_connector_configs():
    c_list = hs.connector.list_configs()
    assert isinstance(c_list, list), "Not list"
    print(f"     → {len(c_list)} configs")
t("List configs", test_connector_configs)

# 24. Stream
print("\n24. STREAM")
def test_stream():
    ch_list = hs.stream.list_channels()
    assert isinstance(ch_list, list), "Not list"
    print(f"     → {len(ch_list)} channels")
t("List channels", test_stream)

# 25. Background Tasks
print("\n25. BACKGROUND TASKS")
def test_bg_tasks():
    t_list = hs.background_task.list()
    assert isinstance(t_list, list), "Not list"
    print(f"     → {len(t_list)} tasks")
t("List tasks", test_bg_tasks)

# 26. Integrations
print("\n26. INTEGRATIONS")
def test_integrations():
    i_list = hs.integration.list()
    assert isinstance(i_list, list), "Not list"
    print(f"     → {len(i_list)} integrations")
t("List integrations", test_integrations)

# 27. Service Tokens
print("\n27. SERVICE TOKENS")
def test_service_tokens():
    t_list = hs.service_token.list()
    assert isinstance(t_list, list), "Not list"
    print(f"     → {len(t_list)} tokens")
t("List tokens", test_service_tokens)

# 28. Operational Webhooks
print("\n28. OPERATIONAL WEBHOOKS")
def test_op_webhooks():
    w_list = hs.operational_webhook.list()
    assert isinstance(w_list, list), "Not list"
    print(f"     → {len(w_list)} webhooks")
t("List op webhooks", test_op_webhooks)

# 29. Rate Limits
print("\n29. RATE LIMITS")
def test_rate_limits():
    r_list = hs.rate_limit.list()
    assert isinstance(r_list, list), "Not list"
    print(f"     → {len(r_list)} limits")
t("List limits", test_rate_limits)

# 30. Audit
print("\n30. AUDIT")
def test_audit():
    r = hs.audit.list()
    assert r is not None, "No data"
t("List audit", test_audit)

# 31. Webhook Verification
print("\n31. WEBHOOK VERIFICATION")
def test_verify():
    wh = Webhook("whsec_test")
    try:
        wh.verify("{}", {})
        assert False, "Should fail"
    except WebhookVerificationError:
        pass
t("Reject invalid signature", test_verify)

# 32. Error Handling
print("\n32. ERROR HANDLING")
def test_auth_error():
    bad = HookSniff("bad", retries=0)
    try:
        bad.me()
        assert False, "Should fail"
    except AuthenticationError:
        pass
t("AuthenticationError", test_auth_error)

def test_not_found():
    try:
        hs.endpoint.get("00000000-0000-0000-0000-000000000000")
        assert False, "Should fail"
    except NotFoundError:
        pass
t("NotFoundError", test_not_found)

# Cleanup
print("\n🧹 CLEANUP")
def test_cleanup_ep():
    hs.endpoint.delete(ep_id)
t("Delete endpoint", test_cleanup_ep)

def test_cleanup_app():
    hs.application.delete(app_id)
t("Delete app", test_cleanup_app)

# Summary
print(f"\n{'=' * 50}")
print(f"{passed} PASSED, {failed} FAILED")
print(f"{'=' * 50}")

if failed > 0:
    sys.exit(1)
