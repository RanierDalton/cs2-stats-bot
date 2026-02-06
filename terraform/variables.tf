variable "aws_region" {
  description = "Região AWS para deploy"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de deployment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "instance_type" {
  description = "Tipo de instância EC2"
  type        = string
  default     = "t2.micro"  # Free tier elegível
}

variable "key_name" {
  description = "Nome da chave SSH para acesso à instância EC2"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "Lista de CIDRs permitidos para acesso SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # ATENÇÃO: Restrinja isso para seu IP em produção!
}

variable "domain_name" {
  description = "Nome de domínio para o bot (opcional, usado para SSL)"
  type        = string
  default     = ""
}

variable "ssl_email" {
  description = "Email para renovação de certificados Let's Encrypt"
  type        = string
  default     = ""
}

# Secrets - devem ser passados via tfvars ou variáveis de ambiente
variable "bot_token" {
  description = "Token do Discord Bot"
  type        = string
  sensitive   = true
}

variable "gemini_api_key" {
  description = "Chave de API do Gemini"
  type        = string
  sensitive   = true
}

variable "db_root_password" {
  description = "Senha root do MySQL"
  type        = string
  sensitive   = true
  default     = "change-me-root-password"
}

variable "db_user" {
  description = "Usuário do banco de dados"
  type        = string
  default     = "cs_user"
}

variable "db_password" {
  description = "Senha do usuário do banco de dados"
  type        = string
  sensitive   = true
  default     = "change-me-user-password"
}

variable "db_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "cs_stats"
}
