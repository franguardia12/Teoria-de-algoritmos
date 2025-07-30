from collections import deque

def calcular_distancias_bfs(grafo, origen):
    cola = deque()
    visitados = set()
    dist = {}
    cola.append(origen)
    visitados.add(origen)
    for v in grafo.nodes():
        dist[v] = 0

    while not len(cola) == 0:
        v = cola.pop()
        for w in grafo.neighbors(v):
            if w not in visitados:
                cola.appendleft(w)
                dist[w] = dist[v] + 1
                visitados.add(w)

    return dist



def validar_solucion_clustering(grafo, K, C, solucion):
    if len(solucion) > K:
        return False
    
    vertices = grafo.nodes() 
    cubiertos = set()

    for cluster in solucion:
        for v in cluster:
            if v not in vertices:
                return False
            
            if v in cubiertos:
                return False #hay un vértice en dos clusters
            else:
                cubiertos.add(v)
            
            distancia = calcular_distancias_bfs(grafo, v)
            for w in cluster:
                if v == w:
                    continue

                if w not in vertices:
                    return False
                
                if distancia[w] > C:
                    return False
                
    if len(cubiertos) != len(vertices):
        return False

    return True
