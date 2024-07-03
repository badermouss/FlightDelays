from datetime import datetime

import networkx as nx

from modello.model import Model


myModel = Model()
myModel.buildGraph(5)
myModel.printGraphDetails()

v0 = myModel.getAllNodes()[0]

connessa = list(nx.node_connected_component(myModel._grafo, v0))
v1 = connessa[10]

pathD = myModel.trovaCamminoDijkstra(v0, v1)
pathBFS = myModel.trovaCamminoBFS(v0, v1)
pathDFS = myModel.trovaCamminoDFS(v0, v1)

print("Metodo Dijsktra")
print(*pathD, sep="\n")
print("-"*10)
print("Metodo albero BFS")
print(*pathBFS, sep="\n")
print("-"*10)
print("Metodo albero DFS")
print(*pathDFS, sep="\n")

tic = datetime.now()
bestPath, bestScore = myModel.getCamminoOttimo(v0, v1, 3)
print("-"*10)
print(f"Cammino ottimo tra {v0} e {v1} ha peso: {bestScore} trovato in {datetime.now() - tic}")
print(*bestPath, sep="\n")


