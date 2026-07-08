from __future__ import annotations

from gateway.ratelimit import RateLimiter


def test_corta_al_exceder():
    rl = RateLimiter(limit_per_minute=3)
    assert all(rl.allow("acme", now=1000.0 + i) for i in range(3))
    assert rl.allow("acme", now=1003.0) is False


def test_aisla_por_tenant():
    rl = RateLimiter(limit_per_minute=1)
    assert rl.allow("acme", now=0)
    assert rl.allow("globex", now=0)   # otro tenant no se ve afectado
    assert rl.allow("acme", now=1) is False
