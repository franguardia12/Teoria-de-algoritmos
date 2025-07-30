import pulp
from pulp import PULP_CBC_CMD
from collections import deque
import networkx as nx
import time


IMPRIMIR = False

def calcular_distancias_bfs(grafo, origen):
    cola    = deque([origen])
    visitado= {origen}
    dist    = {origen: 0}
    while cola:
        v = cola.popleft()
        for w in grafo.neighbors(v):
            if w not in visitado:
                visitado.add(w)
                dist[w] = dist[v] + 1
                cola.append(w)
    return dist

def k_clustering_pl(grafo, k):
    V = list(grafo.nodes())
    n = len(V)
    dist = {i: calcular_distancias_bfs(grafo, V[i]) for i in range(n)}

    M = max(dist[i][V[j]] 
            for i in range(n) 
            for j in range(n) 
            if V[j] in dist[i])

    prob = pulp.LpProblem("Min_K_Clustering", pulp.LpMinimize)

    x = {(i,c): pulp.LpVariable(f"x_{i}_{c}", cat="Binary")
         for i in range(n) for c in range(k)}
    D = pulp.LpVariable("D", lowBound=0, cat="Integer")


    for i in range(n):
        prob += pulp.lpSum(x[i,c] for c in range(k)) == 1


    for i in range(n):
        for j in range(i+1, n):
            d_ij = dist[i].get(V[j], M) 
            for c in range(k):
                prob += D >= d_ij - M*(2 - x[i,c] - x[j,c])

    prob += D

    prob.solve(PULP_CBC_CMD(msg=IMPRIMIR))

    D_opt = int(pulp.value(D))
    clusters = [[] for _ in range(k)]
    for i in range(n):
        for c in range(k):
            if pulp.value(x[i,c]) > 0.5:
                clusters[c].append(V[i])

   
    return D_opt, clusters
