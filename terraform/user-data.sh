#!/bin/bash
set -e

# Script de inicialização da instância EC2
# Este script será executado na primeira inicialização da instância

echo "=== Iniciando configuração da instância EC2 ==="

# Atualizar sistema
apt-get update -y
apt-get upgrade -y

# Instalar dependências básicas
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git

# Instalar Docker
echo "=== Instalando Docker ==="
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Habilitar Docker para iniciar no boot
systemctl enable docker
systemctl start docker

# Adicionar usuário ubuntu ao grupo docker
usermod -aG docker ubuntu

# Criar diretório da aplicação
mkdir -p /home/ubuntu/cs2-stats-bot
cd /home/ubuntu/cs2-stats-bot

# Criar arquivo .env com as variáveis
cat > .env <<EOF
BOT_TOKEN=${bot_token}
GEMINI_API_KEY=${gemini_api_key}
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=${db_root_password}
DB_USER=${db_user}
DB_PASSWORD=${db_password}
DB_NAME=${db_name}
EOF

# Ajustar permissões
chown -R ubuntu:ubuntu /home/ubuntu/cs2-stats-bot
chmod 600 /home/ubuntu/cs2-stats-bot/.env

# Instalar Certbot para Let's Encrypt (se domínio configurado)
%{ if domain_name != "" }
echo "=== Instalando Certbot ==="
apt-get install -y certbot python3-certbot-nginx

# Nota: A configuração SSL será feita após o deploy inicial via script
echo "DOMAIN_NAME=${domain_name}" >> /home/ubuntu/cs2-stats-bot/.env
echo "SSL_EMAIL=${email}" >> /home/ubuntu/cs2-stats-bot/.env
%{ endif }

echo "=== Configuração inicial concluída ==="
echo "Próximos passos:"
echo "1. Clone o repositório: git clone https://github.com/SEU-USUARIO/cs2-stats-bot.git /home/ubuntu/cs2-stats-bot"
echo "2. Execute: docker compose up -d"
