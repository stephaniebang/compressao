import numpy as np
from PIL import Image
import scipy.linalg

def imagetomatrix(nome, tipo):
	'''
	A funcao recebe o nome do arquivo da imagem e o tipo de matriz a ser formada e retorna a matriz da imagem
	Imagens L tem matriz m x n, sendo m, n os pixels da imagem
	Imagens RGB tem matriz m x n x 3, sendo o numero 3 correnspondente aos componentes vermelho, verde e azul da imagem 
	'''
	return np.asarray(Image.open(nome).convert(tipo))
#-------------------------------------------------------------------------------
def matrixtoimage(matriz, tipo):
	nome=np.array(matriz)
	img = Image.fromarray(nome, tipo)
	img.save('comprimida.png')
	img.show()
#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
def soma(matriz1,matriz2):
	if matriz1==[]:return matriz2
	if matriz2==[]:return matriz1
	soma = []
	if len(matriz1)!=1:
		for i in range (len(matriz1)):
			lin = []
			for j in range (len(matriz1[i])):
				lin.append(matriz1[i][j] + matriz2[i][j])
			soma.append(lin)
		return soma
	if len(matriz1)==1:
		for i in range(len(matriz1[0])):
			soma.append(matriz1[0][i]+matriz2[0][i])
		return [soma]
#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
def matrizvetor(A, b):
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
#-------------------------------------------------------------------------------
def escalarvetor(s,v):
	z=[]
	for i in range(len(v)):
		sm=s*v[i]
		z.append(sm)
	return z
#-------------------------------------------------------------------------------
def escalarmatriz(s,M):
	z=[]
	if len(M)!=1:
		for j in range(len(M)):
			w=[]
			for i in range(len(M[j])):
				sm=s*M[j][i]
				w.append(sm)
			z.append(w)
		return z
	if len(M)==1:
		return [escalarvetor(s,M[0])]
#-------------------------------------------------------------------------------
def vetorvetor(v1,v2):
	mult=[]
	for i in range(len(v1)):
		m=[]
		for j in range(len(v2)):
			m.append(v1[i]*v2[j])
		mult.append(m)
	return mult
#-------------------------------------------------------------------------------
def qr(matriz):
	Q, R = scipy.linalg.qr(matriz)
	return Q,R
#-------------------------------------------------------------------------------
def iteracao(matriz,e):
	Q,R=qr(matriz)
	U=Q
	for i in range(int(1/e)):
		An=mult(R,Q)
		Q,R=qr(An)
		U=mult(U,Q)
	return U,An
#-------------------------------------------------------------------------------
def autovalores(matriz):
	eigenvalures=[]
	for i in range(len(matriz[0])):
		eigenvalures.append(matriz[i][i])
	return eigenvalures
#-------------------------------------------------------------------------------
def autovetores(matriz):
	eigenvectors=[]
	for i in range(len(matriz[0])):
		eigenvectors.append([matriz[0][i],matriz[1][i],matriz[2][i]])
	return eigenvectors
#-------------------------------------------------------------------------------
def organiza(evc,evl):
	n=len(evl)
	z=[]
	evc2=[]
	for i in range(n):
		z.append(abs(evl[i]))
	evl2=sorted(z,reverse=True)
	for i in range(n):
		ind=z.index(evl2[i])
		evc2.append(evc[int(ind)])
	return evc2,evl2
#-------------------------------------------------------------------------------
def imagem(eigenvalures,eigenvectors,V,k):
	A=[]
	for i in range(k):
		Ai=vetorvetor(eigenvectors[i],V[i])
		Ai=escalarmatriz(eigenvalures[i],Ai)
		A=soma(A,Ai)
	return A
#-------------------------------------------------------------------------------
def svd(M,eigenvalures,eigenvectors):
	V=[]
	for i in range(len(eigenvalures)):
		p=matrizvetor(M,eigenvectors[i])
		p=escalarvetor(1/((eigenvalures[i])**(1/2)),p)
		V.append(p)
	return V,eigenvalures,eigenvectors
#-------------------------------------------------------------------------------
def normaliza(eigenvectors):
	for i in range(len(eigenvectors)):
		s=0
		for j in range(len(eigenvectors[i])):
			s=s+(eigenvectors[i][j])**2
		s=s**(1/2)
		norm=1/s
		eigenvectors[i]=escalarvetor(norm,eigenvectors[i])
	return eigenvectors	
#-------------------------------------------------------------------------------
def main():
	nome=str(input('Digite o nome da imagem:'))
	k = int(input('Digite o valor de k: '))
	A=imagetomatrix(nome+'.png', 'L')
	A.tolist()
	At=transposta(A)
	AtA=mult(At,A)
	print("Achando auto-valores e auto-vetores")
	U,An=iteracao(AtA,0.0001)
	eigenvalures=autovalores(An)
	eigenvectors=autovetores(U)
	print("Organizando em ordem decrescente")
	eigenvectors2,eigenvalures2=organiza(eigenvectors,eigenvalures)
	eigenvectors2=normaliza(eigenvectors2)
	print("Fazendo a SVD e gerando a imagem")
	V,eigenvalures2,eigenvectors2=svd(A,eigenvalures2,eigenvectors2)
	A=imagem(eigenvalures,eigenvectors,V,k)
	matrixtoimage(A,'L')

main()
