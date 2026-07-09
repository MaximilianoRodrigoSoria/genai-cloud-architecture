"""Autenticación por tenant: resuelve una API key a su Tenant."""

from __future__ import annotations

from .config import TENANTS, Tenant


def authenticate(api_key: str | None) -> Tenant | None:
    """Devuelve el Tenant de la API key, o None si es inválida/ausente."""
    if not api_key:
        return None
    return TENANTS.get(api_key)
