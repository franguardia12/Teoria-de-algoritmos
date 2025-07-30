Para ejecutar el programa, estando ubicado en la carpeta TP1, escribir en la terminal:

python3 tp1.py ruta/a/entrada.txt

Donde ruta/a/entrada es la ruta donde se encuentra el archivo .txt del set de datos a probar y tp1.py es el archivo donde se encuentra el código del algoritmo implementado

El programa espera que en ese archivo el set de datos consista en un número n que indique la cantidad de timestamps tanto de transacciones como de intervalos, luego en otra línea cada intervalo aproximado con su correspondiente error (cada uno en una línea diferente) es decir con la forma "timestamp_intervalo, error_intervalo" y finalmente cada timestamp de transacción del sospechoso (también cada uno en una línea diferente)

El resultado obtenido es una lista de listas donde cada sublista es una transacción del sospechoso con el intervalo aproximado que se le asignó y el error de este, es decir con la forma [timestamp_transaccion, timestamp intervalo, error_intervalo], esto siempre y cuando la asignación haya podido ser posible

El resultado obtenido en la asignación de intervalos puede variar en ciertos casos, sobretodo cuando había más de una asignación posible dada la distribución de timestamps, pero se garantiza que si la asignación fue posible entonces cada timestamp de transacción estará asignada a un intervalo distinto que la cubra