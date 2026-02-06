terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Buscar AMI mais recente do Ubuntu 22.04
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group para a instância EC2
resource "aws_security_group" "bot_sg" {
  name        = "cs2-stats-bot-sg"
  description = "Security group para CS2 Stats Bot"

  # SSH
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Permitir todo tráfego de saída
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "cs2-stats-bot-sg"
    Environment = var.environment
    Project     = "CS2-Stats-Bot"
  }
}

# Instância EC2
resource "aws_instance" "bot_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.bot_sg.id]

  # Configuração de disco
  root_block_device {
    volume_type = "gp3"
    volume_size = 20  # GB - ajuste conforme necessário
    encrypted   = true
  }

  # User data para bootstrap da instância
  user_data = templatefile("${path.module}/user-data.sh", {
    bot_token       = var.bot_token
    gemini_api_key  = var.gemini_api_key
    db_root_password = var.db_root_password
    db_user         = var.db_user
    db_password     = var.db_password
    db_name         = var.db_name
    domain_name     = var.domain_name
    email           = var.ssl_email
  })

  tags = {
    Name        = "cs2-stats-bot-server"
    Environment = var.environment
    Project     = "CS2-Stats-Bot"
  }
}

# Elastic IP para IP fixo
resource "aws_eip" "bot_eip" {
  instance = aws_instance.bot_server.id
  domain   = "vpc"

  tags = {
    Name        = "cs2-stats-bot-eip"
    Environment = var.environment
    Project     = "CS2-Stats-Bot"
  }
}
