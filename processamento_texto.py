# ******************* Imports *********************
import string


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
    
    #significativas = [w for w in palavras if not w in stopwords]
    
    #frase = ' '.join(significativas)
    
    frase = ' '.join(palavras)
    
    for term in termos:
        frase = frase.replace(term, '')
    
    return frase