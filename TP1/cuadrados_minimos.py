# Imports necesarios para el notebook
from random import seed

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from tp1 import es_rata
from util import time_algorithm

MIN_ERROR = 5
# El maximo error es el minimo de las horas
# El salto del error es la mitad del MIN_HORA

# Estos parámetros determinan el minimo y el salto de las transacciones sospechosas
MIN_HORA = 500
JUMP = 15

def generar_datos(size=50000):

	# Generamos las horas
    horas = [np.random.randint(MIN_HORA, MIN_HORA + 1)]
    for _ in range(size - 1):
        horas.append(horas[-1] + np.random.randint(0, JUMP))
    
	# Agregamos los errores
    intervalos = [(hora, np.random.randint(MIN_ERROR, MIN_HORA // 2)) for hora in horas[:size]]

    # Generamos sospechosos
    sospechosos = [np.random.randint(hora - error, hora + error) for hora, error in intervalos]
    np.random.shuffle(horas)
    
    return intervalos, sospechosos


# Siempre seteamos la seed de aleatoridad para que los resultados sean reproducibles
def cuadrados_minimos():
	seed(12345)
	np.random.seed(12345)

	sns.set_theme()
	x = np.linspace(100, 50000, 20).astype(int)
	# es_rata recibe intervalos y transacciones sospechosas
	results = time_algorithm(es_rata, x, lambda i: generar_datos(i))
    
	f_nlogn = lambda x, c1, c2: c1 * x * np.log(x) + c2 
	f_n2 = lambda x, c1, c2: c1 * x**2 + c2
     
	c_nlogn, _ = sp.optimize.curve_fit(f_nlogn, x, [results[n] for n in x])
	c_n2, _ = sp.optimize.curve_fit(f_n2, x, [results[n] for n in x])

	ax: plt.Axes
	fig, ax = plt.subplots()
	ax.plot(x, [results[n] for n in x], label="Medición")
	ax.plot(x, [f_nlogn(n, c_nlogn[0], c_nlogn[1]) for n in x], 'r--', label="Ajuste $n /log(n)$")
	ax.plot(x, [f_n2(n, c_n2[0], c_n2[1]) for n in x], 'g--', label="Ajuste $n^2$")
	ax.set_title('Tiempo de ejecución de es_rata')
	ax.set_xlabel('Tamaño del array')
	ax.set_ylabel('Tiempo de ejecución (s)')
	ax.legend()
	plt.show()

	errors_nlogn = [np.abs(c_nlogn[0] * n * np.log(n) + c_nlogn[1] - results[n]) for n in x]
	errors_n2 = [np.abs(c_n2[0] * n**2 + c_n2[1] - results[n]) for n in x]

	print(f"Error cuadrático total para n log(n): {np.sum(np.power(errors_nlogn, 2))}")
	print(f"Error cuadrático total para n^2: {np.sum(np.power(errors_n2, 2))}")
		
	ax: plt.Axes
	fig, ax = plt.subplots()
	ax.plot(x, errors_nlogn, label="Ajuste $n /log(n)$")     
	ax.plot(x, errors_n2, label="Ajuste $n^2$")
	ax.set_title('Error de ajuste')
	ax.set_xlabel('Tamaño del array')
	ax.set_ylabel('Error absoluto (s)')
	ax.legend()
	plt.show()

cuadrados_minimos()