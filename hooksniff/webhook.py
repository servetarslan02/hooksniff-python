import json
import time
import hmac
import hashlib
import base64
from typing import Any, Dict, Union


class WebhookVerificationError(Exception):
    """Webhook verification failed."""
    pass


class Webhook:
    """
    Verify and parse incoming webhook payloads.
    Compliant with the Standard Webhooks specification.

    Usage:
        wh = Webhook("whsec_...")
        event = wh.verify(request.body, request.headers)
    """

    def __init__(self, secret: str):
        if not secret:
            raise ValueError("Webhook secret is required")
        self.secret = secret

    def verify(self, payload: Union[str, bytes], headers: Dict[str, str]) -> Any:
        normalized_headers = {k.lower(): v for k, v in headers.items()}

        msg_id = normalized_headers.get("webhook-id")
        msg_signature = normalized_headers.get("webhook-signature")
        msg_timestamp = normalized_headers.get("webhook-timestamp")

        if not msg_id or not msg_signature or not msg_timestamp:
            raise WebhookVerificationError(
                "Missing required webhook headers (webhook-id, webhook-signature, webhook-timestamp)"
            )

        try:
            timestamp = int(msg_timestamp)
        except ValueError:
            raise WebhookVerificationError("Invalid webhook timestamp")

        now = int(time.time())
        if abs(now - timestamp) > 300:
            raise WebhookVerificationError("Webhook timestamp is too old")

        content = payload if isinstance(payload, str) else payload.decode("utf-8")
        to_sign = f"{msg_id}.{msg_timestamp}.{content}"
        expected_signature = self._sign(to_sign)

        signatures = msg_signature.split(" ")
        is_valid = False
        for sig in signatures:
            parts = sig.split(",", 1)
            if len(parts) != 2:
                continue
            version, signature = parts
            if version != "v1":
                continue

            try:
                if hmac.compare_digest(signature, expected_signature):
                    is_valid = True
                    break
            except Exception:
                continue

        if not is_valid:
            raise WebhookVerificationError("Invalid webhook signature")

        return json.loads(content)

    def _sign(self, content: str) -> str:
        secret_bytes = self.secret.replace("whsec_", "").encode("utf-8")
        try:
            secret_key = base64.b64decode(secret_bytes)
        except Exception:
            secret_key = secret_bytes
        
        return base64.b64encode(
            hmac.HMAC(secret_key, content.encode("utf-8"), hashlib.sha256).digest()
        ).decode("utf-8")
