#!/bin/bash
set -e

# Script de deploy/atualização do bot no EC2
# Executar este script no servidor EC2 para atualizar a aplicação

echo "=== Deploy/Atualização do CS2 Stats Bot ==="

# Navegar para o diretório da aplicação
cd /home/ubuntu/cs2-stats-bot

# Fazer backup do .env atual
if [ -f .env ]; then
    echo "Fazendo backup do arquivo .env..."
    cp .env .env.backup
fi

# Atualizar código do repositório
echo "Atualizando código do repositório..."
if [ -d .git ]; then
    git fetch origin
    git reset --hard origin/main
else
    echo "AVISO: Diretório não é um repositório Git"
    echo "Clone o repositório manualmente se necessário"
fi

# Restaurar .env se foi removido
if [ ! -f .env ] && [ -f .env.backup ]; then
    echo "Restaurando arquivo .env..."
    cp .env.backup .env
fi

# Parar containers existentes
echo "Parando containers..."
docker compose down

# Limpar imagens antigas (opcional)
read -p "Limpar imagens Docker antigas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Limpando imagens antigas..."
    docker image prune -af
fi

# Rebuild e restart dos containers
echo "Reconstruindo e iniciando containers..."
docker compose up --build -d

# Aguardar containers iniciarem
echo "Aguardando containers iniciarem..."
sleep 10

# Verificar status dos containers
echo ""
echo "=== Status dos Containers ==="
docker compose ps

# Verificar logs do bot
echo ""
echo "=== Últimas Linhas dos Logs do Bot ==="
docker compose logs --tail=20 bot

# Health check
echo ""
echo "=== Health Check ==="
if docker compose ps | grep -q "Up"; then
    echo "✓ Containers estão rodando"
    
    # Testar endpoint de health se disponível
    if curl -sf http://localhost/health > /dev/null; then
        echo "✓ Health endpoint respondendo"
    fi
    
    echo ""
    echo "Deploy concluído com sucesso! 🚀"
else
    echo "✗ ERRO: Alguns containers não estão rodando"
    echo "Verifique os logs com: docker compose logs"
    exit 1
fi

# Mostrar informações úteis
echo ""
echo "=== Informações Úteis ==="
echo "Ver logs do bot: docker compose logs -f bot"
echo "Ver logs do nginx: docker compose logs -f nginx"
echo "Ver todos os logs: docker compose logs -f"
echo "Reiniciar serviços: docker compose restart"
echo "Parar serviços: docker compose down"
