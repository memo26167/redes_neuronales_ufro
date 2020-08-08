#Clase 12
from nltk.tokenize import RegexpTokenizer

sentence = 'Chile ganó la Copa América los años 2015 y 2016'

tokenizer = RegexpTokenizer(r'\w+|$[0-9.]+|\S+')
tokenizer.tokenize(sentence)

#Ahora con otro tokenizador para el idioma ingles
from nltk.tokenize import TreebankWordTokenizer

sentence = """All in all, you're just another brick in the wall."""

tokenizer = TreebankWordTokenizer()
tokenizer.tokenize(sentence)


from nltk.tokenize.casual import casual_tokenize

message = """Estuvo muuuuuuy bueno el concierto!!!!! Grandeeee @PinkFloyd :*"""
casual_tokenize(message)
casual_tokenize(message, reduce_len=True, strip_handles=True)

from nltk.tokenize import TweetTokenizer

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

sent = "Estuvo muuuuuuy bueno el concierto!!!!! Grandeeee @PinkFloyd :*"

tknzr.tokenize(sent)

#########   N-gramas

import re

sentence = """Led Zeppelin fue un grupo británico de hard rock, fundado en 1968."""
pattern = re.compile(r"([-\s.,;!?])+")

tokens = pattern.split(sentence)
tokens = [x for x in tokens if x and x not in '- \t\n.,;!?']
tokens

from nltk.util import ngrams

X = list(ngrams(tokens, 2))
print(X)

list(ngrams(tokens, 3))

two_grams = list(ngrams(tokens, 2))
Y = [" ".join(x) for x in two_grams]

print(Y)

########## Stop words (eliminacion de palabras de conexion)

stop_words = ['a', 'am', 'the', 'on', 'off', 'this', 'is']
tokens = ['the', 'house', 'is', 'on', 'fire']
tokens_without_stopwords = [x for x in tokens if x not in stop_words]
print(tokens_without_stopwords)

import nltk

nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')
print(len(stop_words))
print(stop_words[:7])

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words

print(len(sklearn_stop_words))
print(len(stop_words))

stop_words = nltk.corpus.stopwords.words('spanish')
print(len(stop_words))
print(stop_words[:15])

########### Normalizacion
#NORMALIZAR LAS PALABRAS

tokens['CIENCIA', 'Ciencia', 'CiEnCiA']
normalized_tokens = [x.lower() for x in tokens]
print(normalized_tokens)

########### Stemming

def stem(phrase):
    return ' '.join([re.findall('^(.*ss|.*?)(s)?$', word)[0][0].strip("'") for word in phrase.lower().split()])

print(stem('casas'))
print(stem("Mis amigos viven en Padre Las Casas")) # Lo convierte de plural a singular

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

' '.join([stemmer.stem(w).strip("'") for w in "dish washer's washed dishes".split()])

from nltk import SnowballStemmer

stemmer = SnowballStemmer('spanish')

' '.join([stemmer.stem(w).strip("'") for w in "Entre mis amigos ella es mi mejor amiga".split()])
