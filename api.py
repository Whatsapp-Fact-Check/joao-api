# ************ Imports ****************
import pandas as pd 
import os

import numpy as np 

from dicionario_embed import dicionario_embed
from embed import calcula_embed

# Dicionario em com as noticias convertidas para vetores
# O dicionário esta na forma:
#         {"fastT" : fastT, "flair" : flair}, sendo fastT/flair a lista com os vetores das noticias calculadas pelo FastText/Flair

dicio_vetores = dicionario_embed()


# ************** Cálculo de similaridade entre as notícias *********************************

# Para descobrir qual a notícia mais similar do banco com a frase que foi recebida, primeiro a frase é convertida em vetor
# usando os embaddings, em seguida para cada um dos embaddings é feito o seguinte procedimento:
# 	1) O vetor da frase (v1) é comparado com cada um dos vetores do banco (v2) para que se descubra qual o mais similar,
# a medida de simimilaridade usada é o arco-cosseno dado pela fórmula arcos(<|v1|,|v2|> / (|v1|*|v2|))
# 	2) Após feito esse cálculo para todas as notícias do banco, a lista com os valores encontrados para a similaridade é ordenada
# e são retornados as 10 noticias com maior similaridade
#	3) Serão selecionadas como retorno da API aquelas noticias que estiverem presente em ambas as listas de 10 mais similares
  
def arcos(vet1, vet2):   
    vetor_np1 = vet1.detach().numpy()
    
    try:
        vetor_np2 = vet2.detach().numpy()
    except:
        vetor_np2 = vet2
    
    simi = (np.dot(vetor_np1,vetor_np2)) / (np.linalg.norm(vetor_np1) * np.linalg.norm(vetor_np2))
    return np.arccos(simi)


def similaridade(frase, tipo_embeding):

	vetor_frase = calcula_embed(frase, tipo_embeding)

	lista_similaridade = []
	for i in dicio_vetores[tipo_embeding]: # Primeira posição do vetor é a frase e a segunda o vetor de embedings
		lista_similaridade.append((arcos(vetor_frase,i[1]), i[0]))

	lista_similaridade.sort(reverse = False)

	return lista_similaridade[:10]

def gerar_respostas(frase):
	lista_embedings = ['fastT','flair']
	lista_similares = []
	for emb in lista_embedings:
		lista_similares.append(similaridade(frase,emb))
	
	lista_final = []

	for i in range(0,len(lista_similares[0])):
		noticia_fast = lista_similares[0][i]
		for j in range(0,len(lista_similares[0])):
			noticia_flair = lista_similares[1][j]
			if (noticia_fast[1] == noticia_flair[1]):
				lista_final.append(noticia_fast)
	
	return lista_final
