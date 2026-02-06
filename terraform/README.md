# 🏗️ Infraestrutura Terraform para CS2 Stats Bot

Este diretório contém a infraestrutura como código (IaC) para deployer o CS2 Stats Bot na AWS.

## 📁 Estrutura de Arquivos

```
terraform/
├── main.tf                    # Recursos AWS (EC2, Security Groups, EIP)
├── variables.tf               # Variáveis de configuração
├── outputs.tf                 # Outputs após deploy
├── user-data.sh              # Script de bootstrap da EC2
├── terraform.tfvars.example  # Template de configuração
└── .gitignore                # Arquivos ignorados pelo Git
```

## 🚀 Quick Start

### 1. Configurar Variáveis

```bash
cp terraform.tfvars.example terraform.tfvars
# Edite terraform.tfvars com seus valores
```

### 2. Inicializar Terraform

```bash
terraform init
```

### 3. Validar Configuração

```bash
terraform validate
terraform plan
```

### 4. Aplicar Infraestrutura

```bash
terraform apply
```

## 📋 Recursos Criados

- **EC2 Instance**: t2.micro Ubuntu 22.04 (Free Tier)
- **Security Group**: Portas 22 (SSH), 80 (HTTP), 443 (HTTPS)
- **Elastic IP**: IP público fixo
- **User Data**: Bootstrap automático com Docker

## 🔧 Variáveis Principais

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `aws_region` | Região AWS | `us-east-1` |
| `instance_type` | Tipo de instância | `t2.micro` |
| `key_name` | Nome da chave SSH | - |
| `domain_name` | Domínio (opcional) | `""` |
| `bot_token` | Token Discord (secret) | - |
| `gemini_api_key` | Chave Gemini (secret) | - |

Ver todas em [`variables.tf`](./variables.tf)

## 📤 Outputs

Após `terraform apply`, você receberá:

- `instance_public_ip`: IP público da instância
- `ssh_command`: Comando SSH para conectar
- `https_url`: URL do bot (HTTPS)

## 🔐 Segurança

> [!CAUTION]
> **Nunca commite arquivos sensíveis!**

Arquivos protegidos pelo `.gitignore`:
- `terraform.tfvars` (contém secrets)
- `*.tfstate` (pode conter dados sensíveis)
- `*.pem` / `*.key` (chaves privadas)

## 💡 Dicas

### Verificar custos antes de aplicar
```bash
terraform plan
# Revise os recursos que serão criados
```

### Destruir infraestrutura (quando não precisar mais)
```bash
terraform destroy
```

### Atualizar apenas variáveis de ambiente
```bash
# Edite terraform.tfvars
terraform apply -var="bot_token=NOVO_TOKEN"
```

### Ver estado atual
```bash
terraform show
```

## 📚 Documentação Completa

Para guia detalhado de deployment, consulte:
- [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)

## 🆘 Troubleshooting

### Erro: "key pair does not exist"
```bash
# Crie a chave na AWS Console primeiro:
# EC2 > Key Pairs > Create Key Pair
```

### Erro: "UnauthorizedOperation"
```bash
# Configure AWS credentials:
aws configure
# Ou use variáveis de ambiente:
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### Erro ao aplicar user-data
```bash
# Verifique sintaxe do script:
terraform validate

# Force recreação da instância:
terraform taint aws_instance.bot_server
terraform apply
```

## 🔗 Links Úteis

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
