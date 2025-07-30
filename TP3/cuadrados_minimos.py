# Imports necesarios para el notebook
import random
from random import seed
import networkx as nx

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from louvain import louvain_algo
from programacion_lineal import k_clustering_pl
from backtracking import k_clusters_backtracking
from util import time_algorithm, generar_datos_intermedios, generar_datos_muy_denso


# Siempre seteamos la seed de aleatoridad para que los resultados sean reproducibles
def cuadrados_minimos():
    seed(12345)
    np.random.seed(12345)

    sns.set_theme()
    x = np.linspace(1, 7, 7).astype(int)  # número de vértices
    vertices = 20  # valor fijo

    # Tiempos medidos
    results_pl = time_algorithm(k_clustering_pl, x, lambda n: generar_datos_muy_denso(vertices, n))
    tiempos_pl = np.array([results_pl[n] for n in x])

    # Ajuste: log(T(n)) = log(a) + n * log(b)
    log_tiempos = np.log(tiempos_pl)
    (m, c), _ = sp.optimize.curve_fit(lambda n, m, c: m * n + c, x, log_tiempos)

    a = np.exp(c)
    b = np.exp(m)

    # Gráfico
    fig, ax = plt.subplots()
    ax.plot(x, tiempos_pl, 'o-', label="Medición k_clustering_pl")
    #ax.plot(x, a * (b ** x), 'r--', label=f"Ajuste $O({k_clusters}^n)$")
    ax.plot(x, a * (b ** x), 'r--', label=f"Ajuste $O(K^{{{vertices}}})$")

    ax.set_title('Tiempo de ejecución de k_clustering_pl')
    ax.set_xlabel('Número de clusters (k)')
    ax.set_ylabel('Tiempo de ejecución (s)')
    ax.legend()
    plt.show()

    # Errores
    errores_pl = np.abs(a * (b ** x) - tiempos_pl)
    print(f"Error cuadrático total: {np.sum(errores_pl ** 2):.4f}")
    print(f"Ajuste estimado: T(n) ≈ {a:.4e} * {b:.4f}^n")

def generar_grafo(cantidad_nodos, k_clusters):
    semilla = 20
    extras = 5
    grafo = nx.random_tree(cantidad_nodos, semilla)
    posibles_aristas = list(nx.non_edges(grafo))
    random.shuffle(posibles_aristas)
    for i in range(min(extras, len(posibles_aristas))):
        u, v = posibles_aristas[i]
        grafo.add_edge(u, v)
    return grafo, k_clusters

cuadrados_minimos()