import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def testar_por_volume(motor, base_url, limites_vizinhos):
    print(f"\nAvaliando {motor} por volume de varredura")
    tempos_medios = []
    
    for limite in limites_vizinhos:
        url = f"{base_url}?limite_vizinhos={limite}"
        print(f" -> Buscando com limite de {limite} vizinhos")
        
        tempos_requisicao = []
        for _ in range(5):
            try:
                resposta = requests.get(url, timeout=10)
                if resposta.status_code == 200:
                    tempo = resposta.json().get("tempo_execucao_ms", None)
                    if tempo is not None:
                        tempos_requisicao.append(tempo)
            except:
                pass
                
        if tempos_requisicao:
            media = round(sum(tempos_requisicao) / len(tempos_requisicao), 2)
        else:
            media = 0.0
            
        print(f"    Resultado para {limite} vizinhos: {media} ms")
        tempos_medios.append(media)
        
    return tempos_medios

if __name__ == "__main__":
    usuario_teste = 1
    limites_vizinhos = [10, 20, 50, 100]
    
    url_postgres = f"http://127.0.0.1:8000/recomendar/colaborativo/postgres/{usuario_teste}"
    url_neo4j = f"http://127.0.0.1:8000/recomendar/colaborativo/neo4j/{usuario_teste}"
    
    print("Iniciando Teste de Volume e Complexidade de Varredura")
    
    try:
        requests.get(f"{url_postgres}?limite_vizinhos=10")
        requests.get(f"{url_neo4j}?limite_vizinhos=10")
    except:
        print("Erro: A API esta desligada")
        exit()
        
    medias_pg = testar_por_volume("PostgreSQL", url_postgres, limites_vizinhos)
    medias_neo = testar_por_volume("Neo4j", url_neo4j, limites_vizinhos)
    
    print("\nConstruindo o terceiro grafico de analise")
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(limites_vizinhos, medias_pg, marker='o', label='PostgreSQL', color='#336699', linewidth=2.5)
    plt.plot(limites_vizinhos, medias_neo, marker='s', label='Neo4j', color='#45b597', linewidth=2.5)
    
    for x, y in zip(limites_vizinhos, medias_pg):
        plt.text(x, y + 50, f"{y}ms", ha='center', va='bottom', color='#336699', fontweight='bold')
    for x, y in zip(limites_vizinhos, medias_neo):
        plt.text(x, y - 100, f"{y}ms", ha='center', va='top', color='#45b597', fontweight='bold')
        
    plt.title('Complexidade: Tempo de Resposta vs Volume de Vizinhos Varridos', fontsize=14, fontweight='bold')
    plt.xlabel('Volume de Vizinhos Considerados no Algoritmo (Limite)', fontsize=12)
    plt.ylabel('Tempo Medio de Resposta (ms)', fontsize=12)
    plt.xticks(limites_vizinhos)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    
    nome_arquivo = 'grafico_volume.png'
    plt.savefig(nome_arquivo, bbox_inches='tight')
    print(f"\nSucesso! Terceiro grafico salvo como '{nome_arquivo}'!")