import pandas as pd
import networkx as nx
import csv
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
import heapq
import time

start_time = time.time()

v_acess = pd.read_csv("arquivos/Vertices.csv", delimiter=",")

# Classe que salva as informações dos vértices

class Estacao:
    def __init__(self, cor, id, estacao, elevador, rampa):
        self.cor = cor
        self.id = id
        self.estacao = estacao
        self.elevador = elevador
        self.rampa = rampa

mapa = {}

for index, row in v_acess.iterrows():
    cor = row["Cor"]
    id = row["Id"]
    estacao = row["Estacao"]
    elevador = row["Elevador"]
    rampa = row["Rampa"]

    mapa[estacao] = Estacao(cor, id, estacao, elevador, rampa)

def imprimir_mapa(mapa):
        for estacao, info in mapa.items():
            print(f"Estacao: {estacao}")
            print(f"Cor: {info.cor}")
            print(f"ID: {info.id}")
            print(f"Elevador: {info.elevador}")
            print(f"Rampa: {info.rampa}")

#imprimir_mapa(mapa)

arestas = []
grafo = {}
arestas2 = []
grafoAux = {}

def Grafo1(): #grafo principal

    arestas_df = pd.read_csv("arquivos/Arestas.csv", delimiter=",")

    for index, row in arestas_df.iterrows(): # Percorre o arquivo e salva as conexões na lista de arestas
        origem = row["Origem"]
        destino = row["Destino"]
        tempo = row["Tempo"]
        arestas.append((origem, destino, tempo))

    for origem, destino, tempo in arestas:
        if origem not in grafo:
            grafo[origem] = []
        grafo[origem].append((destino, tempo))

Grafo1()

def Grafo2(): # grafo auxiliar, contém acessibilidade

    arestas_df = pd.read_csv("arquivos/Arestas.csv", delimiter=",")

    for index, row in arestas_df.iterrows(): # Percorre o arquivo e salva as conexões na lista de arestas
        origem = row["Origem"]
        destino = row["Destino"]
        tempo = row["Tempo"]

        if destino in mapa: # Para cada destino que se deseja chegar:
            estacao_destino = mapa[destino]
            elevador = estacao_destino.elevador
            rampa = estacao_destino.rampa

            if elevador == 1 and rampa == 1:  # Se tiver elevador e rampa na estação
                tempo = tempo * 2.5
            elif rampa == 1:  # Se tiver rampa na estação
                tempo = tempo * 3
            elif elevador == 1:   # Se tiver elevador tátil na estação
                tempo = tempo * 2

        arestas2.append((origem, destino, tempo))

    for origem, destino, tempo in arestas2:
        if origem not in grafoAux:
            grafoAux[origem] = []
        grafoAux[origem].append((destino, tempo))

Grafo2()


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        
    def print_path(self, distances, parent, source, destination): # Imprimi o caminho

            print(f"        Caminho mínimo entre {source} e {destination}\n")

            crawl = destination
            path = []

            while parent[crawl] is not None:
                path.append(crawl)
                crawl = parent[crawl]

            path.append(source)
            path = path[::-1]  # Inverter a ordem para imprimir da origem ao destino

            estacoes = []

            for station in path:
                estacoes.append(station)

            for estacao in estacoes:
                print(estacao)

            if destination not in path:
                print("\nNão há caminho direto possível.")

            elif distances[destination] < 2000:
                print(f"\nTempo total: {distances[destination]}", " minutos.")

    def dijkstra1(self, source, destination):

        distances = {station: sys.maxsize for station in self.graph}
        visited = {station: False for station in self.graph}
        parent = {station: None for station in self.graph}
        distances[source] = 0

        pq = [(0, source)]  # Fila prioritária inicializada com a origem e distância zero

        while pq:
            min_distance, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            if u == destination:
                break

            if u in self.graph:
                for v, weight in self.graph[u]:
                    if not visited[v] and distances[u] != sys.maxsize and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        parent[v] = u
                        heapq.heappush(pq, (distances[v], v))

        self.print_path(distances, parent, source, destination)

    def dijkstra2(self, source, destination, com_elevador:bool, com_rampa:bool):

        if source not in self.graph or destination not in self.graph:
          print("Estação de origem ou destino inválida.")
          return

        distances = {station: sys.maxsize for station in self.graph}
        visited = {station: False for station in self.graph}
        parent = {station: None for station in self.graph}
        distances[source] = 0

        pq = [(0, source)]

        while pq: # enquanto a fila não estiver fazia
            min_distance, u = heapq.heappop(pq)
            if u is None:
                break

            visited[u] = True

            if u == destination:
                break
            if u in self.graph:

                for v, weight in self.graph[u]:

                    if v not in mapa:
                        continue

                    elif v in visited and v in distances and not visited[v] and distances[u] != sys.maxsize and distances[u] + weight < distances[v]:

                        # Casos envolvendo a presença ou ausência de elevador e rampa

                        if (com_elevador and mapa[v].elevador == 1) and not com_rampa:
                          distances[v] = distances[u] + weight
                          parent[v] = u

                        elif (com_rampa and mapa[v].rampa == 1) and not com_elevador:
                          distances[v] = distances[u] + weight
                          parent[v] = u

                        elif (com_elevador and mapa[v].elevador == 1) and (com_rampa and mapa[v].rampa == 1):
                          distances[v] = distances[u] + weight
                          parent[v] = u


                        heapq.heappush(pq, (distances[v], v))

                    else:
                        continue

        self.print_path(distances, parent, source, destination)
        
input_acess = pd.read_csv("arquivos/inputAcess.csv", delimiter=",")

e = 0
r = 0

saida = ""
chegada = " "

com_elevador = 0
com_rampa = 0

for index, row in input_acess.iterrows():

    saida = row["Saída"]
    chegada = row["Chegada"]
    e = row["E"]
    r = row["R"]

    if saida not in mapa:
        print(f"Estação de saída não encontrada")

    elif chegada not in mapa:
        print(f"Estação de chegada não encontrada.")

    elif saida == chegada:
        print("Origem igual ao destino, o tempo de desocamento é zero")

    else:

      source_station = saida
      destination_station = chegada

      if(e == 0 and r == 0):

        dijkstra1 = Dijkstra(grafo)
        dijkstra1.dijkstra1(source_station, destination_station)

      else:

        dijkstra2 = Dijkstra(grafoAux)
        dijkstra2.dijkstra2(source_station, destination_station, e, r)


      print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

end_time = time.time()
execution_time = (end_time - start_time) * 1000  # Convertendo para milissegundos

print(f"Tempo de execução: {execution_time:.2f} milissegundos")