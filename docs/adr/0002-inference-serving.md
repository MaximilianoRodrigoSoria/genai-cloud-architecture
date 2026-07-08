# ADR 0002 — Serving de inferencia

## Estado
Aceptada.

## Contexto
Hay que decidir cómo servir la inferencia: gestionada vs self-hosted, y cómo
optimizar costo/latencia.

## Decisión
Inferencia **gestionada (Bedrock/Vertex)** + **caching semántico** + **ruteo de
modelos** (barato para tareas simples). Batching donde el caso lo permita.

## Consecuencias
- (+) Costo y latencia más bajos por cache y ruteo.
- (−) Complejidad de invalidación de cache (se acota con TTL y umbral de similitud).
