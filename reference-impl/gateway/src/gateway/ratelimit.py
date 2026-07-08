"""Rate limiting por tenant (ventana fija, en memoria).

ponytail: ventana fija en memoria; para producción, mover a Redis con token bucket
(sirve para varias instancias del gateway).
"""

from __future__ import annotations

import time


class RateLimiter:
    def __init__(self, limit_per_minute: int):
        self.limit = limit_per_minute
        self._hits: dict[str, list[float]] = {}

    def allow(self, tenant: str, now: float | None = None) -> bool:
        now = now if now is not None else time.time()
        window = [t for t in self._hits.get(tenant, []) if now - t < 60]
        if len(window) >= self.limit:
            self._hits[tenant] = window
            return False
        window.append(now)
        self._hits[tenant] = window
        return True
