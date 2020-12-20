#!/usr/bin/env python
# coding: utf-8

# ![imagen.png](attachment:imagen.png)

# ![imagen.png](attachment:imagen.png)

# In[1]:


from nltk.util import ngrams
from nltk.tokenize.casual import casual_tokenize

import nltk
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

puntuacion = set((',', '.', '--', '-', '¡', '!', '¿', '?', ':', ';', '``', "''", '(', ')', '[', ']', '«',
                  '»', '/', '—', '_', '..', '+', '…', '‘', '’', '–', '%', '“', '”', '″', '"', '·', '|',
                  '<', '>', '=', '*', '°'))

class n_gram_tokenizer:
    def __init__(self, n_order=2):
        self.n_order = n_order

    def tokenize(self, document):
        tokens = casual_tokenize(document.lower())

        # Eliminamos stopwords
        tokens = [x for x in tokens if x not in stopwords]
        # Eliminamos puntuacion
        tokens = [x for x in tokens if x not in puntuacion]

        #lista de ngramas, en cada ngrama hay una tupla que contiene sus tokens
        n_grams = list(ngrams(tokens, self.n_order))
        n_grams = [" ".join(x) for x in n_grams]

        return n_grams


# In[2]:



# Definimos la funcion para analisis de discriminacion lineal (LDA)
import numpy as np

from nlpia.data.loaders import get_data
import pandas as pd

#Esta línea ayuda a mostrar la columna ancha de texto SMS dentro de una impresión de Pandas DataFrame.
sms = get_data('sms-spam')


# Alternativamente al metodo de tf_idf_vectorizer, se puede utilizar libreria sklearn y utilizador TfidVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

tokenizacion = n_gram_tokenizer(n_order=2).tokenize

tfidf_model = TfidfVectorizer(tokenizer=tokenizacion)

# sus filas son los documentos y sus columnas cada token del corpus, cada valor representara el valor de TF-IDF
tfidf_docs = tfidf_model.fit_transform(raw_documents=sms.text).toarray()

# Iniciaremos un vector para mostrar con True or False, para ver si un documento es spam o no.
spam_labels = sms.spam.astype(bool).values


# In[6]:


#Separamos el conjunto de datos en un set de entrenamiento y otro set de teste
from sklearn.model_selection import train_test_split

vector_train, vector_test, label_train, label_test = train_test_split(tfidf_docs, spam_labels, test_size=0.5, random_state=5)


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)



label_pred = lda.fit(vector_train, label_train).predict(vector_train)


# In[11]:





