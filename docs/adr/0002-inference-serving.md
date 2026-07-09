# ADR 0002 — Serving de inferencia, ruteo y control de costos

- Estado: aceptada
- Fecha: 2026-07-09

## Contexto

La inferencia LLM es el mayor costo y la mayor fuente de latencia de la
plataforma. Necesitamos servirla de forma escalable y con el gasto bajo control,
sin sacrificar calidad en las tareas que sí la requieren.

## Decisión

- **Serving:** Amazon Bedrock como default (modelos gestionados, autoscaling
  implícito). SageMaker solo para modelos propios/fine-tuned.
- **Ruteo de modelos:** un router clasifica cada request y manda las tareas
  simples a un modelo **barato** (p. ej. Haiku) y las complejas a uno **caro**
  (Sonnet/Opus). Se puede overridear por tenant/tier.
- **Caching semántico:** antes de inferir, se busca una respuesta previa
  suficientemente similar; si existe, se devuelve sin pagar inferencia.
- **Atribución de costo:** cada request suma tokens × precio_por_modelo, etiquetado
  por `tenant_id`, exportado a observabilidad.

## Alternativas evaluadas

- **Un solo modelo grande para todo:** simple pero caro y con latencia peor en
  tareas triviales. Rechazada.
- **Sin cache:** rechazada — un porcentaje alto de prompts se repite o se parece;
  cachear es la palanca de costo más barata de implementar.
- **Batching de inferencia síncrono:** se reserva para cargas async (ingesta),
  no para el request interactivo, donde perjudica la latencia.

## Consecuencias

- (+) Costo por request significativamente menor (cache + ruteo).
- (+) Latencia mejor en el caso común (tareas simples al modelo rápido).
- (−) Complejidad: hay que mantener el router y la política de similitud del cache.
- (−) Riesgo de cache stale o de un mal ruteo; se mitiga con umbral de similitud
  conservador y overrides por tenant. La `reference-impl/gateway/` implementa y
  testea el router y el cache.
