"""Minimal Vault AppRole client with HTTPS and no secrets in logs."""
from __future__ import annotations
from .config import required_env


def fetch_vault_secrets(*, mount: str = "secret", path: str) -> dict:
    """Fetch KV v2 secrets from VAULT_ADDR via AppRole environment settings."""
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("Install requests for Vault support") from exc
    addr = required_env("VAULT_ADDR").rstrip("/")
    if not addr.startswith("https://"):
        raise ValueError("VAULT_ADDR must use HTTPS")
    role_id = required_env("VAULT_ROLE_ID")
    secret_id = required_env("VAULT_SECRET_ID")
    response = requests.post(f"{addr}/v1/auth/approle/login",
                             json={"role_id": role_id, "secret_id": secret_id}, timeout=20)
    response.raise_for_status()
    token = response.json()["auth"]["client_token"]
    secret_response = requests.get(f"{addr}/v1/{mount}/data/{path.lstrip('/')}",
                                   headers={"X-Vault-Token": token}, timeout=20)
    secret_response.raise_for_status()
    return secret_response.json()["data"]["data"]
