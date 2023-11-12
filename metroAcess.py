import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

v_acess = pd.read_csv("arquivos/VerticeAcess.csv", delimiter=",")

# Classe que salva as informações dos vértices 

class Estacao2:
    def __init__(self, cor, id, estacao, elevador, rampa, piso):
        self.cor = cor
        self.id = id
        self.estacao = estacao
        self.elevador = elevador
        self.rampa = rampa
        self.piso = piso

vertices2 = []

mapa = {}

for index, row in v_acess.iterrows():
    cor = row["Cor"]
    id = row["Id"]
    estacao = row["Estacao"]
    elevador = row["Elevador"]
    rampa = row["Rampa"]
    piso = row["Piso Tátil"]

    mapa[estacao] = Estacao2(cor, id, estacao, elevador, rampa, piso)

def imprimir_mapa(mapa):
        for estacao, info in mapa.items():
            print(f"Estacao: {estacao}")
            print(f"Cor: {info.cor}")
            print(f"ID: {info.id}")
            print(f"Elevador: {info.elevador}")
            print(f"Rampa: {info.rampa}")
            print(f"Piso Tátil: {info.piso}")

#imprimir_mapa(mapa)


arestas_df = pd.read_csv("arquivos/Arestas.csv", delimiter=",")
arestas = []

for index, row in arestas_df.iterrows(): # Percorre o arquivo e salva as conexões na lista de arestas
    origem = row["Origem"]
    destino = row["Destino"]
    tempo = row["Tempo"]

    if destino in mapa: # Para cada destino que se deseja chegar: 
        estacao_destino = mapa[destino]
        elevador = estacao_destino.elevador
        rampa = estacao_destino.rampa
        piso_tatil = estacao_destino.piso

        # A aresta recebe um peso (tempo) adicional

        if elevador == 1:  # Se tiver elevador na estação
            tempo = tempo * 1
        elif rampa == 1:  # Se tiver rampa na estação
            tempo = tempo * 3
        elif piso_tatil == 1:   # Se tiver piso tátil na estação
            tempo = tempo * 2

    arestas.append((origem, destino, tempo))

grafo = {}

for origem, destino, tempo in arestas:
    if origem not in grafo:
        grafo[origem] = []
    grafo[origem].append((destino, tempo))

#print(grafo)


trajeto2 = []

contador = 0

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def minimum_distance(self, distances, visited):
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

        estacoes = []

        for station in path:
            estacoes.append(station)

        for estacao in estacoes:
            print(estacao)

        if destination not in path:
            print("\nNão há caminho direto possível.")

        elif distances[destination] < 2000:
            print(f"\nTempo total: {distances[destination]}", " minutos.")

        #dijkstra.print_edge_weights(parent, source_station, destination_station)

    def print_edge_weights(self, parent, source, destination):

        #print(f"Peso das arestas no caminho mínimo entre {source} e {destination}:")

        crawl = destination

        while parent[crawl] is not None:
            parent_station = parent[crawl]
            for neighbor, weight in self.graph[parent_station]:
                if neighbor == crawl:
                    print(f"{parent_station} -> {crawl}: {weight}")
            crawl = parent_station


    def dijkstra(self, source, destination, com_elevador:bool, com_rampa:bool, com_piso:bool):

        if source not in self.graph or destination not in self.graph:
          print("Estação de origem ou destino inválida.")
          return

        distances = {station: sys.maxsize for station in self.graph}
        visited = {station: False for station in self.graph}
        parent = {station: None for station in self.graph}
        distances[source] = 0

        while True:
            u = self.minimum_distance(distances, visited)
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

                        # Casos envolvendo a presença ou ausência de elevador, rampa e piso tpatil

                        if (com_elevador and mapa[v].elevador == 1) and not com_rampa and not com_piso:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("111  ",parent[v], "  ")

                        elif (com_rampa and mapa[v].rampa == 1) and not com_elevador and not com_piso:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("222",parent[v], "  ")

                        elif (com_piso and mapa[v].piso == 1) and not com_elevador and not com_rampa:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("333",parent[v], "  ")

                        elif (com_elevador and mapa[v].elevador == 1) and (com_rampa and mapa[v].rampa == 1) and not com_piso:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("444",parent[v], "  ")

                        elif (com_elevador and mapa[v].elevador == 1) and (com_piso and mapa[v].piso == 1) and not com_rampa:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("555",parent[v], "  ")

                        elif (com_piso and mapa[v].piso == 1) and (com_rampa and mapa[v].rampa == 1) and not com_elevador:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("666",parent[v], "  ")

                        elif (com_elevador and mapa[v].elevador == 1) and (com_rampa and mapa[v].rampa == 1) and (com_piso and mapa[v].piso == 1):
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("777",parent[v], "  ")

                        elif not com_elevador and not com_rampa and not com_piso:
                          distances[v] = distances[u] + weight
                          parent[v] = u
                          #print("888",parent[v], "  ")

                    else:
                        continue

        self.print_path(distances, parent, source, destination)


if __name__ == "__main__":

    input_acess = pd.read_csv("arquivos/inputAcess.csv", delimiter=",")

    vertices2 = []
    e =  0
    p = 0
    r = 0
    
    saida = ""
    chegada = " "

    # Váriaveis que indicam que o indivíduo não precisa ter o elemento na estação

    com_elevador = 0
    com_rampa = 0
    com_piso = 0


    #mapa = {}

    for index, row in input_acess.iterrows():

        saida = row["Saída"]
        chegada = row["Chegada"]
        e = row["E"]
        r = row["R"]
        p = row["P"]


        if saida not in mapa:
            print(f"Estação de saída não encontrada")
            
        if chegada not in mapa:
            print(f"Estação de chegada não encontrada.")

        if saida == chegada:
            print("Origem igual ao destino, o tempo de desocamento é zero")

        else:
            source_station = saida
            destination_station = chegada

            dijkstra = Dijkstra(grafo)
            dijkstra.dijkstra(source_station, destination_station, e, r, p)

          

            print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")



