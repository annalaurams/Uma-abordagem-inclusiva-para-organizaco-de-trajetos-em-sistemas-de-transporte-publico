import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import sys


v_acess = pd.read_csv("arquivos/Vertices.csv", delimiter=",") # Lê o arquivo

# Classe que salva as informações do nó

class Estacao:
    def __init__(self, cor, id, estacao):
        self.cor = cor
        self.id = id
        self.estacao = estacao

mapa = {} # salva todos os vértices, a chave é o nome da estação

for index, row in v_acess.iterrows(): # Percorre o arquivo e salva as informações de cada estação
    cor = row["Cor"]
    id = row["Id"]
    estacao = row["Estacao"]
    mapa[estacao] = Estacao(cor, id, estacao)

def imprimir_mapa(mapa):
        for estacao, info in mapa.items():
            print(f"Estacao: {estacao}")
            print(f"Cor: {info.cor}")
            print(f"ID: {info.id}")

#imprimir_mapa(mapa)

arestas_df = pd.read_csv("arquivos/Arestas.csv", delimiter=",")

arestas = []

for index, row in arestas_df.iterrows(): # Percorre o arquivo e salva as conexões na lista de arestas
    origem = row["Origem"]
    destino = row["Destino"]
    tempo = row["Tempo"]
    arestas.append((origem, destino, tempo))

grafo = {}

for origem, destino, tempo in arestas: # Insere no grafo as conexões
    if origem not in grafo:
        grafo[origem] = []
    grafo[origem].append((destino, tempo))



# Algoritmo de Dijkstra

trajeto = []

class Dijkstra:  
    def __init__(self, graph): # O construtor da classe recebe o grafo como parâmetro e o armazena como um atributo
        self.graph = graph

    def minimum_distance(self, distances, visited):  #Encontra a estação não visitada com a menor distância, a partir da origem
        min_distance = sys.maxsize
        min_station = None

        for station in distances:
            if not visited[station] and distances[station] <= min_distance:
                min_distance = distances[station]
                min_station = station

        return min_station

    def print_path(self, distances, parent, source, destination): # Imprimi o caminho
        print(f"        Caminho mínimo entre {source} e {destination}\n")

        crawl = destination
        path = []

        while parent[crawl] is not None:
            path.append(crawl)
            crawl = parent[crawl]

        path.append(source)
        path = path[::-1]  # Inverter a ordem para imprimir da origem ao destino

        # Crie uma lista para armazenar as estações no caminho
        estacoes = []

        for station in path:
            estacoes.append(station)

        # Imprima as estações uma embaixo da outra
        for estacao in estacoes:
            print(estacao)

        print(f"\nTempo total: {distances[destination]}", " minutos.")

    def dijkstra(self, source, destination):
        distances = {station: sys.maxsize for station in self.graph} #  Dicionário que armazena as distâncias mínimas conhecidas a partir da estação de origem
        visited = {station: False for station in self.graph} # Rastreia se uma estação foi visitada, inicialmente, todas são marcadas como não visitadas (False)
        parent = {station: None for station in self.graph} # Nó pai de cada estação
        distances[source] = 0

        while True: 
            u = self.minimum_distance(distances, visited)
            if u is None or u == destination:  # # não há mais nós não visitados alcançáveis a partir da estação de origem e chegamos à estação de destino
                break

            visited[u] = True

            if u == destination:
                break
            if u in self.graph:

                for v, weight in self.graph[u]: # weight representa o peso associado à aresta que conecta u a v.

                #  Esta condição abaixo verifica se a estação vizinha v não foi visitada, se a distância de u até v é menor e se distances[u] não é infinito 

                    if not visited[v] and distances[u] != sys.maxsize and distances[u] + weight < distances[v]: 
                          distances[v] = distances[u] + weight
                          parent[v] = u

                    else:
                        continue

        self.print_path(distances, parent, source, destination)


if __name__ == "__main__":

  input = pd.read_csv("arquivos/input.csv", delimiter=",")

  for index, row in input.iterrows():

      saida = ""
      chegada = ""

      saida = row["Saída"]
      chegada = row["Chegada"]

      source_station = saida
      destination_station = chegada

      if saida == chegada:
        print("Origem igual ao destino, o tempo de desocamento é zero")

      else:

        dijkstra = Dijkstra(grafo)
        dijkstra.dijkstra(source_station, destination_station)

        print("--------------------------------------------------------------------------------------------------------------------------------------------\n")

# Imprimi os vértices e arestas de uma única estação, baseada na cor ou jóia da linha

def print_graph(mapa, grafo):
    G = nx.DiGraph()

    nodes = [estacao for estacao, info in mapa.items() if info.cor == "Amarela"]
    G.add_nodes_from(nodes)

    edges = [(origem, destino) for origem, destinos in grafo.items() if origem in nodes
                  for destino, _ in destinos if destino in nodes]
    G.add_edges_from(edges)

    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='yellow', font_color='black', edge_color='lightblue',
            node_size=1500, width=5.0, font_size=8) 

    plt.show()

print_graph(mapa, grafo)



def desenhar_grafo(grafo, mapa, largura_aresta=1.0, layout='spring_layout', constante_mola=1.0):
    G = nx.Graph()

    for estacao, info in mapa.items():
        G.add_node(estacao, color="lightblue", id=info.id) 

    for origem, destinos in grafo.items():
        for destino, tempo in destinos:
            G.add_edge(origem, destino, tempo=tempo)

    if layout == 'spring_layout':
        pos = nx.spring_layout(G, k=constante_mola)
    else:
        pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(20, 15))

    nx.draw(G, pos, with_labels=True, font_color='black', font_size=8, node_size=1200, width=largura_aresta, node_color="lightblue")  # Modificado para cor lightblue

    edge_labels = {(origem, destino): f"{tempo}" for origem, destinos in grafo.items() for destino, tempo in destinos}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=6)

    plt.show()


#desenhar_grafo(grafo, mapa, largura_aresta=3.0, layout='spring_layout', constante_mola=0.2)
