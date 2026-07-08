"""AuthN por tenant: resuelve el tenant a partir de la API key."""

from __future__ import annotations

from gateway.config import API_KEYS


def resolve_tenant(api_key: str | None) -> str | None:
    """Devuelve el tenant_id para una API key, o None si es inválida."""
    if not api_key:
        return None
    return API_KEYS.get(api_key)
