#MOTOR DE BUSQUEDA
#Rastreo de sitios a traves de la barra de búsqueda

import requests
from bs4 import BeautifulSoup


class Content:
    '''
    Clase para contenidos de algun articulo de pagina web
    '''
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        print("New article found for topic: {}".format(self.topic))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))
        print("URL: {}".format(self.url))


class Website:
    """
    Clase para la estructura de un sitio web
    """
    def __init__(self, name, url, searchUrl, resultListing,
                 resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:

    def getPage(self, url):
        '''
        Funcion para solicitar codigo fuente html de una url
        '''
        # Crawler se hace pasar por Firefox, desde Ubuntu linux
        header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
        try:
            req = requests.get(url, headers=header)
        except requests.exceptions.RequestException:
            return None
        if req.status_code != 200:  # Error en el request
            print("Hubo un error")
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        '''
        Funcion que realiza una seleccion por CSS selectors
        '''
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            #return childObj[0].get_text() solo entrega el primero
            return '\n'.join(
            [elem.get_text() for elem in childObj])
        return ""

    def search(self, topic, site):
        """
        Busca en un sitio web un tópico
        y registra todas las paginas encontradas
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs["href"]
            # Verifica si es una URL relativa o absoluta.
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("Tenemos un problema!!")
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()


crawler = Crawler()

# siteData = [['O\'Reilly Media', 'http://oreilly.com',
#              'https://ssearch.oreilly.com/?q=', 'article.product-result',
#              'p.title a', True, 'h1', 'section#product-description'],
#             ['Reuters', 'http://reuters.com',
#              'http://www.reuters.com/search/news?blob=',
#              'div.search-result-content', 'h3.search-result-title a',
#              False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
#             ['Brookings', 'http://www.brookings.edu',
#              'https://www.brookings.edu/search/?s=',
#              'div.list-content article', 'h4.title a', True, 'h1',
#              'div.post-body']]

# Base de datos de sitios web
"""
Los campos son, en orden, los siguientes:http://www.gamba.cl/?s=

[ Nombre, url, url de busqueda, listado de resultados,
 url de resultados, url absoluta?, tag titulo, tag contenido]

Todos son CSS selectors a excepcion de, url absoluta, que es booleano
"""
siteData = [['Gamba.cl', 'http://www.gamba.cl/', 'http://www.gamba.cl/?s=',
             'div.listing div.column h2', 'a', True, 'h1',
             'div.post-content [style]:is(p):not(:has(script)), div.post-content strong, div.post-content .twitter-tweet']]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3],
                         row[4], row[5], row[6], row[7]))

topics = ['piñera']

for topic in topics:
    print("GETTING INFO ABOUT: " + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)
