import networkx as nx
import sys
import os

COMA = ","

def main():
    verificar_argumentos()
    grafo = generar_grafo(sys.argv[1])
    K = int(sys.argv[2])
    mapeo = louvain_algo(grafo, K)
    clusters = {}
    for nodo, com in mapeo.items():
        clusters.setdefault(com, []).append(nodo)
    for idx, nodos in enumerate(clusters.values(), start=1):
        nodos_ordenados = sorted(nodos)
        print(f"Cluster {idx} = {nodos_ordenados}")
    distancia_maxima = calcular_distancia_maxima(grafo, clusters)
    print(f"Distancia maxima = {distancia_maxima}")
    
def verificar_argumentos():
    if len(sys.argv) != 3:
        raise ValueError(
            "Uso esperado: python3 tp3.py ruta/a/grafo.txt <K>"
        )
    path = sys.argv[1]
    if not os.path.exists(path):
        raise ValueError("El archivo ingresado no existe")
    if not path.endswith('.txt'):
        raise ValueError("El archivo ingresado no es un .txt")

def generar_grafo(path_grafo):
    G = nx.Graph()
    with open(path_grafo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if COMA not in linea:
                raise SyntaxError(
                    "Cada línea debe contener nodos separados por coma"
                )
            u, v = linea.split(COMA)
            G.add_edge(u.strip(), v.strip())
    return G

def calcular_modularidad(grafo, asignacion_comunidades):
    m = grafo.size(weight='weight')
    
    grado = {n: grafo.degree(n, weight='weight') for n in grafo.nodes()}
    acumulado = 0.0

    for i in grafo.nodes():
        for j, datos in grafo[i].items():
            peso_ij = datos.get('weight', 1.0)
            if asignacion_comunidades[i] == asignacion_comunidades[j]:
                acumulado += peso_ij - (grado[i] * grado[j]) / (2.0 * m)

    return acumulado / (2.0 * m)

def calcular_delta_modularidad(grafo, nodo, comunidad_destino, asignacion_comunidades):
    m = grafo.size(weight='weight')
    k_i = grafo.degree(nodo, weight='weight')

    # k_i,in: peso de aristas entre nodo y miembros de comunidad_destino
    k_i_in = sum(
        datos.get('weight', 1.0)
        for vecino, datos in grafo[nodo].items()
        if asignacion_comunidades.get(vecino) == comunidad_destino
    )

    # suma de grados de todos los nodos en comunidad_destino
    suma_tot = sum(
        grafo.degree(n, weight='weight')
        for n, com in asignacion_comunidades.items()
        if com == comunidad_destino
    )

    # peso de aristas internas de comunidad_destino
    miembros = [n for n, com in asignacion_comunidades.items() if com == comunidad_destino]
    subgrafo = grafo.subgraph(miembros)
    suma_in = subgrafo.size(weight='weight')

    # delta Q -> Formula de diapositivas "06 - Comunidades"
    parte1 = (suma_in + k_i_in) / (2.0 * m) - ((suma_tot + k_i) / (2.0 * m))**2
    parte2 = suma_in / (2.0 * m) - (suma_tot / (2.0 * m))**2 - (k_i / (2.0 * m))**2
    return parte1 - parte2

def primera_fase(grafo):
    # cada nodo en su propia comunidad
    asignacion = {n: n for n in grafo.nodes()}
    hubo_mejora = True

    while hubo_mejora:
        hubo_mejora = False
        for nodo in grafo.nodes():
            comunidad_original = asignacion[nodo]
            # retirar nodo
            asignacion[nodo] = None

            # comunidades candidatas
            comunidades_vecinas = {
                asignacion[vecino]
                for vecino in grafo[nodo]
                if asignacion[vecino] is not None
            }
            candidatas = comunidades_vecinas.union({comunidad_original})

            mejor_delta = 0.0
            mejor_comunidad = comunidad_original

            # probar candidatas
            for com_cand in candidatas:
                asignacion[nodo] = com_cand
                delta_meter_nodo = calcular_delta_modularidad(grafo, nodo, com_cand, asignacion) # deltaQ(i -> com_cand)
                delta_sacar_nodo_comunidad_actual = -calcular_delta_modularidad(grafo, nodo, comunidad_original, asignacion) # deltaQ(D -> i) = -deltaQ(i -> D)
                if delta_meter_nodo + delta_sacar_nodo_comunidad_actual > mejor_delta:
                    mejor_delta = delta_meter_nodo + delta_sacar_nodo_comunidad_actual
                    mejor_comunidad = com_cand

            # asignar la mejor
            asignacion[nodo] = mejor_comunidad
            if mejor_comunidad != comunidad_original:
                hubo_mejora = True

    return asignacion

def segunda_fase(grafo, asignacion_comunidades):
    G2 = nx.Graph()
    comunidades = set(asignacion_comunidades.values())
    G2.add_nodes_from(comunidades)

    for u, v, datos in grafo.edges(data=True):
        peso = datos.get('weight', 1.0)
        cu = asignacion_comunidades[u]
        cv = asignacion_comunidades[v]
        if G2.has_edge(cu, cv):
            G2[cu][cv]['weight'] += peso
        else:
            G2.add_edge(cu, cv, weight=peso)

    return G2

def louvain_algo(grafo_original, K):
    grafo_actual = grafo_original.copy()
    mapeo_global = {n: n for n in grafo_original.nodes()}

    # Modularidad inicial 
    Q_prev = calcular_modularidad(grafo_original, mapeo_global)

    while True:
        asignacion = primera_fase(grafo_actual)

        nuevo_mapeo = {
            nodo_orig: asignacion[mapeo_global[nodo_orig]]
            for nodo_orig in mapeo_global
        }

        Q_new = calcular_modularidad(grafo_original, nuevo_mapeo)

        # Solo confirmamos el cambio si hay mejora
        if Q_new > Q_prev:
            mapeo_global = nuevo_mapeo
            Q_prev = Q_new
            grafo_actual = segunda_fase(grafo_actual, asignacion)
            if len(set(mapeo_global.values())) <= K:
                return mapeo_global
        else:
            # No hay ganancia
            break

    # Fusionamos si hay mas de K
    asign = mapeo_global.copy()
    while len(set(asign.values())) > K:
        Q_actual = calcular_modularidad(grafo_original, asign)
        mejor_ganancia = None
        mejor_asignacion = None

        comunidades = list(set(asign.values()))
        # pruebar todas las parejas de comunidades
        for i in range(len(comunidades)):
            for j in range(i+1, len(comunidades)):
                c1, c2 = comunidades[i], comunidades[j]
                # fusionar c2 en c1 temporalmente
                temp = {}
                for nodo, c in asign.items():
                    temp[nodo] = c1 if c == c2 else c
                Q_temp = calcular_modularidad(grafo_original, temp)
                gain = Q_temp - Q_actual
                if mejor_ganancia is None or gain > mejor_ganancia:
                    mejor_ganancia = gain
                    mejor_asignacion = temp
        asign = mejor_asignacion
    return asign

def calcular_distancia_maxima(grafo, clusters):
    diametros = []
    for nodos in clusters.values():
        diam_cluster = 0
        for u in nodos:
            distancias = nx.single_source_shortest_path_length(grafo, u)
            # Máxima distancia desde u a otros en su mismo cluster
            max_en_cluster = max(distancias[v] for v in nodos)
            diam_cluster = max(diam_cluster, max_en_cluster)
        diametros.append(diam_cluster)
    return max(diametros) if diametros else 0
