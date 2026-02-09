#!/usr/bin/env python
"""
Baseado na infraestrutura definida:
- EC2 Instance com Docker Compose
- Security Group com portas 22, 80, 443
- Elastic IP para IP fixo
- Serviços Docker: Nginx, Bot, MySQL, MinIO
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import GenericDatabase
from diagrams.onprem.database import MySQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.saas.chat import Discord

# Configurações do diagrama
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
}

with Diagram(
    "CS2 Stats Bot - Arquitetura AWS (Real - Terraform)",
    filename="aws_architecture_diagram",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    outformat="png"
):

    users = Discord("Usuários Discord")

    with Cluster("AWS Cloud"):
        ec2 = EC2("EC2 Instance\nt3.medium")

        with Cluster("Docker Compose\n(dentro da EC2)", graph_attr={"bgcolor": "lightblue"}):

            with Cluster("Containers (bot_network)"):
                nginx = Nginx("Nginx\nReverse Proxy + SSL")
                bot = Python("Discord Bot\nOCR + Gemini AI")
                mysql = MySQL("MySQL 8.0")
                minio = Docker("MinIO\nImage Storage")

            with Cluster("Docker Volumes"):
                vol_db = Docker("db_data")
                vol_minio = Docker("minio_data")
                vol_ssl = Docker("letsencrypt")

    users >> Edge(label="HTTPS/WSS") >> ec2
    ec2 >> Edge(label="") >> nginx
    nginx >> Edge(label="proxy") >> bot

    bot >> Edge(label="SQL") >> mysql
    bot >> Edge(label="upload img") >> minio
    bot >> Edge(label="Discord API", style="dashed") >> users

    mysql >> Edge(style="dotted") >> vol_db
    minio >> Edge(style="dotted") >> vol_minio
    nginx >> Edge(style="dotted") >> vol_ssl

print("✅ Diagrama gerado: aws_architecture_diagram.png")
