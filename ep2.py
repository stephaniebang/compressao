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

def tridiag(matriz):
	'''
	A funcao recebe uma matriz simetrica e a tridiagonaliza por decomposicao QR com rotacao de Givens
	'''
	cont = 0
	
	for j in range (len(matriz[0]) - 2):
		i = 1 + cont
	
		while (i < len(matriz[0]) - 1):
			givens(matriz, (i, j))
			i += 1
		cont += 1

def givens(matriz, (x, y)):
	'''
	A funcao recebe uma matriz e as coordenadas de um ponto nela e zera o ponto localizado abaixo por rotacao de Givens
	'''
	c = math.sqrt(matriz[x][y] ** 2.0 / (matriz[x][y] ** 2 + matriz[x + 1][y] ** 2))
	s = math.sqrt(matriz[x + 1][y] ** 2.0 / (matriz[x][y] ** 2 + matriz[x + 1][y] ** 2))
	
	if ((matriz[x][y] > 0 and matriz[x+1][y] > 0) or (matriz[x][y] < 0 and matriz[x+1][y] < 0)):
		s *= -1
	for i in range (len(matriz[0])):
		cima = matriz[x][i]				# copia do ponto (x, i)
		baixo = matriz[x + 1][i]			# copia do ponto (x + 1, i)
		matriz[x][i] = cima * c - baixo * s
		matriz[x + 1][i] = cima * s + baixo * c

def qr(A):
    m, n = np.shape(A)
    Q = np.eye(m)
    for i in range(n - (m == n)):
        H = np.eye(m)
        H[i:][i:] = make_householder(A[i:][i])
        Q = np.dot(Q, H)
        A = np.dot(H, A)
    return Q, A
 
def make_householder(a):
    v = a / (a[0] + np.copysign(np.linalg.norm(a), a[0]))
    v[0] = 1
    H = np.eye(np.shape(a[0]))
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])
    return H
    
def iteracao(A,k):
	for i in range(k):
		Q,R=linalg.qr(A)
		
		A=mult(R,Q)
	
	return A

def SVD(A, diag, k):
	V = []
	
	for i in range (k):
		col=[]
		for j in range (len(A)):
			col.append(A[i][j])
		if (diag[i] != 0):
			multrealvetor(col, 1/math.sqrt(abs(diag[i])))
		V.append(col)
	
	return V

def soma(matriz1, matriz2):
	'''
	Soma matriz
	'''
	soma = []
	for i in range (len(matriz1)):
	 	lin = []
	 	
	 	for j in range (len(matriz1)):
	 		lin.append(matriz1[i][j]+matriz2[i][j])
	 	
	 	soma.append(lin)
	
	return soma
	
def multvetor(col,lin):
	mult = []
	
	for i in range(len(col)):
		m = []
		
		for j in range(len(lin)):
			m.append(col[i] * lin[j])
		
		mult.append(m)
	
	return mult

def multrealvetor(vetor, real):
	for i in range(len(vetor)):
		vetor[i] *= real

####################
# Funcao principal #
####################

def main():
	k=int(input('Digite o valor de k: '))
	t = [[1,1,2, 7], [0, -1, 5, 1]]

	A = matrizDaImagem('google.png', 'L')
	At = transposta(A)
	AtA = mult(At, A)
	B=iteracao(AtA,k)
	diag = []
	for i in range(len(B[0])):	
		diag.append(B[i][i])
	print(len(diag))
	sorted(diag, key=abs, reverse=True)
	
	V = SVD(A, diag, k)
	Vt = transposta(V)
	
	U = []
	imagem = []
	lin = []
	
	for i in range(k):
		lin.append(0)
	
	for i in range (k):
		U.append(0)
		imagem.append(lin)
	
		
	
	for i in range (k): 
		U[i] = 1
		multrealvetor(U, math.sqrt(abs(diag[i])))
		uv = multvetor(U, Vt[i])
		
		imagem = soma(imagem, uv)
	
	pil_im = Image.fromarray(uint8(imagem))
	pil_im.save("your_file.png")
	
	'''	
	from matplotlib import pyplot as plt
	plt.imshow(arr, interpolation='nearest')
	plt.show()
	'''
	
main()
