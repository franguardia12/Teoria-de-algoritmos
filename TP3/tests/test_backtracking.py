import time
import sys, os
import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backtracking import k_clusters_backtracking, generar_grafo


# (archivo_grafos, k, distancia maxima esperada)
casos = [
    ("50_3.txt", 3, 3)
]

@pytest.mark.parametrize("path_grafo, k, distancia_esperada", casos)
def test_k_clusters_distancia_y_tiempo(path_grafo, k, distancia_esperada):
    ruta = os.path.join("tests", path_grafo)
    grafo = generar_grafo(ruta)

    inicio = time.perf_counter()
    clusters, distancia_obtenida = k_clusters_backtracking(grafo, k=k)
    duracion = time.perf_counter() - inicio
    assert distancia_obtenida == distancia_esperada, (
        f"{path_grafo} con k={k}: "
        f"esperada={distancia_esperada}, obtenida={distancia_obtenida} "
    )
    print(f"{path_grafo} | k={k} → distancia {distancia_obtenida}, tiempo {duracion:.3f}s")
    for cluster in clusters:
        print(f"  Cluster: {cluster}")
