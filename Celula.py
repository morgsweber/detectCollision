from Linha import Linha

class Celula:
	def __init__(self, listaDeInteiros = []):
		self.listaDeInteiros = listaDeInteiros

	def imprime(self): 
		print (self.listaDeInteiros)

	def set(self, a : int): 
		self.listaDeInteiros.append(a)

	def existe(self, a: Linha() ) -> bool:
		if a in self.listaDeInteiros:
			return True
		else: 
			return False