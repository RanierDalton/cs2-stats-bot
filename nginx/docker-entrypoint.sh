#!/bin/sh
set -e

# Script de inicialização do container nginx

echo "=== Nginx + Certbot Docker Entrypoint ==="

# Verificar se há certificados SSL
if [ -d "/etc/letsencrypt/live" ] && [ "$(ls -A /etc/letsencrypt/live)" ]; then
    echo "Certificados SSL encontrados"
else
    echo "AVISO: Nenhum certificado SSL encontrado"
    echo "Para gerar certificados, execute o script setup-ssl.sh no host"
fi

# Verificar configuração do nginx
nginx -t

# Executar comando passado como argumento
exec "$@"
