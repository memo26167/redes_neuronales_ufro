from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()
docs = ["La UFRO está en Temuco, y yo estudio en la ufro."]
docs.append("La Ufro es una universidad estatal.")
docs.append("Facultad de Ingeniería y Ciencia, Ufro.")
print(docs)

doc_tokens = []
for doc in docs:
    doc_tokens += [sorted(tokenizer.tokenize(doc.lower()))]
print(doc_tokens)
print(len(doc_tokens[0]))

all_doc_tokens = sum(doc_tokens, [])
print(all_doc_tokens)
print(len(all_doc_tokens))

lexicon = sorted(set(all_doc_tokens))
print(len(lexicon))
print(lexicon)

from collections import OrderedDict

zero_vector = OrderedDict((token, 0) for token in lexicon)
zero_vector

import copy
from collections import Counter
"""
copy.copy () crea una copia independiente, una instancia separada de su vector cero, en lugar de reutilizar 
una referencia (puntero) a la ubicación de memoria del objeto original. De lo contrario, simplemente estaría 
sobrescribiendo el mismo zero_vector con nuevos valores en cada ciclo, y no tendría un cero nuevo en cada 
pasada del ciclo.
"""
doc_vectors = []
for doc in docs:
    vec = copy.copy(zero_vector)
    tokens = tokenizer.tokenize(doc.lower())
    token_counts = Counter(tokens)
    for key, value in token_counts.items():
        vec[key] = value / len(lexicon)
    doc_vectors.append(vec)

print(doc_vectors[0])

vectors = []
for vec in doc_vectors:
    vectors.append([val for val in vec.values()])

print(vectors[0])


