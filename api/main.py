import time
from fastapi import FastAPI
from sqlalchemy import text
from api.database import get_postgres_connection
from api.database import get_neo4j_session

app = FastAPI(title="Motor de Recomendação")


@app.get("/")
def root():
    return {"status": "API rodando"}


@app.get("/recomendar/postgres/{user_id}")
def recomendar_postgres(user_id: int):
    query = text("""
        select f.title
        from filmes f
        join filme_genero fg on f."movieId" = fg."movieId"
        where fg.id_genero in(
            select fg2.id_genero 
            from avaliacoes a 
            join filme_genero fg2 on a."movieId" = fg2."movieId"
            where a."userId" = :user_id and a.rating >= 4.0
        )
        and f."movieId" not in(
            select "movieId" from avaliacoes where "userId" = :user_id
        )
        group by f."movieId", f.title
        order by count(fg.id_genero) desc
        limit 5;
        """)

    start_time = time.time()

    with get_postgres_connection() as conn:
        result = conn.execute(query, {"user_id": user_id}).fetchall()

        end_time = time.time()

        filmes_recomendados = [row[0] for row in result]

        tempo_ms = round((end_time - start_time) * 1000, 2)

        return {
            "usuario_alvo": user_id,
            "motor": "PostgreSQL",
            "tempo_execucao_ms": tempo_ms,
            "recomendacoes": filmes_recomendados,
        }


# nós ficam entre parenteses(u:User) e relacionamentos ficam entre colchetes-r[r:RATED]->


@app.get("/recomendar/neo4j/{user_id}")
def recomendar_neo4j(user_id: int):
    query = """
        match (u:User {userId: $user_id})-[r:RATED]->(:Movie)-[:IN_GENRE]->(g:Genre)
        where r.rating >= 4.0
        with u, collect(DISTINCT g) as generos_favoritos
        
        match (f:Movie)-[:IN_GENRE]->(g2:Genre)
        where g2 in generos_favoritos
        
        and not (u)-[:RATED]->(f)
        
        return f.title as title, count(g2) as score
        order by score desc
        limit 5
    """

    start_time = time.time()

    with get_neo4j_session() as session:
        result = session.run(query, user_id=user_id)
        filmes_recomendados = [record["title"] for record in result]

        end_time = time.time()

        tempo_ms = round((end_time - start_time) * 1000, 2)

        return {
            "usuario_alvo": user_id,
            "motor": "Neo4j",
            "tempo_execucao_ms": tempo_ms,
            "recomendacoes": filmes_recomendados,
        }

#aqui segue uma ordem, em primeiro lugar encontra filmes que o usuario alvo avaliou acima/igual a 4.
#em segundo lugar ele acha os vizinhos, cujo sao usuarios que gostaram dos mesmos filmes
#em terceiro lugar pega os outros filmes que os vizinhos gostaram
#em quarto lugar verifica que o usuario ainda nao viu esses filmes novos 
#em quinto lugar calculr a forma de recomendacao baseada em quantos vizinhos gostaram


@app.get("/recomendar/colaborativo/neo4j/{user_id}")
def recomendar_colaborativo_neo4j(user_id: int):
    query = """
        MATCH (u1:User {userId: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
        WHERE r1.rating >= 4.0 AND r2.rating >= 4.0 AND u1 <> u2
        WITH u1, u2, count(m) AS forca_amizade
        ORDER BY forca_amizade DESC 
        LIMIT 50
        
        MATCH (u2)-[r3:RATED]->(m2:Movie)
        WHERE r3.rating >= 4.0 AND NOT (u1)-[:RATED]->(m2)
        
        RETURN m2.title AS title, count(u2) AS score
        ORDER BY score DESC
        LIMIT 5
    """
    
    start_time = time.time()
    
    with get_neo4j_session() as session:
        result = session.run(query, user_id=user_id)
        filmes_recomendados = [record["title"] for record in result]
        
    end_time = time.time()
    tempo_ms = round((end_time - start_time) * 1000,2)
    
    return {
        "usuario_alvo": user_id,
        "motor":"Neo4j (Colaborativo)",
        "tempo_execucao_ms": tempo_ms,
        "recomendacoes": filmes_recomendados
    }
    
    
#Aqui ele segue a mesma premissa da busca de cima, so que com o postgres

@app.get("/recomendar/colaborativo/postgres/{user_id}")
def recomendar_colaborativo_postgres(user_id: int):
    query = text("""
        with FilmesAlvo AS (
            select "movieId" 
            from avaliacoes 
            where "userId" = :user_id and rating >= 4.0
        ),
        Vizinhos AS (
            select distinct a."userId"
            from avaliacoes a
            join FilmesAlvo fa ON a."movieId" = fa."movieId"
            where a."userId" != :user_id and a.rating >= 4.0
        ),
        Recomendacoes AS (
            select a."movieId", COUNT(distinct a."userId") as score
            from avaliacoes a
            join Vizinhos v ON a."userId" = v."userId"
            where a.rating >= 4.0
              and a."movieId" NOT IN (select "movieId" from avaliacoes where "userId" = :user_id)
            group by a."movieId"
        )
        select f.title
        from Recomendacoes r
        join filmes f ON r."movieId" = f."movieId"
        order by r.score desc
        LIMIT 5;
    """)
    
    start_time = time.time()
    
    with get_postgres_connection() as conn:
        result = conn.execute(query, {"user_id": user_id}).fetchall()
                             
    end_time = time.time()
    tempo_ms = round((end_time - start_time) * 1000, 2)                         
                             
    filmes_recomendados = [row[0] for row in result]                         
                             
    return{
        "usuario_alvo": user_id,
        "motor": "PostgresSQL (Colaborativo)",
        "tempo_execucao_ms": tempo_ms,
        "recomendacoes": filmes_recomendados
    }                         
    