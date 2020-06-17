# ************ Imports ****************
from flair.embeddings import DocumentPoolEmbeddings
from flair.embeddings import WordEmbeddings
from flair.embeddings import FlairEmbeddings
from flair.embeddings import StackedEmbeddings
from flair.data import Sentence


# **************************** Definição dos Embeddings ********************************************
def define_embed():
	# Aqui é inicializado o embeddings do FastText em português
	# A opreação seguinte define o embedding para documentos, usando o método Pool para agregar cada embeddings das palavras
	pt_embedding = WordEmbeddings('pt')
	document_embedding = DocumentPoolEmbeddings([pt_embedding])

	# Inicializando os embeddings do Flair
	flair_embedding_forward = FlairEmbeddings('pt-forward')
	flair_embedding_backward = FlairEmbeddings('pt-backward')

	# Para o Flair é recomendado inicializar dois tipos de embeddings, forward e backward, e empilha-los usando StackedEmbeddings
	stacked_embeddings = StackedEmbeddings([
											flair_embedding_forward,
											flair_embedding_backward,
										   ])

	document_embedding_flair = DocumentPoolEmbeddings([stacked_embeddings])

	embeddings = {"fastT": document_embedding, "flair":document_embedding_flair}

	return embeddings