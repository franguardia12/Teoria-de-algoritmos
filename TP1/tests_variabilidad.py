import unittest
import os
from tp1 import es_rata
from tp1 import obtener_intervalos_y_transacciones_sospechoso
from sys import argv, stdin, stderr


def verificar_salida_esperada(salidas, intervalos):
    if len(salidas) != len(intervalos):
        return False
    for salida in salidas:
        transaccion, hora, error = salida
        if transaccion < hora - error or transaccion > hora + error:
            return False
    return True

class TestAlgoritmoMafia(unittest.TestCase):
    def test_casos_archivos(self):
        # Ruta de la carpeta que contiene los archivos de prueba
        carpeta_tests = 'tests_catedra'
        archivos = ["5-es.txt", "5-no-es.txt", "10-es-bis.txt", "10-es.txt", "10-no-es-bis.txt", "10-no-es.txt", "50-es.txt", "50-no-es.txt", "100-es.txt", "100-no-es.txt", "500-es.txt", "500-no-es.txt", "1000-es.txt", "1000-no-es.txt", "5000-es.txt", "5000-no-es.txt"]

        for archivo in archivos:
            print("Ahora se testea el archivo " + archivo)
            ruta_archivo = os.path.join(carpeta_tests, archivo)

            intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(ruta_archivo)
            resultado = es_rata(intervalos, transacciones_sospechoso)

            if 'no' in archivo:
                resultado_no_valido = verificar_salida_esperada(resultado, intervalos)
                self.assertFalse(resultado_no_valido)
            else:
                resultado_valido = verificar_salida_esperada(resultado, intervalos)
                self.assertTrue(resultado_valido)


    def test_todos_valores_iguales_no_es_rata(self):
        carpeta_tests = 'tests_propios'
        archivo = "02-no-es.txt"
        print("Ahora se testea el archivo " + archivo)
        ruta_archivo = os.path.join(carpeta_tests, archivo)


        intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(ruta_archivo)
        resultado = es_rata(intervalos, transacciones_sospechoso)

        resultado_no_valido = verificar_salida_esperada(resultado, intervalos)
        self.assertFalse(resultado_no_valido)


    def test_todos_los_puntos_cubiertos_pero_no_es_rata(self):
        carpeta_tests = 'tests_propios'
        archivo = "03-no-es.txt"
        print("Ahora se testea el archivo " + archivo)
        ruta_archivo = os.path.join(carpeta_tests, archivo)


        intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(ruta_archivo)
        resultado = es_rata(intervalos, transacciones_sospechoso)

        resultado_no_valido = verificar_salida_esperada(resultado, intervalos)
        self.assertFalse(resultado_no_valido)


    def test_todos_valores_iguales_es_rata(self):
        carpeta_tests = 'tests_propios'
        archivo = "01-es.txt"
        print("Ahora se testea el archivo " + archivo)
        ruta_archivo = os.path.join(carpeta_tests, archivo)


        intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(ruta_archivo)
        resultado = es_rata(intervalos, transacciones_sospechoso)

        resultado_valido = verificar_salida_esperada(resultado, intervalos)
        self.assertTrue(resultado_valido)

    
    def test_intervalos_cubren_puntos_pero_no_es_rata(self):
        carpeta_tests = 'tests_propios'
        archivo = "04-no-es.txt"
        print("Ahora se testea el archivo " + archivo)
        ruta_archivo = os.path.join(carpeta_tests, archivo)


        intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(ruta_archivo)
        resultado = es_rata(intervalos, transacciones_sospechoso)

        resultado_no_valido = verificar_salida_esperada(resultado, intervalos)
        self.assertFalse(resultado_no_valido)



if __name__ == "__main__":
    unittest.main()

    

    


