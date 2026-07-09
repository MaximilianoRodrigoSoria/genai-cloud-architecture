"""Tenants y tiers (registro demo en memoria).

En producción, los tenants viven en una tabla (DynamoDB) y la identidad la
resuelve Cognito; acá se hardcodea un registro chico para la demo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    name: str
    rate_per_sec: float          # tokens de rate limit por segundo
    burst: int                   # capacidad del bucket (ráfaga)
    daily_token_quota: int       # cuota de tokens por día
    force_model: str | None = None  # override de ruteo: "cheap" | "expensive" | None


TIERS: dict[str, Tier] = {
    "free": Tier("free", rate_per_sec=1.0, burst=3, daily_token_quota=50_000, force_model="cheap"),
    "pro": Tier("pro", rate_per_sec=10.0, burst=20, daily_token_quota=2_000_000),
    "enterprise": Tier("enterprise", rate_per_sec=50.0, burst=100, daily_token_quota=50_000_000),
}


@dataclass(frozen=True)
class Tenant:
    id: str
    name: str
    tier: str
    api_key: str


# api_key -> Tenant
TENANTS: dict[str, Tenant] = {
    "key-free-abc": Tenant("t-free", "Acme Free", "free", "key-free-abc"),
    "key-pro-def": Tenant("t-pro", "Globex Pro", "pro", "key-pro-def"),
    "key-ent-ghi": Tenant("t-ent", "Initech Enterprise", "enterprise", "key-ent-ghi"),
}
