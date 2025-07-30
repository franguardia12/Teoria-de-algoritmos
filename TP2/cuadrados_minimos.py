# Imports necesarios para el notebook
from random import seed

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from tp2 import desencriptar
from util import time_algorithm, obtener_diccionario



PORCENTAJE_ERRONEOS = 0
# Este parámetro indica la probabilidad de que se se le agregue un error al texto
# que en consecuencia es el porcentaje de errores para la sample generada

ES_UNA_PALABRA = False
# Este parámetro indica si se quiere generar el texto con una unica palabra


def generar_datos(diccionario :dict, size :int, max_largo) -> tuple[str, dict]:
	
	"""
	Genera una lista de textos encriptados (sin espacios) usando palabras del diccionario.
	
	devuelve una tupla: (texto, diccionario)
	"""
	lista_palabras = list(diccionario)
	lista_palabras.pop(0)
	if ES_UNA_PALABRA:
		seleccionadas = [np.random.choice(lista_palabras)] * size
	else:
		seleccionadas = np.random.choice(lista_palabras, size)
	texto = "".join(seleccionadas)

		
	if np.random.randint(0, 100) <= PORCENTAJE_ERRONEOS:
		texto = agregar_errores(texto, size)
	return texto, diccionario, max_largo

def agregar_errores(texto: str, n: int) -> str:
	"""
	Agrega errores al texto encriptado y lo devuelve.
	"""
	caracteres = "abcdefghijklmnopqrstuvwxyz"
	texto = list(texto)
	for _ in range(n):
		error = np.random.choice(["insertar", "borrar", "sustituir"])
		pos = np.random.randint(0, len(texto)-1)

		if error == "insertar":
			texto.insert(pos, np.random.choice(list(caracteres)))

		elif error == "borrar":
			if pos == 0:
				texto.pop(0)
			else:
				texto.pop(pos)
		elif error == "sustituir":
			texto[pos] = np.random.choice(list(caracteres))

	return "".join(texto)
# Siempre seteamos la seed de aleatoridad para que los resultados sean reproducibles
def cuadrados_minimos():
	seed(12345)
	np.random.seed(12345)

	sns.set_theme()
	x = np.linspace(100, 5000, 20).astype(int)
	# desencriptar recibe un texto y un diccionario
	diccionario = obtener_diccionario()
	max_largo = (max(len(palabra) for palabra in diccionario) + 1)
	results = time_algorithm(desencriptar, x, lambda i: generar_datos(diccionario, i, max_largo))
    
	#f_nlogn = lambda x, c1, c2: c1 * x * np.log(x) + c2 
	#f_n2 = lambda x, c1, c2: c1 * x**2 + c2
	#f_n3 = lambda x, c1, c2: c1 * x**3 + c2
	f_nL2 = lambda x, c1, c2: c1 * x * (max_largo**2) + c2
     
	#c_nlogn, _ = sp.optimize.curve_fit(f_nlogn, x, [results[n] for n in x])
	#c_n2, _ = sp.optimize.curve_fit(f_n2, x, [results[n] for n in x])
	#c_n3, _ = sp.optimize.curve_fit(f_n3, x, [results[n] for n in x])
	c_nL2, _ = sp.optimize.curve_fit(f_nL2, x, [results[n] for n in x])

	ax: plt.Axes
	fig, ax = plt.subplots()
	ax.plot(x, [results[n] for n in x], label="Medición")
	#ax.plot(x, [f_nlogn(n, c_nlogn[0], c_nlogn[1]) for n in x], 'r--', label="Ajuste $n /log(n)$")
	#ax.plot(x, [f_n2(n, c_n2[0], c_n2[1]) for n in x], 'g--', label="Ajuste $n^2$")
	#ax.plot(x, [f_n3(n, c_n3[0], c_n3[1]) for n in x], 'b--', label="Ajuste $n^3$")
	ax.plot(x, [f_nL2(n, c_nL2[0], c_nL2[1]) for n in x], 'm--', label="Ajuste $n * L^2$")
	ax.set_title('Tiempo de ejecución de desencriptar')
	ax.set_xlabel('Cantidad de palabras')
	ax.set_ylabel('Tiempo de ejecución (s)')
	ax.legend()
	plt.show()

	#errors_nlogn = [np.abs(c_nlogn[0] * n * np.log(n) + c_nlogn[1] - results[n]) for n in x]
	#errors_n2 = [np.abs(c_n2[0] * n**2 + c_n2[1] - results[n]) for n in x]
	#errors_n3 = [np.abs(c_n3[0] * n**3 + c_n3[1] - results[n]) for n in x]
	errors_nL2 = [np.abs(f_nL2(n, c_nL2[0], c_nL2[1]) - results[n]) for n in x]

	#print(f"Error cuadrático total para n log(n): {np.sum(np.power(errors_nlogn, 2))}")
	#print(f"Error cuadrático total para n^2: {np.sum(np.power(errors_n2, 2))}")
	#print(f"Error cuadrático total para n^3: {np.sum(np.power(errors_n3, 2))}")
	print(f"Error cuadrático total para n⋅L²: {np.sum(np.power(errors_nL2, 2))}")
		
	ax: plt.Axes
	fig, ax = plt.subplots()
	#ax.plot(x, errors_nlogn, label="Ajuste $n /log(n)$")     
	#ax.plot(x, errors_n2, label="Ajuste $n^2$")
	#ax.plot(x, errors_n3, label="Ajuste $n^3$")
	ax.plot(x, errors_nL2, label="Ajuste $n * L^2$")
	ax.set_title('Error de ajuste')
	ax.set_xlabel('Cantidad de palabras')
	ax.set_ylabel('Error absoluto (s)')
	ax.legend()
	plt.show()

cuadrados_minimos()