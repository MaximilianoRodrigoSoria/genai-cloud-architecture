"""Tests del cache semántico (stub por similitud léxica)."""

from __future__ import annotations

from gateway.cache import SemanticCache, similarity


def test_similitud_exacta_y_disjunta():
    assert similarity("hola mundo", "hola mundo") == 1.0
    assert similarity("hola mundo", "chau luna") == 0.0


def test_hit_en_prompt_igual():
    cache = SemanticCache(threshold=0.8)
    cache.put("t1", "cual es la garantia", "12 meses")
    assert cache.get("t1", "cual es la garantia") == "12 meses"


def test_miss_en_prompt_distinto():
    cache = SemanticCache(threshold=0.8)
    cache.put("t1", "cual es la garantia", "12 meses")
    assert cache.get("t1", "como cancelo mi cuenta") is None


def test_aislado_por_tenant():
    cache = SemanticCache(threshold=0.8)
    cache.put("t1", "hola", "respuesta de t1")
    assert cache.get("t2", "hola") is None
