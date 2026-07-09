# Infra (Terraform skeleton)

Esqueleto de la infraestructura AWS del subconjunto desplegable: datos por tenant
(DynamoDB), objetos por tenant (S3), cola de ingesta (SQS), secretos (Secrets
Manager) e identidad (Cognito). Es una **referencia de estructura** — falta
completar IAM fino, red (VPC/PrivateLink), API Gateway + WAF, cómputo (ECS/Lambda),
inferencia (Bedrock/SageMaker) y el vector store (OpenSearch), tal como marca
`docs/architecture.md`.

## Uso

```bash
terraform init
terraform plan -var="environment=dev"
# terraform apply   # requiere credenciales AWS y revisar el plan
```

> No lo apliques tal cual en una cuenta real sin revisar: es un punto de partida
> para razonar la infra, no un módulo de producción endurecido.
