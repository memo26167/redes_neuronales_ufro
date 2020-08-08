from nltk.tokenize import TreebankWordTokenizer

sentence = """La UFRO está en Temuco, y yo estudio en la ufro."""
tokenizer = TreebankWordTokenizer()
tokens = tokenizer.tokenize(sentence.lower())
tokens

from collections import Counter

#obtenemos un diccionario
bag_of_words = Counter(tokens)
bag_of_words

bag_of_words.most_common()

times_ufro_appears = bag_of_words['ufro']
print(times_ufro_appears)

num_unique_words = len(bag_of_words)
print(num_unique_words)

tf = times_ufro_appears / num_unique_words
print(tf)
