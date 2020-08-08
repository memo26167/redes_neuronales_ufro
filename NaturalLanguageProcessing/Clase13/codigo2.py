from collections import Counter
from nltk.tokenize import TreebankWordTokenizer
from nlpia.data.loaders import kite_text


print(kite_text)

tokenizer = TreebankWordTokenizer()
tokens = tokenizer.tokenize(kite_text.lower())
token_counts = Counter(tokens)
print(token_counts)
print(len(token_counts))

import nltk
#nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
tokens = [x for x in tokens if x not in stopwords]
puntuacion = set((',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']'))
tokens = [x for x in tokens if x not in puntuacion]
kite_counts = Counter(tokens)
print(kite_counts.most_common()[:10])


print(len(kite_counts))

#VECTORIZANDO EL RECUENTO DE LA FRECUENCIA DE PALABRAS
document_vector = []
doc_length = len(tokens)

for key, value in kite_counts.most_common():
    document_vector.append(value / doc_length)

print(document_vector)

