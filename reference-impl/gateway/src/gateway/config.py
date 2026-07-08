"""Config del gateway: mapeo API key → tenant y límites por tenant."""

from __future__ import annotations

# Demo: en producción esto vive en un store seguro (Secrets Manager / DB).
API_KEYS: dict[str, str] = {
    "key-acme": "acme",
    "key-globex": "globex",
}

# Requests permitidos por ventana, por tenant.
RATE_LIMIT_PER_MINUTE = 5

# TTL del cache semántico (segundos).
CACHE_TTL_SECONDS = 300
