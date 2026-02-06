FROM nginx:alpine

# Instalar Certbot para Let's Encrypt
RUN apk add --no-cache certbot certbot-nginx

# Copiar configuração customizada do nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar página HTML de status
COPY html/index.html /usr/share/nginx/html/index.html

# Criar diretório para ACME challenge
RUN mkdir -p /var/www/certbot

# Expor portas HTTP e HTTPS
EXPOSE 80 443

# Script de entrypoint customizado
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
