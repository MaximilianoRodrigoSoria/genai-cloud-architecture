# Estrategia de multi-tenancy

Cómo la plataforma aísla datos, tráfico y costos entre tenants.

## Modelo de aislamiento: pool con opción de silo

Por defecto, **pool** (recursos compartidos, aislamiento lógico por `tenant_id`):
es el más eficiente en costo y el que mejor escala a muchos tenants chicos. Para
tenants premium o con requisitos regulatorios, se ofrece **silo** (recursos
dedicados: base, índice o hasta cuenta AWS separada).

| Dimensión | Pool (default) | Silo (premium) |
|---|---|---|
| Vector store | Un índice, `namespace = tenant_id` | Índice/colección dedicada |
| Datos | Tabla compartida, partition key `tenant_id` | Tabla/DB dedicada |
| Objetos | Bucket compartido, prefijo `s3://.../{tenant_id}/` | Bucket dedicado |
| Costo | Bajo, compartido | Alto, predecible/aislado |
| Blast radius | Mayor | Menor |

## Aislamiento de datos

- **Vector store (OpenSearch):** cada consulta filtra por `tenant_id` y usa el
  namespace del tenant; nunca se hace retrieval cross-tenant.
- **DynamoDB:** partition key `tenant_id`; las políticas IAM restringen por
  `dynamodb:LeadingKeys` para que ni un bug de aplicación cruce tenants.
- **S3:** prefijo por tenant + políticas de bucket con condición sobre el prefijo.

## Rate limiting y cuotas

Dos niveles, ambos por tenant:

- **Rate limit** (protege la plataforma): requests/segundo con token bucket. Al
  excederlo → `429`.
- **Cuota** (controla el gasto): tope de tokens/costo por período (día/mes). Al
  agotarla → `429` o degradación a un modelo más barato, según el tier.

Los límites se parametrizan por **tier** (free / pro / enterprise). La
`reference-impl/gateway/` implementa el rate limit por token bucket y las cuotas
por tier.

## Atribución de costos

Cada request se etiqueta con `tenant_id`, modelo y tokens (entrada/salida). El
costo = tokens × precio_por_modelo se acumula por tenant y se exporta a la capa
`llmops-observability` (contadores Prometheus con label `tenant`/`model`). Esto
permite facturar por uso real y detectar tenants que abusan.

## Ruteo de modelos y caching por tenant

- El **ruteo** (barato vs caro) puede tener overrides por tenant: un enterprise
  puede forzar siempre el modelo grande; un free, siempre el barato.
- El **cache semántico** es por tenant (namespace de cache = `tenant_id`) para no
  filtrar respuestas entre clientes.
