from Celula import Celula
import numpy as np

a = Celula()
matriz = np.full((4, 4), Celula())
matriz[2][2].set(2)
if matriz[2][2].existe(2):
	print('blabal')