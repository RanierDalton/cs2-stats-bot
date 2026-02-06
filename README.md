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

### 2. Execução

Suba os containers, construindo a imagem do bot a partir do **Dockerfile**:

```bash
docker compose up --build -d
```

#### 2.1 Apenas o Banco de Dados (Docker Run)

Caso deseje rodar o banco de dados de forma isolada (útil para desenvolvimento local do bot fora do container). 

> [!IMPORTANT]
> **Você deve executar o comando abaixo de dentro da pasta raiz do projeto (`cs2-stats-bot`)**. Caso contrário, o Docker poderá criar um diretório vazio em vez de usar o arquivo `db.sql`.

No terminal (dentro da pasta `cs2-stats-bot`):

```bash
# Se estiver no Linux/macOS ou PowerShell (Windows)
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=senha_secreta -e MYSQL_DATABASE=cs_stats -p 3306:3306 -d mysql:8.0
```

> [!NOTE]
> O arquivo `db.sql` é mapeado como volume e executado automaticamente pelo MySQL na inicialização do container. Se houver erro de "batch_readline", verifique se você não está tentando montar um diretório em vez do arquivo SQL.


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

## 🧪 Testes e Qualidade de Código

Para garantir a estabilidade e o padrão do código, utilizamos `unittest`, `flake8` e `autopep8`.

### 1. Executando Testes Unitários
Para rodar a suíte de testes (atualmente 27 testes):

```powershell
# Windows
$env:PYTHONPATH='.'; python -m unittest discover -s tests

# Linux/Mac
export PYTHONPATH=$PYTHONPATH:.
python -m unittest discover -s tests
```

### 2. Verificando Lint (Flake8)
Para verificar se o código segue o padrão (PEP 8 com ajustes):

```bash
flake8 .
```

### 3. Corrigindo Formatação Automaticamente (Autopep8)
Para corrigir automaticamente espaços, indentação e outros erros de estilo:

```bash
autopep8 --in-place --recursive --aggressive .
```


-----

## 🚀 Deploy em Produção na AWS

O projeto possui infraestrutura automatizada para deploy na AWS usando **Terraform** e **GitHub Actions (CI/CD)**.

### Recursos de Infraestrutura

- **Terraform**: Infraestrutura como código para AWS (EC2, Security Groups, Elastic IP)
- **Docker Compose**: Orquestração de containers (Bot, MySQL, Nginx)
- **Nginx**: Reverse proxy com HTTPS (Let's Encrypt)
- **CI/CD**: Pipeline automatizado com GitHub Actions

### Quick Start

```bash
# 1. Configurar Terraform
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edite terraform.tfvars com suas credenciais

# 2. Deploy da infraestrutura
terraform init
terraform plan
terraform apply

# 3. Configurar SSL (após deploy)
ssh -i ~/.ssh/sua-chave.pem ubuntu@SEU_IP
cd /home/ubuntu/cs2-stats-bot
bash scripts/setup-ssl.sh
```

### Documentação Completa

Para guia detalhado de deployment, consulte:
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guia completo de deployment AWS
- **[terraform/README.md](terraform/README.md)** - Documentação Terraform

### Estrutura de Infraestrutura

```
.
├── terraform/          # Infraestrutura como código (AWS)
│   ├── main.tf        # Recursos AWS
│   ├── variables.tf   # Variáveis configuráveis
│   └── outputs.tf     # Outputs do deploy
├── nginx/             # Configuração do servidor web
│   ├── nginx.conf     # Config HTTPS/SSL
│   └── Dockerfile     # Image nginx + Certbot
├── scripts/           # Scripts de automação
│   ├── deploy.sh      # Deploy/atualização
│   └── setup-ssl.sh   # Configuração SSL
├── .github/workflows/ # CI/CD Pipelines
│   ├── ci.yml        # Testes e lint
│   └── cd.yml        # Deploy automático
└── docs/              # Documentação
    └── DEPLOYMENT.md  # Guia completo
```

### CI/CD Automatizado

O projeto possui pipelines GitHub Actions:
- **CI**: Executa em cada push/PR - testes, linting, build Docker
- **CD**: Executa após CI passar - deploy automático na AWS

Ver workflows em [`.github/workflows/`](.github/workflows/)
