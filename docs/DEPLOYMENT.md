# 🚀 Guia de Deployment AWS - CS2 Stats Bot

Este guia detalha todo o processo de deployment do CS2 Stats Bot na AWS usando Terraform e CI/CD automatizado.

## 📋 Pré-requisitos

### 1. Conta AWS
- Conta AWS Academy ou AWS Educate (conta de estudante)
- Access Keys configuradas (AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY)
- Região recomendada: `us-east-1` (mais recursos no Free Tier)

### 2. Ferramentas Locais
- [Terraform](https://www.terraform.io/downloads) >= 1.0
- [AWS CLI](https://aws.amazon.com/cli/) configurado
- Git
- (Opcional) [Session Manager Plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

### 3. Chave SSH
Crie um par de chaves SSH na AWS:
```bash
# Via AWS Console
# EC2 > Key Pairs > Create Key Pair
# Nome: cs2-bot-key
# Tipo: RSA
# Formato: .pem
# Salve o arquivo .pem em local seguro!
```

### 4. Domínio (Opcional mas Recomendado)
- Domínio próprio ou subdomínio
- Apontando para o IP da instância EC2 (configurar após deploy)

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│           AWS EC2 t2.micro              │
│  ┌─────────────────────────────────┐   │
│  │         Docker Compose          │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  │   │
│  │  │ Bot  │  │ MySQL│  │ Nginx│  │   │
│  │  └──────┘  └──────┘  └──────┘  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Security Group:                        │
│  - SSH (22)                            │
│  - HTTP (80)                           │
│  - HTTPS (443)                         │
└─────────────────────────────────────────┘
         ↓
    Elastic IP (fixo)
         ↓
    Let's Encrypt SSL
```

---

## 🔧 Configuração Inicial

### Passo 1: Configurar Variáveis Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edite `terraform.tfvars` com seus valores:

```hcl
aws_region    = "us-east-1"
instance_type = "t2.micro"
environment   = "prod"

# Chave SSH criada na AWS
key_name = "cs2-bot-key"

# Restringir SSH ao seu IP (recomendado)
allowed_ssh_cidr = ["SEU.IP.PUBLICO.AQUI/32"]

# SSL (opcional)
domain_name = "bot.seudominio.com"
ssl_email   = "seu-email@example.com"

# Secrets
bot_token        = "SEU_TOKEN_DISCORD"
gemini_api_key   = "SUA_CHAVE_GEMINI"
db_root_password = "senha_root_super_segura"
db_user          = "cs_user"
db_password      = "senha_user_segura"
db_name          = "cs_stats"
```

> [!CAUTION]
> **NUNCA commite o arquivo `terraform.tfvars`!** Ele está no `.gitignore` por segurança.

### Passo 2: Inicializar Terraform

```bash
cd terraform
terraform init
```

### Passo 3: Validar Configuração

```bash
terraform validate
terraform fmt
terraform plan
```

Revise o plano cuidadosamente antes de aplicar!

---

## 🚀 Deploy Inicial

### Opção A: Deploy Manual com Terraform

```bash
cd terraform

# Aplicar infraestrutura
terraform apply

# Confirmar com 'yes'
```

Após conclusão, anote os outputs:
- `instance_public_ip`: IP público da instância
- `ssh_command`: Comando para conectar via SSH

### Opção B: Deploy via GitHub Actions (Automatizado)

1. **Configurar Secrets no GitHub:**
   - Vá em: `Settings > Secrets and variables > Actions > New repository secret`
   - Adicione os seguintes secrets:

| Secret Name | Descrição | Exemplo |
|------------|-----------|---------|
| `AWS_ACCESS_KEY_ID` | Access Key da AWS | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Secret Key da AWS | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `EC2_HOST` | IP público da instância | `54.123.45.67` |
| `EC2_SSH_PRIVATE_KEY` | Chave privada SSH (.pem) | Conteúdo completo do arquivo |
| `EC2_KEY_NAME` | Nome da chave na AWS | `cs2-bot-key` |
| `BOT_TOKEN` | Token do Discord | `MTIwOTg...` |
| `GEMINI_API_KEY` | Chave do Gemini | `AIzaSy...` |
| `DB_ROOT_PASSWORD` | Senha root MySQL | `senha_root_segura` |
| `DB_USER` | Usuário MySQL | `cs_user` |
| `DB_PASSWORD` | Senha do usuário MySQL | `senha_user_segura` |
| `DB_NAME` | Nome do banco | `cs_stats` |

2. **Ativar Deploy Automático:**
   - Edite `.github/workflows/cd.yml`
   - Descomente as etapas do Terraform (linhas 20-56)
   - Commit e push para `main`

3. **Acompanhar Deploy:**
   - Vá em `Actions` no GitHub
   - Veja o workflow "CD - Deploy to AWS" executando

---

## 🔐 Configurar SSL/HTTPS

Após o primeiro deploy, configure SSL com Let's Encrypt:

```bash
# Conectar ao EC2
ssh -i ~/.ssh/cs2-bot-key.pem ubuntu@SEU_IP_PUBLICO

# Configurar variáveis
export DOMAIN_NAME=bot.seudominio.com
export SSL_EMAIL=seu-email@example.com

# Executar script de configuração SSL
cd /home/ubuntu/cs2-stats-bot
bash scripts/setup-ssl.sh
```

> [!IMPORTANT]
> Antes de executar, certifique-se de que:
> 1. Seu domínio aponta para o IP público da instância
> 2. As portas 80 e 443 estão abertas no Security Group
> 3. Não há outro serviço usando essas portas

Certificados serão renovados automaticamente a cada 90 dias via cron job.

---

## 📦 Deploy de Atualizações

### Deploy Manual

```bash
# Conectar ao EC2
ssh -i ~/.ssh/cs2-bot-key.pem ubuntu@SEU_IP_PUBLICO

# Executar deploy
cd /home/ubuntu/cs2-stats-bot
bash scripts/deploy.sh
```

### Deploy Automatizado (CI/CD)

1. Faça push para branch `main`
2. Pipeline CI executará testes e linting
3. Se CI passar, pipeline CD fará deploy automático
4. Acompanhe em `Actions` no GitHub

---

## 🔍 Monitoramento e Troubleshooting

### Ver Logs dos Containers

```bash
# Logs do bot
docker compose logs -f bot

# Logs do nginx
docker compose logs -f nginx

# Logs do MySQL
docker compose logs -f db

# Todos os logs
docker compose logs -f
```

### Verificar Status

```bash
# Status dos containers
docker compose ps

# Health check
curl http://localhost/health

# Ver processos
docker compose top
```

### Reiniciar Serviços

```bash
# Reiniciar todos
docker compose restart

# Reiniciar apenas o bot
docker compose restart bot

# Parar tudo
docker compose down

# Iniciar tudo
docker compose up -d
```

### Problemas Comuns

#### 1. Container não inicia

```bash
# Ver logs detalhados
docker compose logs bot

# Verificar .env
cat .env

# Reconstruir imagem
docker compose up --build -d
```

#### 2. Erro de SSL

```bash
# Verificar certificados
ls -la /var/lib/docker/volumes/cs2-stats-bot_letsencrypt/_data/live/

# Renovar certificado manualmente
docker run --rm \
    -v "$(pwd)/letsencrypt:/etc/letsencrypt" \
    certbot/certbot renew

# Reiniciar nginx
docker compose restart nginx
```

#### 3. Banco de dados não conecta

```bash
# Verificar se MySQL está rodando
docker compose ps db

# Testar conexão
docker compose exec db mysql -u root -p

# Ver logs do MySQL
docker compose logs db
```

#### 4. Out of Memory

```bash
# Ver uso de memória
free -h
docker stats

# Limpar containers/imagens antigas
docker system prune -a
```

---

## 💰 Custos Estimados (AWS)

### Free Tier (12 meses)
- EC2 t2.micro: **GRÁTIS** (750 horas/mês)
- 30 GB EBS: **GRÁTIS**
- 15 GB transferência: **GRÁTIS**
- Elastic IP (em uso): **GRÁTIS**

### Após Free Tier
- EC2 t2.micro: ~$8-10/mês
- 20 GB EBS: ~$2/mês
- Elastic IP (em uso): GRÁTIS
- Transferência: variável

**Total estimado: ~$10-12/mês** após Free Tier

> [!TIP]
> Para economizar ainda mais, use **Reserved Instances** ou **Savings Plans**

---

## 🛡️ Segurança

### Checklist de Segurança

- [ ] Chave SSH segura e não compartilhada
- [ ] SSH restrito ao seu IP (`allowed_ssh_cidr`)
- [ ] Secrets armazenados no GitHub Secrets
- [ ] Arquivo `.env` nunca commitado
- [ ] Senhas fortes para banco de dados
- [ ] SSL/TLS configurado
- [ ] Security Group minimalista
- [ ] Logs monitorados regularmente
- [ ] Backups configurados (ver próxima seção)

### Configurar Backups do Banco

```bash
# Script de backup
cat > /home/ubuntu/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/home/ubuntu/backups
mkdir -p $BACKUP_DIR
docker compose exec -T db mysqldump -u root -p$DB_ROOT_PASSWORD cs_stats | gzip > $BACKUP_DIR/cs_stats_$(date +%Y%m%d_%H%M%S).sql.gz
# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/cs_stats_*.sql.gz | tail -n +8 | xargs rm -f
EOF

chmod +x /home/ubuntu/backup-db.sh

# Adicionar ao crontab (backup diário às 2AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/backup-db.sh") | crontab -
```

---

## 📊 Próximos Passos

1. [ ] Configurar alarmes no CloudWatch
2. [ ] Implementar monitoramento com Prometheus/Grafana
3. [ ] Configurar Auto Scaling (se necessário)
4. [ ] Implementar blue-green deployment
5. [ ] Configurar Route 53 para DNS
6. [ ] Adicionar WAF (Web Application Firewall)

---

## 📚 Recursos Úteis

- [Documentação Terraform AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs dos containers
2. Consulte a seção de troubleshooting
3. Verifique se todos os secrets estão configurados
4. Revise o Security Group na AWS

**Em caso de emergência:**
```bash
# Parar tudo
docker compose down

# Limpar volumes (ATENÇÃO: perde dados!)
docker compose down -v

# Reconstruir do zero
docker compose up --build -d
```
