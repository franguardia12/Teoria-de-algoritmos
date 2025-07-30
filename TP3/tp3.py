import sys
import os
import networkx as nx
from louvain import *
from backtracking import *
from programacion_lineal import *

COMA = ","

def main():
    verificar_argumentos()
    grafo = generar_grafo(sys.argv[1])
    k = int(sys.argv[2])
    print("Ingrese el algoritmo a utilizar: \n1. Programación Lineal\n2. Backtracking\n3. Louvain")
    algoritmo_valido = False
    while not algoritmo_valido:
        try:
            opcion = int(input("Ingrese una opción (1, 2 o 3): "))
            if opcion == 1:
                algoritmo_valido = True
            elif opcion == 2:
                algoritmo_valido = True
            elif opcion == 3:
                algoritmo_valido = True
            else:
                print("Opción no válida. Por favor, elija entre 1, 2 o 3.")
        except ValueError:
            print("Entrada no válida. Debe ingresar un número entero.")
    if opcion == 1:
        print("Ejecutando Programación Lineal...")
        distancia, clusters = k_clustering_pl(grafo, k)
    elif opcion == 2:
        print("Ejecutando Backtracking...")
        clusters, distancia = k_clusters_backtracking(grafo, k)
    else:
        print("Ejecutando Louvain...")
        particiones = louvain_algo(grafo, k)
        clusters = {}
        for nodo, com in particiones.items():
            clusters.setdefault(com, []).append(nodo)
        for idx, nodos in enumerate(clusters.values(), start=1):
            nodos_ordenados = sorted(nodos)
            print(f"Cluster {idx} = {nodos_ordenados}")
        distancia_maxima = calcular_distancia_maxima(grafo, clusters)
        print(f"Distancia maxima = {distancia_maxima}")
        return
    for indice, cluster in enumerate(clusters, start=1):
        nodos_ordenados = sorted(cluster)
        print(f"Cluster {indice} = {nodos_ordenados}")
    print(f"Distancia maxima = {distancia}")

def verificar_argumentos():
    if len(sys.argv) != 3:
        raise ValueError("La cantidad de argumentos ingresados no es válida - Expected: python3 tp3.py ruta/a/grafo.txt <K>")
    path_grafo = sys.argv[1]
    if not os.path.exists(path_grafo):
        raise ValueError("El archivo ingresado no existe. Verificar formato correcto: 'grafos/nombre_grafo.txt'")
    if not path_grafo.endswith(".txt"):
        raise ValueError("El archivo ingresado no es un archivo de texto")
    try:
        k = int(sys.argv[2])
        if k <= 0:
            raise ValueError("El valor de K debe ser un entero positivo")
    except ValueError:
        raise ValueError("El segundo argumento debe ser un número entero positivo que representa K")

def generar_grafo(path_grafo):
    """
    Genera un grafo a partir de un archivo de texto donde cada línea contiene dos nodos separados por una coma, representando una arista entre ellos.
    """
    grafo = nx.Graph()
    with open(path_grafo, 'r') as archivo:
        for linea in archivo:
            if linea.strip():
                if COMA not in linea:
                    raise SyntaxError("Cada línea debe contener una coma para separar los nodos")
                nodos = linea.strip().split(COMA)
                if len(nodos) == 2 and nodos[0] and nodos[1]:
                    grafo.add_edge(nodos[0], nodos[1])
                else:
                    raise SyntaxError("Cada línea debe contener exactamente dos nodos")
    return grafo

main()