from numpy import *
import numpy as np
import matplotlib.image
import Image
from math import copysign, hypot
import math
import Image

######################
# Funcoes auxiliares #
######################

def matrizDaImagem(nome, tipo):
	'''
	A funcao recebe o nome do arquivo da imagem e o tipo de matriz a ser formada e retorna a matriz da imagem
	Imagens L tem matriz m x n, sendo m, n os pixels da imagem
	Imagens RGB tem matriz m x n x 3, sendo o numero 3 correnspondente aos componentes vermelho, verde e azul da imagem 
	'''
	return np.asarray(Image.open(nome).convert(tipo))

def matrizXvetor(A, b):
	'''
	A funcao retorna o produto da matriz com o vetor (coluna)
	'''
	v = []
	
	for i in range(len(A)):
		s = 0
		
		for j in range(len(A[0])):
			s += A[i][j] * b[j]
	
		v.append(s)
	
	return v

def transposta(matriz):
	'''
	A funcao recebe uma matriz e retorna a sua transposta
	'''
	trans = []
	
	for i in range (len(matriz[0])):
		trans.append([matriz[0][i]])
	
	for i in range (1, len(matriz), 1):
		for j in range (len(matriz[0])):
			trans[j].append(matriz[i][j])
	
	return trans

def mult(matriz1, matriz2):
	'''
	A funcao recebe duas matrizes, tal que a multiplicacao matriz1 * matriz2 seja possivel, e retorna o produto delas
	'''
	prod = []
	
	for i in range (len(matriz1)):
		prod.append([])
		
		for j in range (len(matriz2[0])):
			p = 0
			
			for k in range (len(matriz1[0])):
				p += matriz1[i][k] * matriz2[k][j]
		
			prod[i].append(p)
	
	return prod

def iteracao(matriz, e, maximo):
	'''
	A funcao recebe uma matriz, um numero e e um numero maximo. A funcao ira realizar metodo QR ate os componentes da matriz abaixo da diagonal
	terem valor menor que e ou a quantidade de iteracoes alcancar maximo e retorna U = Q1 * Q2 * ... com os autovetores aproximados da matriz
	'''
	Q, R = linalg.qr(matriz)
	U = Q
	cont = 1
	
	while (checa(matriz, e) and cont < maximo):
		Q, R = linalg.qr(matriz)
		matriz = mult(R, Q)
		U = mult(U, Q)
		cont += 1
	
	return U

def checa(matriz, e):
	'''
	A funcao recebe uma matriz e um numero e e retorna False se todos os elementos da matriz abaixo da diagonal sao menores que e e retorna False 
	caso contrario
	'''
	cont = 0
	j = 1
	
	for i in range (len(matriz[0]) - 1):
		j += cont
		
		while (j < len(matriz)):
			if (matriz[i][j] > e):
				return True
			
			j += 1
		
	return False

def SVD(A, U, diag, k):
	'''
	A funcao retorna V da SVD, dados A, U e os valores singulares
	'''
	V = []
	
	for i in range(len(A)):
		multrealvetor(A[i], 1.0 / math.sqrt(diag[i]))
	
	for i in range(k):
		V.append(matrizXvetor(A, [row[i] for row in U]))
	
	return V

def soma(matriz1, matriz2):
	'''
	A funcao recebe a matriz1 e a matriz2 e retorna a soma das matrizes
	'''
	soma = []
	for i in range (len(matriz1)):
	 	lin = []
	 	
	 	for j in range (len(matriz1)):
	 		lin.append(matriz1[i][j] + matriz2[i][j])
	 	
	 	soma.append(lin)
	
	return soma
	
def multvetor(col,lin):
	'''
	A funcao recebe um vetor col e um vetor lin e retorna a multiplicacao col x lin
	'''
	mult = []
	
	for i in range(len(col)):
		m = []
		
		for j in range(len(lin)):
			m.append(col[i] * lin[j])
		
		mult.append(m)
	
	return mult

def multrealvetor(vetor, real):
	'''
	A funcao recebe um vetor e um real e multiplica o vetor pelo real
	'''
	for i in range(len(vetor)):
		vetor[i] *= real

def decres(vetor, matriz):
	'''
	A funcao recebe um vetor com autovalores e uma matriz com autovetores correspondentes e torna a sequencia dos componentes no vetor
	decrescente, trocando a ordem dos autovetores da matriz de modo a acompanhar os autovalores 
	'''
	vdecres = [-1 for i in range(len(vetor))]
	vposicao = [i for i in range(len(vetor))]
	
	for i in range (len(vetor)):
		j = len(vetor) - 1
		
		if (abs(vetor[i]) >= vdecres[j]):
			while (vetor[i] >= vdecres[j] and j >= 0):
				j -= 1
			
			substitui(vdecres, vetor[i], j + 1)
			substitui(matriz, matriz[i], j + 1)

def substitui(lista, valor, posicao):
	'''
	A funcao recebe uma lista, um valor (que pode ser uma lista) e uma posicao e ela adiciona o valor a lista na posicao, excluindo o valor
	da ultima posicao da lista
	'''
	copia = vetor
	vetor[posicao] = valor
	
	for i in range (posicao + 1; i < len(vetor); 1):
		vetor[i] = copia[i - 1]


####################
# Funcao principal #
####################

def main():
	k = int(input('Digite o valor de k: '))
	nome = 'google'						# imagem tem m x n pixels
	
	A = matrizDaImagem(nome + '.png', 'L')		# A = m x n
	A.tolist()
	At = transposta(A.tolist())
	AtA = mult(At, A.tolist())
	
	print('Funcao iteracao')
	U = iteracao(AtA, 0.001, 15)				# U = m x n
	
	diag = []
	
	for i in range(len(AtA[0])):
		diag.append(AtA[i][i])
	
	print('Funcao decres')
	decres(diag, U)
	
	print('Funcao SVD')
	V = SVD(A.tolist(), U, diag, k)			# V = k x n
	
	imagem = []
	lin = []
	
	for i in range (len(A[0])):
		lin.append(0)
	
	for i in range (len(A)):
		imagem.append(lin)
	
	print('Finalmente obtendo a matriz da imagem comprimida :)')
	for i in range (k): 
		multrealvetor(U[i], math.sqrt(abs(diag[i])))
		uv = multvetor(V[i], U[i])
		imagem = somaMatriz(imagem, uv)
	
	npimagem = np.matrix(imagem)
	plt.imsave(nome + "comprimida.png", npimagem, cmap = 'gray')

	print('Imagem comprimida salva como ' + nome + 'comprimida.png')
	
main()
