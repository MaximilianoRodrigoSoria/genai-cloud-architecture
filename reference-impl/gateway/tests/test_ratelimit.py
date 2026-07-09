"""Tests del token bucket (reloj inyectado, sin sleep)."""

from __future__ import annotations

from gateway.ratelimit import TokenBucket


def test_permite_la_rafaga_y_luego_bloquea():
    now = [0.0]
    bucket = TokenBucket(rate=1.0, capacity=3, clock=lambda: now[0])
    assert bucket.allow() and bucket.allow() and bucket.allow()
    assert not bucket.allow()  # agotó la capacidad


def test_recarga_con_el_tiempo():
    now = [0.0]
    bucket = TokenBucket(rate=1.0, capacity=3, clock=lambda: now[0])
    for _ in range(3):
        bucket.allow()
    assert not bucket.allow()
    now[0] = 1.0  # pasó 1s → +1 token a rate=1/s
    assert bucket.allow()
    assert not bucket.allow()
