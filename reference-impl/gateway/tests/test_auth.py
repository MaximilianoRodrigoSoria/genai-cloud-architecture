from __future__ import annotations

from gateway.auth import resolve_tenant


def test_key_valida():
    assert resolve_tenant("key-acme") == "acme"


def test_key_invalida():
    assert resolve_tenant("no-existe") is None
    assert resolve_tenant(None) is None
