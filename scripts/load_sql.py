import pandas as pd
from sqlalchemy import create_engine
from etl_process import extract_and_transform

def load_to_postgres():
    movies_df, ratings_df, filme_genero_df, generos_df = extract_and_transform()

    print("\n3. Conectando ao banco PostgreSQL (via Docker)...")
    engine = create_engine('postgresql://user_tcc:password_tcc@localhost:5432/movielens_db')

    print("4. Iniciando a inserção dos dados (Isso pode levar alguns segundos)...")
    
    print(" -> Inserindo Gêneros...")
    generos_df.to_sql('generos', engine, if_exists='replace', index=False)

    print(" -> Inserindo Filmes...")
    movies_df[['movieId', 'title']].to_sql('filmes', engine, if_exists='replace', index=False)

    print(" -> Inserindo Relações Filme-Gênero...")
    filme_genero_completo = filme_genero_df.merge(generos_df, left_on='genre', right_on='nome_genero')
    relacao_final = filme_genero_completo[['movieId', 'id_genero']]
    relacao_final.to_sql('filme_genero', engine, if_exists='replace', index=False)

    print(" -> Inserindo Avaliações...")
    ratings_df.to_sql('avaliacoes', engine, if_exists='replace', index=False)

    print("\nSucesso! Carga no PostgreSQL concluída. O banco relacional está populado.")

if __name__ == "__main__":
    load_to_postgres()