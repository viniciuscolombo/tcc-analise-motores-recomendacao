import requests
import concurrent.futures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

#config
qtd_testes = 100
concorrencia = 20 
usuario_teste = 1

def fazer_requisicao(url):
    try:
        resposta = requests.get(url).json()
        return resposta["tempo_execucao_ms"]
    except Exception:
        return None 
    
def rodar_teste_stress(motor, url):
    print(f"\n fazendo {qtd_testes} requisicoes contra o {motor} ({concorrencia} usuarios juntos)")
    tempos = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concorrencia) as executor:
        resultados = executor.map(fazer_requisicao, [url] * qtd_testes)
        
    for tempo in resultados:
        if tempo is not None:
            tempos.append(tempo)
            print(".", end="", flush=True)
        else:
            print("x", end="", flush=True)
            
    media = round(sum(tempos) / len(tempos), 2)
    tempo_max = round(max(tempos), 2)
    tempo_min = round(min(tempos), 2)
    
    print(f"\n Resultados {motor}:")
    print(f" - Mais rápido: {tempo_min} ms")
    print(f" - Mais lento: {tempo_max} ms")
    print(f" - Média: {media} ms")
    
    return media

if __name__ == "__main__":
    url_postgres = f"http://127.0.0.1:8000/recomendar/postgres/{usuario_teste}"
    url_neo4j = f"http://127.0.0.1:8000/recomendar/neo4j/{usuario_teste}"
    
    print("ligando os bancos")
    requests.get(url_postgres)
    requests.get(url_neo4j)
    
    media_pg = rodar_teste_stress("PostgreSQL", url_postgres)
    media_neo = rodar_teste_stress("Neo4j", url_neo4j)
    
    print("\n Montando grafico de resultados")
    
    motores = ['PostgreSQL', 'Neo4j']
    medias = [media_pg, media_neo]
    cores = ['#336699', '#45b597']
    
    plt.figure(figsize=(8, 5))
    barras = plt.bar(motores, medias, color=cores)
    
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 1, f'{yval} ms', ha='center', va='bottom', fontweight='bold')
        
    plt.title('Teste de Carga: Tempo Médio de Resposta', fontsize=14)
    plt.ylabel('Tempo em Milissegundos (ms)', fontsize=12)
    plt.ylim(0, max(medias) * 1.2) 
    
    nome_arquivo = 'grafico_resultado.png'
    plt.savefig(nome_arquivo, bbox_inches='tight')
    print(f"✅ Gráfico salvo com sucesso na sua pasta como '{nome_arquivo}'!")