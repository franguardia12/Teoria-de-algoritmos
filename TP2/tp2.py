import sys
import os

def main():
    verificar_argumentos()
    diccionario = obtener_diccionario(sys.argv[1])
    max_largo = max(len(palabra) for palabra in diccionario)
    for linea in sys.stdin:
        texto = linea.strip()
        if not texto:
            continue
        resultado = desencriptar(texto, diccionario, max_largo)
        print(resultado)

def verificar_argumentos():
    if len(sys.argv) != 2:
        raise ValueError("La cantidad de argumentos ingresados no es válida")
    path_palabras = sys.argv[1]
    if not os.path.exists(path_palabras):
        raise ValueError("El archivo ingresado no existe")
    if not path_palabras.endswith(".txt"):
        raise ValueError("El archivo ingresado no es un archivo de texto")
    
def obtener_diccionario(path_palabras):
    with open(path_palabras, "r") as archivo:
        diccionario = set()
        for linea in archivo:
            palabra = linea.strip()
            if palabra.isalpha():
                diccionario.add(palabra)
    if not diccionario:
        raise ValueError("El diccionario está vacío o no contiene palabras válidas")
    return diccionario

def desencriptar(texto, diccionario, max_largo):
    """
    Desencripta el texto dado utilizando el diccionario proporcionado.
    Si el texto no puede ser desencriptado, devuelve "No es un mensaje".
    Además del texto y el diccionario, se pasa el largo de la palabra más larga
    del diccionario para optimizar la búsqueda.
    """
    optimos = [False] * (len(texto)+1)

    optimos[0] = True
    optimos[1] = True if texto[0] in diccionario else False

    indices = [-1] * (len(texto) + 1) # Indica el indice donde empieza la palabra que termina en cada posición j
    for j in range(2,len(optimos)):
        for i in range(j, max(0, j - max_largo), -1):
            aux = texto[i-1:j]
            if aux in diccionario and optimos[i-1]:
                optimos[j] = True
                indices[j] = i-1
                break
    if not optimos[-1]:
        return "No es un mensaje"
    return reconstruccion(texto, optimos, indices)

def reconstruccion(texto, optimos, indices):
    palabras = []
    idx = len(texto)
    while idx > 0:
        i = indices[idx]
        palabras.append(texto[i:idx])
        idx = i
    palabras.reverse()
    return " ".join(palabras)

if __name__ == "__main__":
    main()