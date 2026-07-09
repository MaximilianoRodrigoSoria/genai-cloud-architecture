# Esqueleto Terraform del subconjunto desplegable de la plataforma GenAI (AWS).
# Es una REFERENCIA de estructura, no un despliegue completo listo para prod:
# muestra los recursos clave y cómo se parametrizan por tenant. Revisar y
# completar (IAM fino, redes, políticas) antes de usar de verdad.

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      project     = var.project
      environment = var.environment
      managed_by  = "terraform"
    }
  }
}

locals {
  name_prefix = "${var.project}-${var.environment}"
}

# --- Datos por tenant: tabla con partition key tenant_id ---
resource "aws_dynamodb_table" "tenant_data" {
  name         = "${local.name_prefix}-tenant-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tenant_id"
  range_key    = "item_id"

  attribute {
    name = "tenant_id"
    type = "S"
  }
  attribute {
    name = "item_id"
    type = "S"
  }
}

# --- Objetos por tenant: bucket con prefijos s3://.../{tenant_id}/ ---
resource "aws_s3_bucket" "tenant_objects" {
  bucket = "${local.name_prefix}-tenant-objects"
}

resource "aws_s3_bucket_public_access_block" "tenant_objects" {
  bucket                  = aws_s3_bucket.tenant_objects.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- Async: cola de ingesta / batch de embeddings ---
resource "aws_sqs_queue" "ingestion" {
  name                       = "${local.name_prefix}-ingestion"
  visibility_timeout_seconds = 300
}

# --- Secretos de la plataforma (nunca en código) ---
resource "aws_secretsmanager_secret" "app" {
  name = "${local.name_prefix}-app-secrets"
}

# --- Identidad de los tenants ---
resource "aws_cognito_user_pool" "tenants" {
  name = "${local.name_prefix}-users"
}

# NOTA (fuera de este skeleton, para completar):
# - API Gateway + WAF en el ingreso, con authorizer Cognito.
# - Cómputo stateless (ECS/Fargate o Lambda) para gateway + orquestación.
# - Inferencia: Amazon Bedrock (gestionada) y/o SageMaker (modelos propios).
# - Vector store: OpenSearch (k-NN) con namespace por tenant.
# - IAM fino por tenant (dynamodb:LeadingKeys) y VPC + PrivateLink.
