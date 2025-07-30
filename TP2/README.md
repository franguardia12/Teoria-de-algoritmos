Para ejecutar el programa, estando ubicado en la carpeta TP2, escribir en la terminal:

`python3 tp2.py ruta/a/listado-palabras.txt < posibles_mensajes.txt`

Donde `ruta/a/listado-palabras` es la ruta donde se encuentra el archivo .txt con palabras posibles que se consideran como válidas, y `tp2.py` es el archivo donde se encuentra el código del algoritmo implementado.

El programa espera que el archivo posibles_mensajes contenga, en cada línea, una cadena de texto sin espacios, que representa un mensaje encriptado. Por otro lado, en listado-palabras.txt se encuentra el conjunto de palabras que se utilizará para desencriptar.

El resultado obtenido es el mensaje desencriptado con sus espacios correspondientes, o bien "no es un mensaje" si no se encuentra una segmentación válida.
