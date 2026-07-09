"""Tests de autenticación por tenant."""

from __future__ import annotations

from gateway.auth import authenticate


def test_api_key_valida_devuelve_tenant():
    tenant = authenticate("key-pro-def")
    assert tenant is not None
    assert tenant.id == "t-pro" and tenant.tier == "pro"


def test_api_key_invalida_devuelve_none():
    assert authenticate("no-existe") is None


def test_api_key_ausente_devuelve_none():
    assert authenticate(None) is None
    assert authenticate("") is None
