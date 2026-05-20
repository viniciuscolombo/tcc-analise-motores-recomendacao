import requests
import concurrent.futures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

usuario_teste = 1
requisicoes_por_cenario = 50
cenarios_concorrencia = [5, 10, 20, 50] 

def fazer_requisicao(url):
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            return resposta.json().get("tempo_execucao_ms", None)
        return None
    except:
        return None

def rodar_teste(url, concorrencia):
    tempos = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concorrencia) as executor:
        resultados = executor.map(fazer_requisicao, [url] * requisicoes_por_cenario)
    
    for tempo in resultados:
        if tempo is not None:
            tempos.append(tempo)
            
    if not tempos:
        return 5000.0 
    
    return round(sum(tempos) / len(tempos), 2)

if __name__ == "__main__":
    url_postgres = f"http://127.0.0.1:8000/recomendar/colaborativo/postgres/{usuario_teste}"
    url_neo4j = f"http://127.0.0.1:8000/recomendar/colaborativo/neo4j/{usuario_teste}"
    
    medias_postgres = []
    medias_neo4j = []
    
    print("Teste de Escalabilidade e Concorrência")
    
    try:
        requests.get(url_postgres)
        requests.get(url_neo4j)
    except:
        print("ERRO: API desligada")
        exit()

    for c in cenarios_concorrencia:
        print(f"\nTestando com {c} usuários simultâneos")
        
        print(" -> Avaliando PostgreSQL")
        media_pg = rodar_teste(url_postgres, c)
        medias_postgres.append(media_pg)
        
        print(" -> Avaliando Neo4j")
        media_neo = rodar_teste(url_neo4j, c)
        medias_neo4j.append(media_neo)
        
        print(f"   [Médias] Postgres: {media_pg}ms | Neo4j: {media_neo}ms")

    print("\nConstruindo o segundo gráfico de linhas")
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(cenarios_concorrencia, medias_postgres, marker='o', label='PostgreSQL', color='#336699', linewidth=2.5)
    plt.plot(cenarios_concorrencia, medias_neo4j, marker='s', label='Neo4j', color='#45b597', linewidth=2.5)
    
    for x, y in zip(cenarios_concorrencia, medias_postgres):
        plt.text(x, y + 100, f"{y}ms", ha='center', va='bottom', color='#336699', fontweight='bold')
    for x, y in zip(cenarios_concorrencia, medias_neo4j):
        plt.text(x, y - 150, f"{y}ms", ha='center', va='top', color='#45b597', fontweight='bold')

    plt.title('Escalabilidade: Tempo de Resposta vs Carga Concorrente', fontsize=14, fontweight='bold')
    plt.xlabel('Número de Usuários Simultâneos (Concorrência)', fontsize=12)
    plt.ylabel('Tempo Médio de Resposta (ms)', fontsize=12)
    plt.xticks(cenarios_concorrencia)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    
    nome_arquivo = 'grafico_escalabilidade.png'
    plt.savefig(nome_arquivo, bbox_inches='tight')
    print(f"\n🏆 Sucesso! Segundo gráfico salvo como '{nome_arquivo}'!")