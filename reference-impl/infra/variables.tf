variable "region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Nombre del proyecto (prefijo de recursos)"
  type        = string
  default     = "genai-platform"
}

variable "environment" {
  description = "Entorno (dev/stage/prod)"
  type        = string
  default     = "dev"
}

variable "tenant_ids" {
  description = "Tenants a aprovisionar (namespaces/particiones lógicas)"
  type        = list(string)
  default     = ["t-free", "t-pro", "t-ent"]
}
