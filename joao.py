# Para executar: export FLASK_APP=joao.py
#                flask run
# ls -A ~
# source env/bin/activate


# Conhecereis a Verdade e a Verdade Vos Libertará João 8, 32

from flask import Flask
from markupsafe import escape
from flask import request
from flask import jsonify

import pandas as pd 
import os

from api import gerar_respostas
from api_banco import pegar_noticias
from palavras_chave import compara_keywords
from processamento_texto import processamento


noticias = pegar_noticias()
df = pd.DataFrame(noticias)
df.drop(columns = [4,5], inplace = True)
df.rename(columns = {0:'noticia', 1:'link', 2:'data', 3:'checagem'}, inplace = True)


app = Flask(__name__)


def checar(frase):
	if (frase != ''):
		respostas = gerar_respostas(frase.lower())
		lista = []
		if (respostas):
			for resp in respostas:
				limite = compara_keywords(frase,processamento(resp[1]))

				if (limite < 1.1): # 1.1 foi considerado um limite razoáveel pra dizer que duas frases são parecidas

					ind = df[df['noticia'] == resp[1]]['data'].index #Gambiarra pra printar direito
					dicio = {'Checado' : resp[1], 'Data' :  df['data'].loc[[i for i in ind][0]],
							'Checado_por' : df['checagem'].loc[[i for i in ind][0]],
							'Link' : df['link'].loc[[i for i in ind][0]]}
					lista.append(dicio)
			
		return jsonify(lista)
	else:
		return jsonify([])


@app.route('/checagem', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		frase = request.get_json() 
	
		return checar(frase["text"])
	else:
		return "Não encontrado"
