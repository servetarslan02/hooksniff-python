# Adapted for HookSniff API
# HookSniff auth endpoints are at /v1/auth/...
import typing as t
from dataclasses import dataclass

from .common import ApiBase, BaseOptions, serialize_params


class AuthenticationAsync(ApiBase):
    async def login(self, email: str, password: str) -> dict:
        """Login with email and password. Returns JWT token."""
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/auth/login",
            json_body=json.dumps({"email": email, "password": password}),
        )
        return response.json()

    async def register(self, email: str, password: str, name: t.Optional[str] = None) -> dict:
        """Register a new account."""
        import json
        body: dict = {"email": email, "password": password}
        if name:
            body["name"] = name
        response = await self._request_asyncio(
            method="post",
            path="/v1/auth/register",
            json_body=json.dumps(body),
        )
        return response.json()

    async def logout(self, refresh_token: t.Optional[str] = None) -> None:
        """Logout (invalidate refresh token)."""
        import json
        body = {}
        if refresh_token:
            body["refresh_token"] = refresh_token
        await self._request_asyncio(
            method="post",
            path="/v1/auth/logout",
            json_body=json.dumps(body) if body else None,
        )

    async def get_me(self) -> dict:
        """Get current user profile."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/auth/me",
        )
        return response.json()

    async def update_profile(self, name: str, email: str) -> dict:
        """Update profile."""
        import json
        response = await self._request_asyncio(
            method="put",
            path="/v1/auth/profile",
            json_body=json.dumps({"name": name, "email": email}),
        )
        return response.json()

    async def change_password(self, current_password: str, new_password: str) -> None:
        """Change password."""
        import json
        await self._request_asyncio(
            method="put",
            path="/v1/auth/password",
            json_body=json.dumps({
                "current_password": current_password,
                "new_password": new_password,
            }),
        )

    async def forgot_password(self, email: str) -> None:
        """Request password reset email."""
        import json
        await self._request_asyncio(
            method="post",
            path="/v1/auth/forgot-password",
            json_body=json.dumps({"email": email}),
        )

    async def reset_password(self, token: str, new_password: str) -> None:
        """Reset password with token."""
        import json
        await self._request_asyncio(
            method="post",
            path="/v1/auth/reset-password",
            json_body=json.dumps({"token": token, "new_password": new_password}),
        )

    async def verify_email(self, token: str) -> None:
        """Verify email address."""
        import json
        await self._request_asyncio(
            method="post",
            path="/v1/auth/verify-email",
            json_body=json.dumps({"token": token}),
        )

    async def refresh(self, refresh_token: str) -> dict:
        """Refresh access token."""
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/auth/refresh",
            json_body=json.dumps({"refresh_token": refresh_token}),
        )
        return response.json()

    async def enable_2fa(self, password: str) -> dict:
        """Enable 2FA (returns TOTP secret and QR URL)."""
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/auth/2fa/enable",
            json_body=json.dumps({"password": password}),
        )
        return response.json()

    async def confirm_2fa(self, code: str) -> None:
        """Confirm 2FA setup with a code."""
        import json
        await self._request_asyncio(
            method="post",
            path="/v1/auth/2fa/confirm",
            json_body=json.dumps({"code": code}),
        )

    async def verify_2fa(self, temp_token: str, code: str) -> dict:
        """Verify 2FA code during login."""
        import json
        response = await self._request_asyncio(
            method="post",
            path="/v1/auth/2fa/verify",
            json_body=json.dumps({"temp_token": temp_token, "code": code}),
        )
        return response.json()

    async def disable_2fa(self, password: str) -> None:
        """Disable 2FA."""
        import json
        await self._request_asyncio(
            method="post",
            path="/v1/auth/2fa/disable",
            json_body=json.dumps({"password": password}),
        )

    async def export_data(self) -> dict:
        """Export user data (GDPR)."""
        response = await self._request_asyncio(
            method="get",
            path="/v1/auth/export",
        )
        return response.json()

    async def delete_account(self) -> None:
        """Delete account (GDPR)."""
        await self._request_asyncio(
            method="delete",
            path="/v1/auth/account",
        )


class Authentication(ApiBase):
    def login(self, email: str, password: str) -> dict:
        """Login with email and password. Returns JWT token."""
        import json
        response = self._request_sync(
            method="post",
            path="/v1/auth/login",
            json_body=json.dumps({"email": email, "password": password}),
        )
        return response.json()

    def register(self, email: str, password: str, name: t.Optional[str] = None) -> dict:
        """Register a new account."""
        import json
        body: dict = {"email": email, "password": password}
        if name:
            body["name"] = name
        response = self._request_sync(
            method="post",
            path="/v1/auth/register",
            json_body=json.dumps(body),
        )
        return response.json()

    def logout(self, refresh_token: t.Optional[str] = None) -> None:
        """Logout (invalidate refresh token)."""
        import json
        body = {}
        if refresh_token:
            body["refresh_token"] = refresh_token
        self._request_sync(
            method="post",
            path="/v1/auth/logout",
            json_body=json.dumps(body) if body else None,
        )

    def get_me(self) -> dict:
        """Get current user profile."""
        response = self._request_sync(
            method="get",
            path="/v1/auth/me",
        )
        return response.json()

    def update_profile(self, name: str, email: str) -> dict:
        """Update profile."""
        import json
        response = self._request_sync(
            method="put",
            path="/v1/auth/profile",
            json_body=json.dumps({"name": name, "email": email}),
        )
        return response.json()

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change password."""
        import json
        self._request_sync(
            method="put",
            path="/v1/auth/password",
            json_body=json.dumps({
                "current_password": current_password,
                "new_password": new_password,
            }),
        )

    def forgot_password(self, email: str) -> None:
        """Request password reset email."""
        import json
        self._request_sync(
            method="post",
            path="/v1/auth/forgot-password",
            json_body=json.dumps({"email": email}),
        )

    def reset_password(self, token: str, new_password: str) -> None:
        """Reset password with token."""
        import json
        self._request_sync(
            method="post",
            path="/v1/auth/reset-password",
            json_body=json.dumps({"token": token, "new_password": new_password}),
        )

    def verify_email(self, token: str) -> None:
        """Verify email address."""
        import json
        self._request_sync(
            method="post",
            path="/v1/auth/verify-email",
            json_body=json.dumps({"token": token}),
        )

    def refresh(self, refresh_token: str) -> dict:
        """Refresh access token."""
        import json
        response = self._request_sync(
            method="post",
            path="/v1/auth/refresh",
            json_body=json.dumps({"refresh_token": refresh_token}),
        )
        return response.json()

    def enable_2fa(self, password: str) -> dict:
        """Enable 2FA (returns TOTP secret and QR URL)."""
        import json
        response = self._request_sync(
            method="post",
            path="/v1/auth/2fa/enable",
            json_body=json.dumps({"password": password}),
        )
        return response.json()

    def confirm_2fa(self, code: str) -> None:
        """Confirm 2FA setup with a code."""
        import json
        self._request_sync(
            method="post",
            path="/v1/auth/2fa/confirm",
            json_body=json.dumps({"code": code}),
        )

    def verify_2fa(self, temp_token: str, code: str) -> dict:
        """Verify 2FA code during login."""
        import json
        response = self._request_sync(
            method="post",
            path="/v1/auth/2fa/verify",
            json_body=json.dumps({"temp_token": temp_token, "code": code}),
        )
        return response.json()

    def disable_2fa(self, password: str) -> None:
        """Disable 2FA."""
        import json
        self._request_sync(
            method="post",
            path="/v1/auth/2fa/disable",
            json_body=json.dumps({"password": password}),
        )

    def export_data(self) -> dict:
        """Export user data (GDPR)."""
        response = self._request_sync(
            method="get",
            path="/v1/auth/export",
        )
        return response.json()

    def delete_account(self) -> None:
        """Delete account (GDPR)."""
        self._request_sync(
            method="delete",
            path="/v1/auth/account",
        )
