from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os
import networkx as nx
import random

TAMANO_CLUSTER = 2

# Este parámetro controla cuantas veces se ejecuta el algoritmo para cada
# tamaño. Esto es conveniente para reducir el error estadístico en la medición
# de tiempos. Al finalizar las ejecuciones, se promedian los tiempos obtenidos
RUNS_PER_SIZE = 20

# Ajustar este valor si se quiere usar más de un proceso para medir los tiempos
# de ejecución, o None para usar todos los procesadores disponibles. Si se usan
# varios procesos, tener cuidado con el uso de memoria del sistema.
MAX_WORKERS = max(1, (os.cpu_count() or 0) - 2)

def _time_run(algorithm, args):
    start = time.time()
    algorithm(*args)
    return time.time() - start

def time_algorithm(algorithm, sizes, get_args):
    futures = {}
    total_times = {i: 0 for i in sizes}

    # Usa un ProcessPoolExecutor para ejecutar las mediciones en paralelo
    # (el ThreadPoolExecutor no sirve por el GIL de Python)
    with ProcessPoolExecutor(MAX_WORKERS) as p:
        for i in sizes:
            for _ in range(RUNS_PER_SIZE):
                futures[p.submit(_time_run, algorithm, get_args(i))] = i

        for f in as_completed(futures):
            result = f.result()
            i = futures[f]
            total_times[i] += result

    return {s: t / RUNS_PER_SIZE for s, t in total_times.items()}

def generar_datos_intermedios(k_clusters: int, n: int, p_intra=0.4, p_inter=0.1):
    """
    Genera un grafo con n nodos y k_clusters clusters, pero con más ruido:
    - p_intra: probabilidad de conectar nodos dentro del cluster (moderado)
    - p_inter: probabilidad de conectar nodos entre clusters (ruido)
    """
    grafo = nx.Graph()
    grafo.add_nodes_from(range(n))

    # Dividir nodos en k grupos aproximadamente iguales
    grupos = [[] for _ in range(k_clusters)]
    for i, nodo in enumerate(range(n)):
        grupos[i % k_clusters].append(nodo)

    # Conectar dentro de cada cluster con probabilidad p_intra (menos denso)
    for grupo in grupos:
        for i in grupo:
            for j in grupo:
                if i < j and random.random() < p_intra:
                    grafo.add_edge(i, j)

    # Conectar entre clusters con probabilidad p_inter (más ruido)
    for i in range(k_clusters):
        for j in range(i + 1, k_clusters):
            for nodo_i in grupos[i]:
                for nodo_j in grupos[j]:
                    if random.random() < p_inter:
                        grafo.add_edge(nodo_i, nodo_j)

    return grafo, k_clusters



def generar_datos_muy_denso(size :int, k_clusters :int) -> tuple:

	grafo = nx.Graph()
	grafo.add_nodes_from(range(size))

	cluster_size = TAMANO_CLUSTER
	num_clusters = size
	for c in range(size):
		start = c * cluster_size
		end = start + cluster_size
		cluster_nodes = list(range(start, min(end, size)))

		for i in cluster_nodes:
			for j in cluster_nodes:
				if i > j:
					grafo.add_edge(i, j)
	for c in range(num_clusters):
		grafo.add_edge(c * cluster_size, (c + 1) * cluster_size)
	return grafo, k_clusters


def _run_function(algorithm, args):
    start = time.time()
    result = algorithm(*args)
    elapsed = time.time() - start
    return elapsed, result

def ejecutar_en_paralelo(algorithm, lista_de_parametros):
    """
    Ejecuta en paralelo la función `algorithm` con cada conjunto de argumentos
    de `lista_de_parametros` (cada elemento es una tupla con los argumentos).

    Devuelve una lista de tuplas (tiempo_ejecucion, resultado) en el mismo orden.

    - algorithm: función a ejecutar
    - lista_de_parametros: lista de tuplas, cada una con los argumentos para algorithm
    """

    resultados = [None] * len(lista_de_parametros)
    with ProcessPoolExecutor(MAX_WORKERS) as executor:
        futuros = {executor.submit(_run_function, algorithm, args): idx for idx, args in enumerate(lista_de_parametros)}

        for futuro in as_completed(futuros):
            idx = futuros[futuro]
            tiempo, resultado = futuro.result()
            resultados[idx] = (tiempo, resultado)

    return resultados