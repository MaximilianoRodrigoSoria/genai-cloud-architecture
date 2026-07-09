# ADR 0001 — Elección de proveedor cloud

- Estado: aceptada
- Fecha: 2026-07-09

## Contexto

Hay que servir un sistema GenAI (RAG + tools) multi-tenant, escalable y seguro,
sin administrar GPUs si se puede evitar. Las dos rutas realistas son AWS y GCP;
la consigna es **elegir una y ser coherente** en todo el diseño.

## Decisión

Se elige **AWS**. La inferencia gestionada se hace con **Amazon Bedrock** (modelos
gestionados, sin GPUs propias) y, para modelos propios, **SageMaker**. El resto:
API Gateway + ECS/Fargate (o Lambda), OpenSearch para vectores, DynamoDB/Aurora +
S3 para datos, Cognito para identidad, SQS para async.

## Alternativas evaluadas

- **GCP (Vertex AI + Cloud Run + Vector Search):** muy sólido y con buena UX de
  Vertex; se descarta solo por foco/coherencia, no por capacidad. Es un swap
  razonable si el target del negocio ya vive en GCP.
- **Multi-cloud desde el día 1:** rechazada — dobla la complejidad operativa sin
  beneficio real en un MVP. Se mantiene portabilidad *donde es barata* (Terraform,
  contenedores, pgvector) sin perseguir agnosticismo total.
- **Self-host de modelos en k8s propio:** rechazada para el MVP por el costo
  operativo de administrar GPUs y autoscaling de inferencia.

## Consecuencias

- (+) Time-to-market: Bedrock evita administrar GPUs.
- (+) Ecosistema integrado (IAM, Cognito, VPC, CloudWatch) reduce fricción de seguridad/observabilidad.
- (−) Acoplamiento a AWS; se mitiga con Terraform, contenedores y pgvector donde aplica.
- (−) Costos de inferencia gestionada a escala; se mitigan con caching + ruteo de modelos (ver `0002`).
