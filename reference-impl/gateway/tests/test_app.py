"""Tests del gateway completo con FastAPI TestClient (offline)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from gateway.app import create_app
from gateway.ratelimit import RateLimiter

PRO = {"Authorization": "Bearer key-pro-def"}
FREE = {"Authorization": "Bearer key-free-abc"}


def test_sin_auth_devuelve_401():
    client = TestClient(create_app())
    assert client.post("/v1/chat", json={"prompt": "hola"}).status_code == 401


def test_request_ok_devuelve_tenant_y_modelo():
    client = TestClient(create_app())
    r = client.post("/v1/chat", json={"prompt": "hola"}, headers=PRO)
    assert r.status_code == 200
    body = r.json()
    assert body["tenant"] == "t-pro"
    assert body["cached"] is False
    assert "answer" in body and body["model"] in ("claude-haiku-4-5", "claude-sonnet-5")


def test_cache_hit_en_repeticion():
    client = TestClient(create_app())
    client.post("/v1/chat", json={"prompt": "misma pregunta exacta"}, headers=PRO)
    r2 = client.post("/v1/chat", json={"prompt": "misma pregunta exacta"}, headers=PRO)
    assert r2.json()["cached"] is True


def test_free_tier_fuerza_modelo_barato():
    client = TestClient(create_app())
    r = client.post(
        "/v1/chat",
        json={"prompt": "analiza y compara paso a paso"},  # sería caro por heurística
        headers=FREE,
    )
    assert r.json()["model"] == "claude-haiku-4-5"  # el tier free lo fuerza a barato


def test_rate_limit_devuelve_429():
    now = [0.0]
    client = TestClient(create_app(rate_limiter=RateLimiter(clock=lambda: now[0])))
    codes = [
        client.post("/v1/chat", json={"prompt": f"pregunta {i}"}, headers=FREE).status_code
        for i in range(5)  # free tier: burst=3
    ]
    assert codes.count(200) == 3
    assert 429 in codes
