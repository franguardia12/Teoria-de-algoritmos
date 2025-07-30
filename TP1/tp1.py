import sys
import os

def main():
    verificar_argumentos()
    path = sys.argv[1]
    intervalos, transacciones_sospechoso = obtener_intervalos_y_transacciones_sospechoso(path)
    evidencia = es_rata(intervalos, transacciones_sospechoso)
    if len(evidencia) < len(intervalos):
        print("No es el sospechoso correcto")
        return
    imprimir_resultados(evidencia)
    
def es_rata(intervalos: list[int, int], sospechosas: list[int]) -> list[list]:
    evidencia = []
    intervalos.sort(key=lambda x: x[0] + x[1])

    for sospechoso in sospechosas:
        asigne = False
        for i in range(len(intervalos)):
            hora = intervalos[i][0]
            error = intervalos[i][1]
            if hora == -1:
                continue
            if sospechoso > hora + error or sospechoso < hora - error:
                continue
            else:
                evidencia.append([sospechoso, hora, error])
                intervalos[i] = (-1, -1)
                asigne = True
                break
        
        if not asigne:
            break
    return evidencia

def imprimir_resultados(evidencia: list[list]) -> None:
    for hecho in evidencia:
        print(f'{hecho[0]} --> {hecho[1]} ± {hecho[2]}') 
    return 

def verificar_argumentos():
    if len(sys.argv) != 2:
        raise ValueError("La cantidad de argumentos ingresados no es válida")
    path = sys.argv[1]
    if not os.path.exists(path):
        raise ValueError("El archivo ingresado no existe")
    if not path.endswith(".txt"):
        raise ValueError("El archivo ingresado no es un archivo de texto")



def obtener_intervalos_y_transacciones_sospechoso(path):
    """

    Esta función recibe el path de un archivo y devuelve dos listas:
    - intervalos: lista de tuplas, donde cada tupla representa un intervalo de tiempo (ini, fin)
    - transacciones_sospechoso: lista de enteros donde cada valor es un timestamp de una transacción del sospechoso

    Si el archivo no cumple con el formato esperado, se finaliza el programa

    """

    intervalos, transacciones_sospechoso = [], []

    with open (path, "r") as archivo:
        try:
            for i, linea in enumerate(archivo):
                if i == 0:
                    # Saltea la primer linea (comentario)
                    continue
                if i == 1:
                    n = int(linea.strip())
                    continue
                linea = linea.strip()
                if i < n+2:              
                    linea = linea.split(",")
                    timestamp_aprox, error = int(linea[0]), int(linea[1])
                    intervalos.append((timestamp_aprox, error))
                else:
                    transacciones_sospechoso.append(int(linea))
            if len(transacciones_sospechoso) != n or len(intervalos) != n:
                raise ValueError("El archivo de entrada no cumple con el formato esperado.")
        except:
            raise ValueError("El archivo de entrada no cumple con el formato esperado.")
    return intervalos, transacciones_sospechoso

if __name__ == "__main__":
    main()