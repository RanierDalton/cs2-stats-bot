# 🤖 CS Stats Bot: Seu Assistente de Estatísticas no Discord

Este é um bot de Discord em Python para rastrear e analisar estatísticas de jogadores e partidas de jogos como Counter-Strike, utilizando **MySQL** para persistência de dados.

A regra de negócio do banco de dados foca em quatro entidades principais:

| Tabela | Descrição Principal | Colunas Chave |
| :--- | :--- | :--- |
| **`player`** | Informações dos jogadores (nome e nick). | `id`, `name`, `nick` |
| **`map`** | Mapas disponíveis. | `id`, `name`, `is_active` |
| **`game`** | Registra cada partida (data, status, placares). | `id`, `dt`, `status`, `adversary_rounds`, `allies_rounds`, `fk_map` |
| **`game_data`** | Estatísticas individuais por jogador em uma partida. | `id`, `fk_player`, `fk_game`, `kills`, `deaths`, `assists`, `headshot`, `damage` |

---

## ⚙️ Instalação e Execução Local

Recomendamos **Docker e Docker Compose** para gerenciar o ambiente de desenvolvimento.

### 1. Preparação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/RanierDalton/cs2-stats-bot.git
    mkdir cs-stats-bot
    cd cs-stats-bot
    ```
2.  Crie e preencha o arquivo **`.env`** na raiz do projeto:

    ```env
    # .env
    BOT_TOKEN=SEU_TOKEN_DO_BOT_DISCORD
    GEMINI_API_KEY=SUA_CHAVE_DO_GEMINI

    # Configurações do Banco de Dados
    DB_HOST=db 
    DB_USER=cs_user
    DB_PASSWORD=senha_secreta
    DB_NAME=cs_stats
    ```
3.  Crie o arquivo **`docker-compose.yml`** para orquestrar os serviços `db` (MySQL) e `bot`:

    ```yaml
    version: '3.8'

    services:
      bot:
        build: .
        container_name: cs_stats_bot
        restart: always
        env_file:
          - .env 
        depends_on:
          - db
    ```

### 2. Execução

Suba os containers, construindo a imagem do bot a partir do **Dockerfile**:

```bash
docker compose up --build -d
````

Para ver os logs do bot:

```bash
docker logs -f cs_stats_bot
```

-----

## 📐 Estrutura e Modificações

O projeto possui a seguinte arquitetura:

```
.
├── image/                # Recursos estáticos
├── src/                  # Código modular
│   ├── main/             # Lógica de Comandos do Discord
│   └── shared/           # Módulos de conexão e queries SQL
├── .env                  # Variáveis de ambiente
├── main.py               # Ponto de entrada do Bot
└── requirements.txt      # Dependências Python
```

  * **Lógica do Bot:** Modifique ou adicione comandos em **`src/main/`**.
  * **Acesso ao DB:** Mantenha a camada de dados em **`src/shared/`**.
  * **Dependências:** Adicione bibliotecas ao **`requirements.txt`** e reconstrua a imagem (`docker compose up --build -d`).

-----

## 🚀 Build e Deploy em Produção

Os scripts a seguir automatizam a preparação de um ambiente Linux (Ubuntu) para o deploy.

### 1\. Script de Deploy do Bot (com Docker Compose)

Este script instala o Docker/Docker Compose, clona o repositório e inicia a aplicação orquestrada.

Crie um arquivo chamado **`deploy_bot.sh`**:

```bash
#!/bin/bash
set -e

# Atualiza e instala utilitários básicos
sudo apt-get update -y
sudo apt-get install ca-certificates curl git -y

# Instala o Docker
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Adiciona o usuário atual ao grupo docker
sudo usermod -aG docker "$USER"
echo "AVISO: Faça logout/login ou execute 'newgrp docker' para aplicar as permissões."

cd /home/$USER
docker compose up --build -d

echo "Deploy da Aplicação concluído. Containers rodando."
```

### 2\. Script de Configuração do Banco de Dados MySQL (Alternativa Sem Docker)

Use esta alternativa se não for usar o MySQL via Docker Compose.

Crie um arquivo chamado **`setup_db_host.sh`**:

```bash
#!/bin/bash
set -e

# Inicia e habilita o serviço MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Clonagem do repositório contendo o script SQL
git clone [https://github.com/InfraWatch-inc/database.git](https://github.com/InfraWatch-inc/database.git)

# Aplica o script SQL para criar o DB e as tabelas
sudo mysql < database/script.sql

echo "Banco de dados 'cs_stats' configurado."
```