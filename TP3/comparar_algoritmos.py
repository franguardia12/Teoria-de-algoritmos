import networkx as nx
import numpy as np
from random import seed

from louvain import louvain_algo
from backtracking import k_clusters_backtracking
from util import generar_datos_muy_denso, generar_datos_intermedios, ejecutar_en_paralelo
from matplotlib import pyplot as plt
from tp3 import generar_grafo


def diametro_maximo_por_cluster(grafo, clusters):
    """
    clusters: lista de listas de nodos
    """
    max_diam = 0
    for grupo in clusters:
        if len(grupo) < 2:
            continue
        subgrafo = grafo.subgraph(grupo)
        if nx.is_connected(subgrafo):
            diam = nx.diameter(subgrafo)
        else:
            diam = max(nx.diameter(c) for c in nx.connected_components(subgrafo) if len(c) > 1)
        max_diam = max(max_diam, diam)
    return max_diam


def comparar_algoritmos():
    rutas_grafos = [
        "10_3.txt",
        "22_3.txt",
        "22_5.txt",
        "30_3.txt",
        "30_5.txt",
        "40_5.txt",
        "45_3.txt"
        #"50_3.txt"
    ]
    
    parametros = []
    nodos = []
    razones = []
    distancias_bt = []
    distancias_lv = []

    for ruta in rutas_grafos:
        grafo = generar_grafo("./tests/" + ruta)
        inicio = ruta.find("_") + 1
        fin = ruta.find(".txt")
        k = int(ruta[inicio: fin])
        parametros.append((grafo, k))
        nodos.append(grafo.number_of_nodes())

    # Ejecutar ambos algoritmos en paralelo
    resultados_bt = ejecutar_en_paralelo(k_clusters_backtracking, parametros)
    resultados_lv = ejecutar_en_paralelo(louvain_algo, parametros)

    for i, (tiempo_bt, resultado_bt) in enumerate(resultados_bt):
        if resultado_bt is None:
            razones.append(np.nan)
            continue

        _, distancia_bt = resultado_bt
        tiempo_lv, resultado_lv = resultados_lv[i]
        grafo, _ = parametros[i]

        # Convertir el mapeo de Louvain a clusters
        clusters_lv = {}
        for nodo, com in resultado_lv.items():
            clusters_lv.setdefault(com, []).append(nodo)


        distancia_lv = diametro_maximo_por_cluster(grafo, list(clusters_lv.values()))
        ratio = distancia_lv / distancia_bt if distancia_bt > 0 else float("inf")
        razones.append(ratio)

        distancias_bt.append(distancia_bt)
        distancias_lv.append(distancia_lv)

        print(f"n={nodos[i]}, tiempo_bt={tiempo_bt:.2f}s, distancia_bt={distancia_bt}, tiempo_lv={tiempo_lv:.2f}s, distancia_lv={distancia_lv}, ratio={ratio:.2f}")

    
    # graficar
    plt.plot(nodos, distancias_bt, marker='o', label="Backtracking", color='blue')
    plt.plot(nodos, distancias_lv, marker='s', label="Louvain", color='orange')

    plt.xlabel("Cantidad de nodos")
    plt.ylabel("Diámetro máximo por cluster")
    plt.title("Comparación de calidad: Louvain vs Backtracking")
    plt.legend()
    plt.grid(True)
    plt.show()

comparar_algoritmos()
