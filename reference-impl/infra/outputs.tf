output "tenant_data_table" {
  description = "Tabla DynamoDB de datos por tenant"
  value       = aws_dynamodb_table.tenant_data.name
}

output "tenant_objects_bucket" {
  description = "Bucket S3 de objetos por tenant"
  value       = aws_s3_bucket.tenant_objects.bucket
}

output "ingestion_queue_url" {
  description = "URL de la cola SQS de ingesta"
  value       = aws_sqs_queue.ingestion.url
}

output "user_pool_id" {
  description = "Cognito User Pool de tenants"
  value       = aws_cognito_user_pool.tenants.id
}
