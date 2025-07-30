import unittest
import os
from tp2 import obtener_diccionario
from tp2 import desencriptar

class TestAlgoritmoTraduccionMensaje(unittest.TestCase):
    def test_casos_archivos(self):
        #Ruta de la carpeta que contiene los archivos de prueba
        carpeta_tests = 'tests_catedra'
        carpeta_sets = 'sets_catedra'
        archivos = [("10_in.txt", "corto.txt"), ("15_in.txt", "mediano.txt"), ("50_in.txt", "corto.txt"), ("60_in.txt", "grande.txt"), ("70_in.txt", "mediano.txt"), 
                    ("80_in.txt", "grande.txt"), ("100_in.txt", "mediano.txt"), ("120_in.txt", "corto.txt"), ("150_in.txt", "grande.txt"), 
                    ("200_in.txt", "gigante.txt"), ("500_in.txt", "gigante.txt"), ("2000_in.txt", "supergigante.txt"), ("5000_in.txt", "supergigante.txt"), 
                    ("lorem_ipsum_in.txt", "lorem_ipsum_words.txt")]

        for archivo in archivos:
            print("Ahora se testea el archivo " + archivo[0])
            ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo[0])
            ruta_archivo_palabras = os.path.join(carpeta_sets, archivo[1])

            diccionario = obtener_diccionario(ruta_archivo_palabras)
            max_largo = max(len(palabra) for palabra in diccionario)

            with open(ruta_archivo_cadenas, 'r') as file:
                for linea in file:
                    texto = linea.strip()
                    if not texto:
                        continue

                    resultado = desencriptar(texto, diccionario, max_largo)

                    if resultado == "No es un mensaje":
                        continue

                    lista_solucion = resultado.split(" ")

                    for palabra in lista_solucion:
                        self.assertTrue(palabra in diccionario)

                    cadena_sin_espacios = "".join(lista_solucion)
                    self.assertTrue(texto == cadena_sin_espacios)


    def test_todas_palabras_iguales_pero_validas_es_mensaje_valido(self):
        carpeta_tests = 'tests_propios'
        carpeta_sets = 'sets_propios'

        archivo_cadenas = "01-es.txt"
        archivo_palabras = "comunes.txt"

        print("Ahora se testea el archivo " + archivo_cadenas)

        ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo_cadenas)
        ruta_archivo_palabras = os.path.join(carpeta_sets, archivo_palabras)

        diccionario = obtener_diccionario(ruta_archivo_palabras)
        max_largo = max(len(palabra) for palabra in diccionario)

        with open(ruta_archivo_cadenas, 'r') as file:
            for linea in file:
                texto = linea.strip()
                if not texto:
                    continue

                resultado = desencriptar(texto, diccionario, max_largo)

                if resultado == "No es un mensaje":
                    continue

                lista_solucion = resultado.split(" ")

                for palabra in lista_solucion:
                    self.assertTrue(palabra in diccionario)

                cadena_sin_espacios = "".join(lista_solucion)
                self.assertTrue(texto == cadena_sin_espacios)


    def test_parecian_ser_mensajes_pero_al_final_no(self):
        carpeta_tests = 'tests_propios'
        carpeta_sets = 'sets_propios'

        archivo_cadenas = "02-no-es.txt"
        archivo_palabras = "set_invisible.txt"

        print("Ahora se testea el archivo " + archivo_cadenas)

        ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo_cadenas)
        ruta_archivo_palabras = os.path.join(carpeta_sets, archivo_palabras)

        diccionario = obtener_diccionario(ruta_archivo_palabras)
        max_largo = max(len(palabra) for palabra in diccionario)

        with open(ruta_archivo_cadenas, 'r') as file:
            for linea in file:
                texto = linea.strip()
                if not texto:
                    continue

                resultado = desencriptar(texto, diccionario, max_largo)

                if resultado == "No es un mensaje":
                    continue

                lista_solucion = resultado.split(" ")

                for palabra in lista_solucion:
                    self.assertTrue(palabra in diccionario)

                cadena_sin_espacios = "".join(lista_solucion)
                self.assertTrue(texto == cadena_sin_espacios)


    def test_cadenas_mezcladas(self):
        carpeta_tests = 'tests_propios'
        carpeta_sets = 'sets_propios'

        archivo_cadenas = "03-mezclados.txt"
        archivo_palabras = "w_set.txt"

        print("Ahora se testea el archivo " + archivo_cadenas)

        ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo_cadenas)
        ruta_archivo_palabras = os.path.join(carpeta_sets, archivo_palabras)

        diccionario = obtener_diccionario(ruta_archivo_palabras)
        max_largo = max(len(palabra) for palabra in diccionario)

        with open(ruta_archivo_cadenas, 'r') as file:
            for linea in file:
                texto = linea.strip()
                if not texto:
                    continue

                resultado = desencriptar(texto, diccionario, max_largo)

                if resultado == "No es un mensaje":
                    continue

                lista_solucion = resultado.split(" ")

                for palabra in lista_solucion:
                    self.assertTrue(palabra in diccionario)

                cadena_sin_espacios = "".join(lista_solucion)
                self.assertTrue(texto == cadena_sin_espacios)


    def test_mensaje_completo(self):
        carpeta_tests = 'tests_propios'
        carpeta_sets = 'sets_propios'

        archivo_cadenas = "04-plan.txt"
        archivo_palabras = "palabras_clave.txt"

        print("Ahora se testea el archivo " + archivo_cadenas)

        ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo_cadenas)
        ruta_archivo_palabras = os.path.join(carpeta_sets, archivo_palabras)

        diccionario = obtener_diccionario(ruta_archivo_palabras)
        max_largo = max(len(palabra) for palabra in diccionario)

        with open(ruta_archivo_cadenas, 'r') as file:
            for linea in file:
                texto = linea.strip()
                if not texto:
                    continue

                resultado = desencriptar(texto, diccionario, max_largo)

                if resultado == "No es un mensaje":
                    continue

                lista_solucion = resultado.split(" ")

                for palabra in lista_solucion:
                    self.assertTrue(palabra in diccionario)

                cadena_sin_espacios = "".join(lista_solucion)
                self.assertTrue(texto == cadena_sin_espacios)


    def test_cadenas_mas_grandes_mezcladas(self):
        carpeta_tests = 'tests_propios'
        carpeta_sets = 'sets_propios'

        archivo_cadenas = "05-mezclados2.txt"
        archivo_palabras = "comunes.txt"

        print("Ahora se testea el archivo " + archivo_cadenas)

        ruta_archivo_cadenas = os.path.join(carpeta_tests, archivo_cadenas)
        ruta_archivo_palabras = os.path.join(carpeta_sets, archivo_palabras)

        diccionario = obtener_diccionario(ruta_archivo_palabras)
        max_largo = max(len(palabra) for palabra in diccionario)

        with open(ruta_archivo_cadenas, 'r') as file:
            for linea in file:
                texto = linea.strip()
                if not texto:
                    continue

                resultado = desencriptar(texto, diccionario, max_largo)

                if resultado == "No es un mensaje":
                    continue

                lista_solucion = resultado.split(" ")

                for palabra in lista_solucion:
                    self.assertTrue(palabra in diccionario)

                cadena_sin_espacios = "".join(lista_solucion)
                self.assertTrue(texto == cadena_sin_espacios)

            

if __name__ == "__main__":
    unittest.main()
