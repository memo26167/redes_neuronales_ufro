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


from collections import Counter
from collections import OrderedDict
import copy
import math

def tf_idf_vectorizer(corpus, tokenizer):
    '''
    Funcion que realiza vectorizacion TF-IDF
    Entradas:
        Corpus es una lista de documentos, que a su ves, son listas de una palabra.
        Tokenizer es una funcion, que toma un documento y entrega una lista de tokens.
    Salida:
        Diccionario ordenado, en la cual se le asigna a cada token un numero.
    '''
    tokens_in_doc = []
    num_tokens_in_doc = []

    for doc in corpus:
        tokens = tokenizacion(doc)
        token_counts = Counter(tokens)
        tokens_in_doc.append(tokens)
        num_tokens_in_doc.append(len(token_counts))

    # Todos los token de los docs
    all_doc_tokens = sum(tokens_in_doc, [])
    # Léxico
    lexicon = sorted(set(all_doc_tokens))
    # Diccionario que contiene en cuantos documentos aparece cada token
    num_documents_containing_token = {}
    for token in lexicon:
        containing_token = 0
        for i, doc in enumerate(corpus):
            if token in tokens_in_doc[i]:
                containing_token += 1
        num_documents_containing_token.update({token: containing_token})
    # Calculo TF-IDF
    tfidf_vectors = []
    zero_vector = OrderedDict((token, 0) for token in lexicon)
    for i, doc in enumerate(corpus):
        vec = copy.copy(zero_vector)
        tokens = tokenizacion(doc)
        token_counts = Counter(tokens)
        for token, value in token_counts.items():
            tf = value / num_tokens_in_doc[i]
            idf = len(corpus) / num_documents_containing_token[token]
            vec[token] = tf * math.log(idf)
        tfidf_vectors.append(vec)
    return tfidf_vectors


# In[3]:


# Definimos la funcion para analisis de discriminacion lineal (LDA)
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix

def LDA_recta(vector, label):
    '''
    Funcion que calcula la recta que une los centroides,
    Entradas:
        vector: array en el que sus filas son vectores, a los cuales se les calculará dos centroides
        label : array de booleanos, que categoriza a cada vector
    Salida:
        recta : array con dimension igual a los vectores a categorizar
    '''
    #Calculamos los centroides en las dimensiones de los tokens de entrenamiento
    centroid = vector[label].mean(axis=0)
    n_centroid = vector[~label].mean(axis=0)

    #vector recta, que une los dos centroides
    recta = centroid - n_centroid

    return recta

def lda_matriz_confusion(recta, vector, label, threshold=0.5):
    '''
    Funcion que calcula la matriz de confusion y la precision del metodo LDA
    Entradas:
        recta : la recta que discrimina los vectores
        vector: array en el que sus filas son vectores, los cuales se discriminarán
        label : array de booleanos, que categoriza a cada vector, se usa para discernir falsas discriminaciones (FP, FN)
        threshold: tolerancia de discriminacion
    '''
    score = vector.dot(recta)

    lda_score = MinMaxScaler().fit_transform(score.reshape(-1,1))

    #Si el score es mayor al threshold, entonces se discrimina
    predict = (lda_score > threshold).astype(int).reshape(-1,)

    print('suma predicciones', sum(predict), predict)
    label = label.astype(int)
    print('suma original    ', sum(label))
    print('total', len(label))

    # matrix = confusion_matrix(label, predict).ravel

    # print(confusion_matrix(label, predict))
    # print(confusion_matrix(label, predict).ravel())
    tn, fp, fn, tp = confusion_matrix(label, predict).ravel()

    print(f"Verdaderos Positivos: {tp} son spam y se clasificaron como spam")
    print(f"Verdaderos Negativos: {tn} no son spam y se clasificaron como no spam")
    print(f"Falsos     Negativos: {fn} son spam y se clasificaron como no spam")
    print(f"Falsos     Positivos: {fp} no son spam y se clasificaron como spam")

    acc = (tp + tn)/(tp+tn+fp+fn)
    print(f"Con una precision de {acc} \n")


# In[4]:


from nlpia.data.loaders import get_data
import pandas as pd

#Esta línea ayuda a mostrar la columna ancha de texto SMS dentro de una impresión de Pandas DataFrame.
pd.options.display.width = 120
sms = get_data('sms-spam')


# In[5]:


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

recta = LDA_recta(vector_train, label_train)


# In[7]:


lda_matriz_confusion(recta, vector_train, label_train, threshold=0.3)
lda_matriz_confusion(recta, vector_test, label_test, threshold=0.3)


# In[9]:


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)


# In[10]:


label_pred = lda.fit(vector_train, label_train)


# In[11]:


label_pred.predict(vector_train)


# In[12]:


vector_train.shape


# In[20]:


35613**2/1000/1000/1000*64/8


# In[ ]:




