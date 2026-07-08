# Esqueleto de infraestructura (AWS) — subconjunto ilustrativo, no productivo.
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# API Gateway HTTP que expone el servicio de inferencia (stub).
resource "aws_apigatewayv2_api" "gateway" {
  name          = "genai-gateway-${var.env}"
  protocol_type = "HTTP"
  tags          = { project = "genai-cloud-architecture", env = var.env }
}

# Tabla particionada por tenant (clave de partición = tenant_id).
resource "aws_dynamodb_table" "tenant_data" {
  name         = "genai-tenant-data-${var.env}"
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
