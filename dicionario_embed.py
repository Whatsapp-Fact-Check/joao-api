# ************ Imports ****************
import pandas as pd 

from api_banco import pegar_noticias


# ********************** Recuperação das notícias já convertidas em vetores ******************************

# Cada notícia é convertida em dois vetores de características usando dois tipo de embeddings, fastText e Flair.
# Os vetores convertidos pelo FastText possuem 300 entradas cada um, já os convertidos pelo Flair possuem 4095 entradas
# Esses vetores foram salvos em um arquivo CSV para evitar que se tenha que converte-los sempre que o código iniciar
# Essa parte do código faz a recuperação desses vetores na pasta "static".

# Quando importados, os vetores vem como uma string, essa função converte a string em um vetor de floats
def converte_float(vetor):
	v = vetor[1:][:-1].split(",")
	lista = []
	for i in range(0,len(v)):
		lista.append(float(v[i]))
	return lista

def dicionario_embed():
	db = pegar_noticias()
	df = pd.DataFrame(db)
	''' O DataFrame possui 6 colunas: 0 -> Texto da Notícia
	                                  1 -> Link da Notícia
	                                  2 -> Data da Checagem
	                                  3 -> Agencia que realizou a checagem
	                                  4 -> vetores do embedding FasText
	                                  5 -> Vetores do embedding Flair
	'''
	df[4] = df[4].apply(converte_float) # Vetores fast convertidos de String para Float
	df[5] = df[5].apply(converte_float) # Vetores flair convertidos de String para Float

	vetores_flair = df.drop(columns = [1,2,3,4]) # Deixando somente a coluna com a noticia e a coluna dos vetores Flair
	vetores_fast = df.drop(columns = [1,2,3,5]) # Deixando somente a coluna com a noticia e a coluna dos vetores Fast

	#vetores_flair = pd.read_csv(os.path.abspath("static/vetor_flair.csv")).drop(columns = "Unnamed: 0")
	#vetores_fast = pd.read_csv(os.path.abspath("static/vetor_fastT.csv")).drop(columns = "Unnamed: 0")
	#vetores_flair['1'] = vetores_flair['1'].apply(converte_float)
	#vetores_fast['1'] = vetores_fast['1'].apply(converte_float)

	# Convertendo os vetores que estão na forma de DataFrame para lista. Essa conversão facilita na iteração posterior
	flair = vetores_flair.values.tolist()
	fastT = vetores_fast.values.tolist()

	dicio_vetores = {"fastT" : fastT, "flair" : flair}

	return dicio_vetores