#!/bin/bash
set -e

# Script para configurar SSL/TLS com Let's Encrypt
# Executar este script após o primeiro deploy

echo "=== Configuração de SSL com Let's Encrypt ==="

# Verificar variáveis de ambiente
if [ -z "$DOMAIN_NAME" ] || [ -z "$SSL_EMAIL" ]; then
    echo "ERRO: Variáveis DOMAIN_NAME e SSL_EMAIL devem estar definidas"
    echo "Exemplo:"
    echo "  export DOMAIN_NAME=bot.meudominio.com"
    echo "  export SSL_EMAIL=seu-email@example.com"
    exit 1
fi

echo "Domínio: $DOMAIN_NAME"
echo "Email: $SSL_EMAIL"

# Verificar se nginx está rodando
if ! docker ps | grep -q nginx; then
    echo "ERRO: Container nginx não está rodando"
    echo "Execute: docker compose up -d nginx"
    exit 1
fi

# Parar nginx temporariamente para obter certificado
echo "Parando nginx temporariamente..."
docker compose stop nginx

# Executar Certbot em modo standalone
echo "Obtendo certificado SSL..."
docker run --rm \
    -p 80:80 \
    -p 443:443 \
    -v "$(pwd)/letsencrypt:/etc/letsencrypt" \
    -v "$(pwd)/certbot_www:/var/www/certbot" \
    certbot/certbot certonly \
    --standalone \
    --email "$SSL_EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN_NAME"

if [ $? -eq 0 ]; then
    echo "✓ Certificado SSL obtido com sucesso!"
    
    # Atualizar nginx.conf com o domínio correto
    echo "Atualizando configuração do nginx..."
    sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN_NAME/g" nginx/nginx.conf
    
    # Reiniciar nginx
    echo "Reiniciando nginx..."
    docker compose up -d nginx
    
    echo "✓ SSL configurado com sucesso!"
    echo "Seu bot está disponível em: https://$DOMAIN_NAME"
else
    echo "✗ Erro ao obter certificado SSL"
    echo "Verifique se:"
    echo "  1. O domínio $DOMAIN_NAME aponta para este servidor"
    echo "  2. As portas 80 e 443 estão abertas no firewall"
    echo "  3. Não há outro processo usando as portas 80/443"
    exit 1
fi

# Configurar renovação automática
echo "Configurando renovação automática..."
cat > /tmp/renew-cert.sh << 'EOF'
#!/bin/bash
docker run --rm \
    -v "$(pwd)/letsencrypt:/etc/letsencrypt" \
    -v "$(pwd)/certbot_www:/var/www/certbot" \
    certbot/certbot renew --quiet

docker compose restart nginx
EOF

chmod +x /tmp/renew-cert.sh
sudo mv /tmp/renew-cert.sh /usr/local/bin/renew-cert.sh

# Adicionar ao crontab (executa diariamente às 3AM)
(crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/renew-cert.sh") | crontab -

echo "✓ Renovação automática configurada"
echo "Certificados serão renovados automaticamente quando necessário"
