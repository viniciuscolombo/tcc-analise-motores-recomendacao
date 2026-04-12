Análise de Desempenho: Bancos de Dados em Grafos vs. Relacionais para Motores de Recomendação

Este repositório contém o código-fonte desenvolvido para o PFC 1

##  Objetivo
O projeto visa desenvolver uma API de recomendação para avaliar e comparar a performance, o tempo de resposta de consultas e a escalabilidade arquitetural entre um banco de dados orientado a grafos (Neo4j) e um banco de dados relacional (PostgreSQL).

##  Tecnologias Utilizadas
* **Linguagem:** Python
* **Processamento de Dados (ETL):** Pandas
* **Bancos de Dados:** PostgreSQL (Relacional) e Neo4j (Grafos)
* **Infraestrutura:** Docker e Docker Compose
* **Dataset:** MovieLens (Small)

##  Configurações dos dados
Os arquivos de dados brutos (.csv) não são sincronizados com o repositório para manter a leveza do projeto. Siga os passos abaixo para configurar o ambiente:
1. Baixe o dataset MovieLens Latest Small: https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
2. Crie uma pasta chamada data na raiz do projeto.
3. Extraia o arquivo .zip e mova os arquivos movies.csv e ratings.csv para dentro da pasta data.

##  Como rodar o projeto localmente
1. Clone o repositório.
2. Suba os bancos de dados utilizando o Docker:
   `docker-compose up -d`
3. Ative o ambiente virtual e instale as dependências.
4. Execute o script de ETL e carga:
   `python scripts/load_sql.py`
   `python scripts/load_graph.py`
