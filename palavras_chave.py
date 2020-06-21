# ************************************* Imports *******************************
import numpy as np
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

from embed import calcula_embed
from api import arcos

# python -m spacy download pt_core_news_sm
nlp = spacy.load('pt_core_news_sm')


# A função a seguir recebe uma frase como paramentro e retorna uma lista onde cada elemento é uma tupla
# a tupla é definida da seguinte forma: (PoS Tag, palavra)
# O primeiro elemento da dupla é a tag 'Part of Speech' (classe gramatical) da palavra na segunda posição da dupla
# São selecionados aqui somente as seguintes classes gramaticais: Substantivo (NOUN/PROPN), Verbo (VERB) e Adjetivo (ADJ).
# Também são retiradas as STOPWORDS
def pegar_keywords(frase):
	dicio_pos = {'NOUN':'NOUN', 'PROPN':'NOUN', 'ADJ':'ADJ', 'VERB':'VERB' }
	doc = nlp(frase)
	lista_chave = []
	for token in doc:
		if (token.pos_ == 'NOUN') or (token.pos_ == 'PROPN') or (token.pos_ == 'ADJ') or (token.pos_ == 'VERB'):
			if str(token) not in STOP_WORDS:
				lista_chave.append((dicio_pos[token.pos_],str(token)))
			
	return lista_chave


# A função recebe a lista de palavras que foi feita pela 'pegar_keywords' e agrupa em uma lista as palavras
# que possuem a mesma classe gramatical
def junta_pos(lista, tipo):
	return [pos_tag[1] for pos_tag in lista if pos_tag[0] == tipo]


# A função 'compara_keywords' recebe duas frases como parametro e retorna uma medida de similaridade entre as duas
# A similaridade é calculada comparando as palavras chave de mesma classe gramatical das duas frases
# A comparação é feita calculando o arcosseno dos embeddings obtidos pelo algoritmo Fast Text
def compara_keywords(frase1,frase2):
	lista1 = pegar_keywords(frase1.lower())
	lista2 = pegar_keywords(frase2.lower())
	POS_list = ['NOUN', 'ADJ', 'VERB']
	nota = []

	for pos in POS_list:
		compara1 = junta_pos(lista1,pos)
		compara2 = junta_pos(lista2,pos)

		if (len(compara1) != 0) and (len(compara2) != 0):
			for p1 in compara1:
				lis = []
				for p2 in compara2:
					tensor1 = calcula_embed(p1, 'fastT')
					tensor2 = calcula_embed(p2, 'fastT')
					if (tensor1.sum().item() != 0)  and (tensor2.sum().item() != 0):   
						if (p1 != p2):
							simi = arcos(tensor1, tensor2)
						else:
							simi = 0
						lis.append(simi)
				nota.append(np.mean(lis))

	return np.mean(nota)
