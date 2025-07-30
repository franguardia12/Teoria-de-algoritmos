import unittest
import os
import networkx as nx
from validador import validar_solucion_clustering

class TestValidadorClusteringBajoDiametro(unittest.TestCase):
    def test_casos_archivos(self):
        #Ruta de los archivos que contienen los casos de prueba
        carpeta_tests = 'tests_catedra'
        archivos = ['10_3.txt', '22_3.txt', '22_5.txt', '30_3.txt', '30_5.txt', '40_5.txt', '45_3.txt', '50_3.txt']
        casos = {
            '10_3.txt': [([[0, 1, 8, 4, 3, 5, 9], [6, 2, 7]], 2, 2), ([[0, 8], [1, 4, 9], [3, 5, 2, 7], [6]], 5, 1)],
            '22_3.txt': [([[0, 13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 6], [7, 10, 17, 15, 14]], 3, 2), ([[0, 13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 6], [7, 10, 17, 15, 14], []], 4, 2), ([[0, 13, 16], [4, 12, 19], [3, 2, 6], [1, 18, 9], [21, 5, 17], [8], [11, 10], [7, 15], [14], [20]], 10, 1)],
            '22_5.txt': [([[0, 16, 4, 8, 21, 1, 7, 20, 11, 14, 18, 5, 10, 17, 19, 2, 9, 15, 12, 13], [3, 6]], 2, 2), ([[0, 16, 21], [4, 10, 15], [8, 11, 2], [1, 20, 14, 17], [7, 19, 6], [18, 9, 12, 13], [5, 3]], 7, 1)],
            '30_3.txt': [([[0, 20, 4, 2, 3, 13, 16, 1, 14, 23, 28, 5, 6, 12, 19, 15, 21, 22, 26, 17, 24, 25, 7, 10, 9], [18, 8, 27, 11, 29]], 2, 3), ([[0, 20, 4, 2, 3, 13, 16, 23, 5, 12], [1, 14, 28, 6, 19], [15, 18, 21, 22, 26, 9], [17, 24, 7, 10, 11], [25, 8, 27], [29]], 6, 2)],
            '30_5.txt': [([[0, 25, 14, 7, 24, 1, 4, 9, 15, 17, 19, 2, 5, 11, 23, 28, 12, 16, 20, 21, 10, 13, 18, 22], [27, 6, 3, 8, 26, 29], [], [], []], 5, 2)],
            '40_5.txt': [([[0, 36, 33, 14, 32, 6, 3, 5, 7, 10, 11, 16, 29, 30, 37, 1, 27, 22, 2, 34, 25], [21, 26, 9, 24, 4, 20, 23, 8, 19, 12], [28, 38, 13, 17, 31, 15, 35, 18, 39]], 3, 2)],
            '45_3.txt': [([[0, 24, 9, 32, 31, 2, 16, 33, 14, 28, 29, 30, 3, 5, 20, 21, 38, 41, 44, 4, 37, 13, 17, 10, 7, 15, 8, 25, 11, 19, 40, 35], [42, 23, 12, 39, 36, 43, 34], [1], [6, 27], [18], [22], [26]], 7, 3)],
            '50_3.txt': [([[0, 11, 28, 45, 4, 9, 22, 24, 18, 32, 20, 2, 42, 48, 3, 46, 5, 13, 23, 31, 36, 10, 40, 35, 30, 8, 44, 41, 26, 38, 39, 27, 16], [1, 21, 19, 15, 43, 33, 6, 7, 37, 14, 49, 12, 34], [47, 17, 25, 29]], 3, 3)]   
        }


        for archivo in archivos:
            print('Ahora se testea el archivo ' + archivo)
            ruta_archivo = os.path.join(carpeta_tests, archivo)
            aristas = []

            with open(ruta_archivo, 'r') as file:
                lineas = file.readlines()
                for i in range(1, len(lineas)):
                    linea = lineas[i].strip().split(",")
                    aristas.append((int(linea[0]), int(linea[1])))

            grafo = nx.Graph()
            grafo.add_edges_from(aristas)
            soluciones = casos[archivo]
            for solucion in soluciones:
                clusters, k, c = solucion
                resultado = validar_solucion_clustering(grafo, k, c, clusters)
                self.assertTrue(resultado)

    def test_mas_de_k_clusters_falla(self):
        grafo = nx.Graph()
        grafo.add_edges_from([(0, 1), (0, 8), (1, 4), (1, 3), (1, 5), (1, 6), (1, 9), (2, 7), (2, 3), (2, 5), (3, 4), (3, 6), (3, 7), (3, 5), (4, 9), (5, 7), (5, 8), (6, 7), (7, 9), (8, 9)])
        solucion = [[0, 13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 6], [7, 10, 17, 15, 14], [1, 4, 9]]
        resultado = validar_solucion_clustering(grafo, 3, 2, solucion)
        self.assertFalse(resultado)

    def test_clusters_con_vertices_random_falla(self):
        grafo = nx.Graph()
        grafo.add_edges_from([(0, 1), (0, 8), (1, 4), (1, 3), (1, 5), (1, 6), (1, 9), (2, 7), (2, 3), (2, 5), (3, 4), (3, 6), (3, 7), (3, 5), (4, 9), (5, 7), (5, 8), (6, 7), (7, 9), (8, 9)])
        solucion = [[0, 13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 200], [7, 10, 150, 15, 14]]
        resultado = validar_solucion_clustering(grafo, 3, 2, solucion)
        self.assertFalse(resultado)

    def test_vertices_con_mayor_distancia_que_c_falla(self):
        grafo = nx.Graph()
        grafo.add_edges_from([(0, 1), (0, 8), (1, 4), (1, 3), (1, 5), (1, 6), (1, 9), (2, 7), (2, 3), (2, 5), (3, 4), (3, 6), (3, 7), (3, 5), (4, 9), (5, 7), (5, 8), (6, 7), (7, 9), (8, 9)])
        solucion = [[6, 13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 0], [7, 10, 17, 15, 14]]
        resultado = validar_solucion_clustering(grafo, 3, 2, solucion)
        self.assertFalse(resultado)

    def test_vertices_en_ningun_cluster_falla(self):
        grafo = nx.Graph()
        grafo.add_edges_from([(0, 1), (0, 8), (1, 4), (1, 3), (1, 5), (1, 6), (1, 9), (2, 7), (2, 3), (2, 5), (3, 4), (3, 6), (3, 7), (3, 5), (4, 9), (5, 7), (5, 8), (6, 7), (7, 9), (8, 9)])
        solucion = [[13, 4, 3, 12, 16, 1, 21, 5, 8, 2, 11, 20], [18, 9, 19, 6], [7, 10, 17, 15, 14]]
        resultado = validar_solucion_clustering(grafo, 3, 2, solucion)
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
