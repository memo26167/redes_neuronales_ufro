# Modelo de Web Crawling
import requests
from bs4 import BeautifulSoup


class Content:
    """
    Clase base para paginas y artículos
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        '''
        Imprime atributos de Content
        '''
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY: \n{}".format(self.body))


class Website:
    """
    Contiene informacion de la estructura del sitio web
    no de una URL en específico
    """
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    """
    Define la clase Crawler, que se crea con métodos para 
    raspar páginas
    """

    def getPage(self, url):
        """
        INtenta obtener páginas
        """
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html5lib')

    def safeGet(self, pageObj, selector):
        """
        Funcion que intenta entregar el contenido de un
        string de un objeto BeautifulSoup con un selector.
        Se entrega un string vacío si no se encuentra nada
        con ese selector.
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join(
            [elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, site, url):
        """
        Extrae contenidos de una URL y un sitio dado
        """
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

# El crawler que se ejecutará
crawler = Crawler()
# Base de datos
'''
Nombre, sitio principal, Título, Body
'''
siteData = [
    ['Ufro Medios', 'http://www.ufromedios.cl/',
     'h1 span', 'div.entry .share-post ~ *'
     ]
]

websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'http://www.ufromedios.cl/reporte-de-seremi-de-salud-informa-una-mujer-fallecida-en-renaico-y-19-contagios-nuevos-en-la-araucania/')
