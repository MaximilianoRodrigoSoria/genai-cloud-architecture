# ADR 0003 — Estrategia de aislamiento de tenants

## Estado
Aceptada.

## Contexto
Distintos tenants tienen distintos requisitos de aislamiento y compliance.

## Decisión
Modelo **híbrido**: pool con partición lógica por `tenant_id` por defecto; silo
(recursos dedicados) para tenants que lo requieran. Rate limiting, cuotas y
atribución de costo **por tenant** en el gateway.

## Consecuencias
- (+) Eficiencia de costo para la mayoría, aislamiento fuerte para quien lo necesite.
- (−) Dos caminos de despliegue a mantener (pool y silo).
