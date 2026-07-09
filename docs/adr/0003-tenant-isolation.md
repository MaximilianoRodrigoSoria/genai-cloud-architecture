# ADR 0003 — Aislamiento y cuotas por tenant

- Estado: aceptada
- Fecha: 2026-07-09

## Contexto

La plataforma sirve a múltiples clientes sobre infraestructura compartida. Hay que
aislar datos, tráfico y costos, y evitar que un tenant afecte a otro (ruido,
abuso, fuga de datos), balanceando costo vs aislamiento.

## Decisión

- **Modelo:** **pool** por defecto (aislamiento lógico por `tenant_id`), con
  opción de **silo** (recursos dedicados) para tenants premium/regulados.
- **Datos:** namespace por tenant en el vector store; partition key `tenant_id` en
  DynamoDB (con IAM `LeadingKeys`); prefijo por tenant en S3.
- **Tráfico:** rate limiting por tenant (token bucket) + cuotas de tokens/costo por
  tier. Exceso → `429` o degradación a modelo barato.
- **Costo:** atribución por `tenant_id` para facturar por uso y detectar abuso.

## Alternativas evaluadas

- **Silo para todos:** máximo aislamiento pero costo y ops que no escalan a muchos
  tenants chicos. Rechazada como default; disponible como tier premium.
- **Pool sin límites por tenant:** rechazada — un tenant ruidoso degrada a todos y
  el gasto se vuelve impredecible.
- **Aislamiento solo a nivel app (sin IAM):** rechazada — un bug de aplicación
  podría cruzar tenants; se refuerza con políticas IAM por `LeadingKeys`.

## Consecuencias

- (+) Costo eficiente y escalable para el grueso de tenants.
- (+) Blast radius acotado por límites y particionado; defensa en profundidad (app + IAM).
- (−) El pool tiene mayor blast radius que el silo; se ofrece silo donde el riesgo lo justifica.
- (−) Complejidad de cuotas y de la lógica de degradación; la `reference-impl/gateway/`
  implementa auth por tenant, rate limit y cuotas por tier.
