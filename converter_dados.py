import csv
import os

def converter_dat_para_csv(arquivo_entrada, arquivo_saida, cabecalhos):
    caminho_entrada = os.path.join('dataset', arquivo_entrada)
    caminho_saida = os.path.join('dataset', arquivo_saida)
    
    print(f"Convertendo {arquivo_entrada} para {arquivo_saida}")
    
    with open(caminho_entrada, 'r', encoding='latin-1') as f_in, \
         open(caminho_saida, 'w', encoding='utf-8', newline='') as f_out:
        
        escritor = csv.writer(f_out)
        escritor.writerow(cabecalhos)
        
        for linha in f_in:
            campos = linha.strip().split('::')
            escritor.writerow(campos)
            
    print(f"Concluido: {arquivo_saida}")

if __name__ == "__main__":
    print("Iniciando conversao")
    
    converter_dat_para_csv(
        'ratings.dat', 
        'ratings.csv', 
        ['userId', 'movieId', 'rating', 'timestamp']
    )

    converter_dat_para_csv(
        'movies.dat', 
        'movies.csv', 
        ['movieId', 'title', 'genres']
    )
    
    converter_dat_para_csv(
        'users.dat', 
        'users.csv', 
        ['userId', 'gender', 'age', 'occupation', 'zip']
    )
    
    print("Conversao finalizada com sucesso")