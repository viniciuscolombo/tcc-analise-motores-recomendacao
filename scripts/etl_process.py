import pandas as pd
import os

def extract_and_transform():
    print("Iniciando o processamento dos dados do MovieLens...")
    
    movies_path = 'data/movies.csv'
    ratings_path = 'data/ratings.csv'
    
    if not os.path.exists(movies_path):
        print(f"Erro: Arquivo não encontrado em {movies_path}. Verifique se os CSVs estão na pasta 'data/'.")
        return None
        
    print("\n1. Lendo os arquivos CSV...")
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    print("2. Tratando e separando a coluna de gêneros...")
    
    # Transforma a string Action|Comedy em uma lista ['Action', 'Comedy']
    movies_df['genres_list'] = movies_df['genres'].str.split('|')
    
    filme_genero_df = movies_df[['movieId', 'genres_list']].explode('genres_list')
    filme_genero_df.rename(columns={'genres_list': 'genre'}, inplace=True)
    
    filme_genero_df = filme_genero_df[filme_genero_df['genre'] != '(no genres listed)']
    
    generos_unicos = filme_genero_df['genre'].unique()
    generos_df = pd.DataFrame(generos_unicos, columns=['nome_genero'])
    generos_df['id_genero'] = range(1, len(generos_df) + 1)
    
    print("\n--- Resumo dos Dados Transformados ---")
    print(f"Total de Filmes: {len(movies_df)}")
    print(f"Total de Avaliações: {len(ratings_df)}")
    print(f"Total de Gêneros Únicos: {len(generos_df)}")
    
    print("\nSucesso! Os dados estão limpos e prontos para a etapa de carga (Load).")
    
    return movies_df, ratings_df, filme_genero_df, generos_df

if __name__ == "__main__":
    extract_and_transform()