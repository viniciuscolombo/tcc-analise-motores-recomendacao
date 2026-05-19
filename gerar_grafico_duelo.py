import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def testar_motor(motor, url):
    print(f"\n[{motor}] Iniciando Duelo")
    
    print("Cold Start")
    try:
        res_frio = requests.get(url)
        tempo_frio = res_frio.json().get("tempo_execucao_ms", 0) if res_frio.status_code == 200 else 0
    except:
        tempo_frio = 0
        
    # Teste a Quente (Hot Start) - A memória já mapeou o caminho
    print("Hot Start")
    try:
        res_quente = requests.get(url)
        tempo_quente = res_quente.json().get("tempo_execucao_ms", 0) if res_quente.status_code == 200 else 0
    except:
        tempo_quente = 0
    
    print(f"Resultado {motor} | Frio: {tempo_frio} ms | Quente: {tempo_quente} ms")
    return tempo_frio, tempo_quente

if __name__ == "__main__":
    usuario_teste = 1
    url_postgres = f"http://127.0.0.1:8000/recomendar/colaborativo/postgres/{usuario_teste}"
    url_neo4j = f"http://127.0.0.1:8000/recomendar/colaborativo/neo4j/{usuario_teste}"
    
    pg_frio, pg_quente = testar_motor("PostgreSQL", url_postgres)
    neo_frio, neo_quente = testar_motor("Neo4j", url_neo4j)
    
    print("\nMontando o gráfico de comparação Frio vs Quente")
    
    labels = ['PostgreSQL', 'Neo4j']
    tempos_frio = [pg_frio, neo_frio]
    tempos_quente = [pg_quente, neo_quente]
    
    x = range(len(labels))
    largura = 0.35
    
    fig, ax = plt.subplots(figsize=(9, 6))
    
    barras_frio = ax.bar([pos - largura/2 for pos in x], tempos_frio, largura, label='Cold Start (1ª Requisição)', color='#1f77b4')
    barras_quente = ax.bar([pos + largura/2 for pos in x], tempos_quente, largura, label='Hot Start (Cache)', color='#ff7f0e')
    
    ax.set_ylabel('Tempo de Resposta em Milissegundos (ms)', fontsize=12)
    ax.set_title('Desempenho Relacional vs Grafos: Cold Start vs Hot Start', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
    ax.legend()
    
    for barra in barras_frio + barras_quente:
        altura = barra.get_height()
        ax.annotate(f'{altura} ms',
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')
                    
    plt.ylim(0, max(max(tempos_frio), max(tempos_quente)) * 1.2)
    plt.tight_layout()
    
    nome_arquivo = 'grafico_duelo.png'
    plt.savefig(nome_arquivo)
    print(f"Sucesso! Gráfico salvo como '{nome_arquivo}'!")