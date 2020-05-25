# No volver a una pagina anterior

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set() # Como una lista, pero de elementos unicos
def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html5lib')
    for link in bs.find_all('a', href = re.compile('^(/wiki/)')):
        if 'href' in link.attrs: # puede no tener href
            if link.attrs['href'] not in pages:
                # Encontramos una nueva pagina
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks('')
