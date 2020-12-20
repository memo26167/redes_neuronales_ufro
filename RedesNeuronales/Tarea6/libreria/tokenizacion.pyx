from __future__ import print_function

import re
from nltk.tokenize.casual import casual_tokenize

# Stopwords
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
stopwords = nltk.corpus.stopwords.words('english')

# Stemming
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

puntuacion = set((',', '.', '--', '-', '¡', '!', '¿', '?', ':', ';', '``', "''", '(', ')', '[', ']', '«',
                  '»', '/', '—', '_', '..', '+', '…', '‘', '’', '–', '%', '“', '”', '″', '"', '·', '|',
                  '<', '>', '=', '*', '°', "'", '___', '{', '}', ':}', '...', '', '^', '`', '´', '$', ' '))

remove_from_text = ['<br /><br />', '\x96', '\x97', "'s", '<SPOILER>', '</SPOILER>', '<p>', '<em>', '</em>', '<i>', '</i>',
                      '<hr>', '<grin>', '<spoiler>', '</spoiler>']

token_removal_characters = ['@', '.com', 'www', '#', '=', '<', '>', 'http', ':']

emoticons = re.compile('(?::|;|=|X)(?:-)?(?:\)|\(|D|P)')

class Tokenizador:
    '''Objeto que tokeniza'''
    def __init__(self, 
                 text_remove=1,   reduce_len=1, strip_handles=1,
                 stopwords=1, puntuacion=1, numbers=1,
                 token_remove=1, stemming=1):    
        
        # Eliminamos caracteres del texto que no se tokenizan bien
        self.text_remove = text_remove
        
        # Reducimos el largo de palabras que repiten caracteres
        self.reduce_len = reduce_len
        
        # Quitamos @handles de twitter
        self.strip_handles = strip_handles
        
        # Eliminar stopwords
        self.delete_stopwords = stopwords
        
        # Eliminar puntuacion
        self.delete_puntuacion = puntuacion
        
        # Eliminar numeros
        self.delete_numbers = numbers
        
        # Eliminamos tokens que contengan caracteres
        self.delete_token_remove = token_remove
        
        # Lematizar
        self.stemming = stemming

    def tokenize(self, document):
        '''Funcion que tokeniza un unico documento'''
        # Eliminamos caracteres del texto que no se tokenizan bien
        if self.text_remove:
            for ch in remove_from_text:
                document = document.replace(ch, " ")
        
        # Normalizamos y tokenizamos
        tokens = casual_tokenize(document.lower(), reduce_len=self.reduce_len, strip_handles=self.strip_handles)
        
        # Normalizamos emoticons
        for i, token in enumerate(tokens):
            if emoticons.match(token.upper()):
                tokens[i] = token.replace('-', '').replace('=', ':').upper()
        
        # Eliminamos tokens que contengan los siguientes caracteres
        if self.delete_token_remove:
            for ch in token_removal_characters:
                tokens = [x for x in tokens if (ch not in x) or (emoticons.match(x))]

        # Separamos tokens divididos por puntos
        y=[]
        for token in tokens:
            y = y + token.split('.')
        tokens = y
        
        # Separamos tokens divididos por guiones bajos
        y=[]
        for token in tokens:
            y = y + token.split('_')
        tokens = y
        
        # Eliminamos stopwords
        if self.delete_stopwords:
            tokens = [x for x in tokens if x not in stopwords]
        # Eliminamos puntuacion
        if self.delete_puntuacion:
            tokens = [x for x in tokens if x not in puntuacion]
        
        # Eliminamos numeros
        if self.delete_numbers:
            tokens = [x for x in tokens if not re.search(r'\d', x)]

        # Lematizar
        if self.stemming:
            tokens = [lemmatizer.lemmatize(x) for x in tokens]
            tokens = [lemmatizer.lemmatize(x, "v") for x in tokens]
        return tokens
    
    def tokenize_corpus(self, corpus):
        '''Funcion que tokeniza un corpus completo y entrega una lista de tokens'''
        tokens_corpus = [self.tokenize(doc) for doc in corpus]
        return tokens_corpus