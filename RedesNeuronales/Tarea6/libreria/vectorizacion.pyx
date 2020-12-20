from __future__ import print_function
import numpy as np

class Vectorizador:
    '''Objeto que vectoriza'''
    def __init__(self, tokenizer, wv, maxlen, dtype=np.float32, scaling=[0, 1]):
        self.tokenizer = tokenizer
        self.wv = wv
        self.maxlen = maxlen
        self.dtype = dtype
        self.scaling = scaling

    def pad_trunc(self, X, zero):
        maxlen = self.maxlen
        new_X = []
        #le asignamos el valor minimo, para que al normalizar, de vector de 0s
        #de tamaño igual a las dimensiones del espacio semantico
        zero_vector = np.array([[zero]*self.wv.vector_size]).astype(self.dtype)
        
        for sample in X:
            #print(sample)
            num_token = len(sample)
            if num_token > maxlen:
                #Se guardan los primeros *maxlen* tokens
                #print(f"Largo de doc: {len(sample)}")
                temp = sample[:maxlen]
            elif num_token < maxlen:
                #Agregamos *maxlen - num_token* tokens
                temp = sample
                additional_elems = maxlen - num_token
                temp = np.concatenate((temp, np.tile(zero_vector, (additional_elems,1)))).astype(self.dtype)
            else:
                temp = sample
            new_X.append(temp)
        return new_X
    
    def normalizar(self, X):
        m = (self.scaling[1]-self.scaling[0])/(np.nanmax(X) - np.nanmin(X))
        X = m*(X - np.nanmin(X)) + self.scaling[0]
        #X = (X - np.nanmin(X)) / (np.nanmax(X) - np.nanmin(X))
        return X

    def vectorizacion(self, corpus):
        X = []
        for doc in corpus:
            tokens = self.tokenizer(doc)
            vectors = np.array([self.wv[w].astype(self.dtype) for w in tokens if w in self.wv.vocab])
            #print(vectors)
            X.append(vectors)
        # Etiquetamos con NaN, aquellos tokens que agregamos, para no considerarlos en la normalizacion
        mini = np.nan
        X = self.pad_trunc(X, mini)
        X = np.array(X,dtype=self.dtype)
        X = self.normalizar(X)
        # Convertimos los NaN en 0
        X = np.nan_to_num(X)
        return X