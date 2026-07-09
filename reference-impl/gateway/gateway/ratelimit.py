"""Rate limiting por tenant con token bucket.

El reloj es inyectable (`clock`) para poder testear el refill de forma
determinista sin `sleep`.
"""

from __future__ import annotations

import time
from typing import Callable


class TokenBucket:
    def __init__(self, rate: float, capacity: int, clock: Callable[[], float] = time.monotonic):
        self.rate = rate
        self.capacity = capacity
        self._clock = clock
        self._tokens = float(capacity)
        self._last = clock()

    def _refill(self) -> None:
        now = self._clock()
        elapsed = max(0.0, now - self._last)
        self._last = now
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)

    def allow(self, cost: float = 1.0) -> bool:
        self._refill()
        if self._tokens >= cost:
            self._tokens -= cost
            return True
        return False


class RateLimiter:
    """Un bucket por tenant, dimensionado por su tier."""

    def __init__(self, clock: Callable[[], float] = time.monotonic):
        self._clock = clock
        self._buckets: dict[str, TokenBucket] = {}

    def allow(self, tenant, tier) -> bool:
        bucket = self._buckets.get(tenant.id)
        if bucket is None:
            bucket = TokenBucket(tier.rate_per_sec, tier.burst, self._clock)
            self._buckets[tenant.id] = bucket
        return bucket.allow()
