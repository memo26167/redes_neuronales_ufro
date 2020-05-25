# Crawler
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("https://es.wikipedia.org/wiki/Georg_Cantor")
bs = BeautifulSoup(html)

#  Extraer links de una pagina de wikipedia
x = []
for link in bs.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        x.append(link.attrs['href'])

# Sin embargo todo el contenido de la paginta se encuentra en la etiqueta div de id= bodyContent

for link in bs.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    # regex que busca links de wikipedia
    if 'href' in link.attrs:
        print(link.attrs['href'])

# construccion de crawler
import datetime
import random

# Establece el generador de numeros aleatorios con seed de la hora actual del sistema
random.seed(datetime.datetime.now())


def getLinks(articleUrl):
    # Obtiene links de wikipedia
    html = urlopen("https://en.wikipedia.org" + articleUrl)
    bs = BeautifulSoup(html)
    return bs.find("div", {"id": "bodyContent"}).findAll("a", href = re.compile("^(/wiki/)(.)*$"))

links = getLinks("/wiki/Richard_Feynman")
# Máximo de 5 links
for i in range(5):
    print(links[i])

i = 0
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    i = i + 1
    if i < 5:
        links = getLinks(newArticle)
    else:
        break
