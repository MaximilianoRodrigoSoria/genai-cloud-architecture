from __future__ import annotations

from gateway.cache import SemanticCache


def test_hit_y_normalizacion():
    c = SemanticCache(ttl_seconds=100)
    c.put("acme", "Hola  Mundo", "v", now=0)
    assert c.get("acme", "hola mundo", now=5) == "v"  # normaliza espacios/case


def test_expira_por_ttl():
    c = SemanticCache(ttl_seconds=10)
    c.put("acme", "x", "v", now=0)
    assert c.get("acme", "x", now=100) is None


def test_aisla_por_tenant():
    c = SemanticCache(ttl_seconds=100)
    c.put("acme", "x", "v", now=0)
    assert c.get("globex", "x", now=0) is None
