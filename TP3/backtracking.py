import math
import networkx as nx

def obtener_todas_las_distancias_minimas(grafo, nodos=None):
    """
    Devuelve una lista de nodos, diccionario que mapea el indice de un nodo en la lista, y
    una matriz dist[i][j] con la distancia mínima entre nodo i y j
    """
    if nodos is None:
        nodos = list(grafo.nodes())

    n = len(nodos)
    indices = {}
    for i, nodo in enumerate(nodos):
        indices[nodo] = i

    dist = [[math.inf]*n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, d in nx.all_pairs_shortest_path_length(grafo):
        if u not in indices:
            continue
        ui = indices[u]
        for v, dv in d.items():
            if v in indices:
                dist[ui][indices[v]] = dv

    return nodos, indices, dist

def k_clusters_backtracking(grafo: nx.Graph, k: int):
    """
    Dado un grafo no dirigido y no pesado y un valor K, determina los 
    K clusters para que la distancia máxima de cada cluster sea mínima.
    Devuelve una lista con los clusters y la distancia máxima.
    """

    orden = sorted(grafo.nodes(), key=lambda u: grafo.degree(u), reverse=True)
    # Este orden sirve para poner los nodos de mayor grado primero (optimizacion)

    nodos, indices, dist = obtener_todas_las_distancias_minimas(grafo, orden)

    clusters = [[] for _ in range(k)]
    mejor_solucion = {
        "clusters": None,
        "distancia_maxima": float('inf')
    }

    _k_clusters_backtracking(grafo, nodos, dist, k, clusters, 0, 0, mejor_solucion)

    if mejor_solucion["clusters"] is None:
        return None

    resultado = [
        [nodos[i] for i in lista_indices_resultado]
        for lista_indices_resultado in mejor_solucion["clusters"]
    ]

    return resultado, mejor_solucion["distancia_maxima"]


def _k_clusters_backtracking(grafo: nx.Graph, nodos: list, dist: list, k: int, clusters: list, indice: int, dist_actual: float, mejor_solucion: dict):
    if dist_actual >= mejor_solucion["distancia_maxima"]:
        return
    
    if indice == len(nodos):
        if any(len(c) == 0 for c in clusters):
            return
        
        for c in clusters:
            sub = grafo.subgraph(nodos[i] for i in c)
            if not nx.is_connected(sub):
                return
        
        diametro = 0
        for c in clusters:
            for i in range(len(c)):
                for j in range(i+1, len(c)):
                    diametro = max(diametro, dist[c[i]][c[j]])
        
        if diametro < mejor_solucion["distancia_maxima"]:
            mejor_solucion["distancia_maxima"] = diametro
            mejor_solucion["clusters"] = [list(c) for c in clusters]
        return

    
    indice_u = indice

    for i in range(k):
        if not clusters[i] and any(not clusters[j] for j in range(i)):
            continue

        clusters[i].append(indice_u)

        if len(clusters[i]) == 1:
            diam_i = 0
        else:
            diam_i = max(dist[indice_u][indice_v] for indice_v in clusters[i])

        nuevo_diam = max(dist_actual, diam_i)

        if nuevo_diam < mejor_solucion["distancia_maxima"]:
            _k_clusters_backtracking(
                grafo, nodos, dist, k,
                clusters, indice+1, nuevo_diam,
                mejor_solucion
            )

        clusters[i].pop()


