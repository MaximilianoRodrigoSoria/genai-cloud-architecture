"""Cache 'semántico' (demo).

ponytail: acá el hit es por texto normalizado (exacto). El upgrade a semántico
real es reemplazar la clave por el embedding del prompt y buscar por similitud
coseno sobre un umbral. La interfaz no cambia.
"""

from __future__ import annotations

import time


class SemanticCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self._store: dict[tuple[str, str], tuple[float, str]] = {}

    @staticmethod
    def _key(tenant: str, prompt: str) -> tuple[str, str]:
        return (tenant, " ".join(prompt.lower().split()))

    def get(self, tenant: str, prompt: str, now: float | None = None) -> str | None:
        now = now if now is not None else time.time()
        item = self._store.get(self._key(tenant, prompt))
        if not item:
            return None
        ts, value = item
        if now - ts > self.ttl:
            return None
        return value

    def put(self, tenant: str, prompt: str, value: str, now: float | None = None) -> None:
        now = now if now is not None else time.time()
        self._store[self._key(tenant, prompt)] = (now, value)
