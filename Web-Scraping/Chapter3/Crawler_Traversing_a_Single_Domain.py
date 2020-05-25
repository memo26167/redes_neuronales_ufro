# Crawler escrito de el libro Web Scraping with Python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

# Nueval semilla random cada dia
random.seed(datetime.datetime.now())

# Funcion que obtiene links
def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
    bs = BeautifulSoup(html, 'html5lib')
    # Nos entrega una lista de todos los links (<a>) dentro de div, que no contienen  ":"
    return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))

# Obtener links de la pagina de Kevin Bacon
links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    # Obtenemos algun link random, de la lista de links, su atributo href que es el link
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    # Imprimimos el nuevo link
    print(newArticle)
    # Obtenemos los links del nuevo artículo
    links = getLinks(newArticle)
