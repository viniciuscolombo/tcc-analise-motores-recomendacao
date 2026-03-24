# 📊 Análise de Desempenho: Bancos de Dados em Grafos vs. Relacionais para Motores de Recomendação

[cite_start]Este repositório contém o código-fonte desenvolvido para o PFC 1

## 🎯 Objetivo
[cite_start]O projeto visa desenvolver uma API de recomendação para avaliar e comparar a performance, o tempo de resposta de consultas e a escalabilidade arquitetural entre um banco de dados orientado a grafos (Neo4j) e um banco de dados relacional (PostgreSQL)[cite: 10].

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Processamento de Dados (ETL):** Pandas
* **Bancos de Dados:** PostgreSQL (Relacional) e Neo4j (Grafos)
* **Infraestrutura:** Docker e Docker Compose
* **Dataset:** MovieLens (Small)

## 🚀 Status Atual do Projeto
- [x] Estruturação do repositório e ambiente virtual.
- [x] Configuração da infraestrutura via Docker (Postgres e Neo4j).
- [x] Script de Extração e Transformação (ETL) dos dados do MovieLens.
- [x] Script de Carga (Load) populando o banco de dados PostgreSQL.
- [ ] Script de Carga (Load) para o banco de dados Neo4j.
- [ ] Desenvolvimento da API e Motores de Busca.

## ⚙️ Como rodar o projeto localmente
1. Clone o repositório.
2. Suba os bancos de dados utilizando o Docker:
   `docker-compose up -d`
3. Ative o ambiente virtual e instale as dependências.
4. Execute o script de ETL e carga:
   `python scripts/load_sql.py`
