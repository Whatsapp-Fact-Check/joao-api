# ******************* Imports *********************
import string
#import unidecode
import spacy
# python -m spacy download pt_core_news_sm
nlp = spacy.load('pt_core_news_sm')


# Realiza um pré-processamento dos textos
def processamento(noticia):
    # Termos comuns nos títulos de notícias, mas não tão relevantes pra comparação
    termos = ['é falso que', 'é falso', 'é antigo', 'é verdadeiro', 'é dúbio que'] 
    
    pontuacao = string.punctuation
    pontuacao += "‘" +  "’"
    
    s = noticia.split(".")[0]
    
    for i in pontuacao:
        s = s.replace(i,'')

    
    palavras = s.lower().split()
    
    frase = ' '.join(palavras)
    
    for term in termos:
        frase = frase.replace(term, '')

    return frase
"""
    doc = nlp(frase)
    sem_acento = []
    for token in doc:
        if (token.pos_ == 'NOUN') or (token.pos_ == 'PROPN') or (token.pos_ == 'ADJ'):
            unaccented_string = unidecode.unidecode(str(token))
            sem_acento.append(unaccented_string)
        else:
            sem_acento.append(str(token))

    frase = ' '.join(sem_acento)
 """   