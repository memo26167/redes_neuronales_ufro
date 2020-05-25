# Tarea 1 para el ramo Curso Redes Neuronales de aprendizaje profundo
# Entrega el texto en negrita de la pagina web
# http://www.pythonscraping.com/pages/warandpeace.html
# Autores: Paz Esparza
#          Guillermo Fonseca
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(), 'html.parser')

print(bs.find('h1').get_text())
print(bs.find('h2').get_text())
for name in bs.find('div', {'id': 'text'}).p.next_siblings:
    if name.name is None:
        print(name)
# En este texto, los p tiene el siguiente formato
# <p></p>, es por eso que el programa funciona
# Sin embargo, en la pagina, esto no ocurre
# ¿Funcionamiento inesperado? Problema es el parser
# HTML correcto es html5lib !!!
