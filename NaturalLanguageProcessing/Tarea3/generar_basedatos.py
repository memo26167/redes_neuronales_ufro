# MOTOR DE BUSQUEDA
# Rastreo de sitios a traves de la barra de búsqueda

import requests
from bs4 import BeautifulSoup
import csv

class Content:
    '''
    Clase para contenidos de algun articulo de pagina web
    '''
    def __init__(self, topic, url, title, body, date):
        self.topic = topic
        self.title = title
        self.body = body
        self.date = date
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
                 resultUrl, absoluteUrl, titleTag, bodyTag, dateTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.dateTag = dateTag


class Crawler:

    def getPage(self, url):
        '''
        Funcion para solicitar codigo fuente html de una url
        '''
        #! Crawler se hace pasar por Firefox, desde Ubuntu linux
        header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
        try:
            req = requests.get(url, headers=header)
        except requests.exceptions.RequestException:
            return None
        if req.status_code != 200:  #! Posible error en el request
            print("Hubo un error")
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        '''
        Funcion que realiza una seleccion por CSS selectors
        '''
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            # Solo entrega el primero elemento del vector de cada selector
            #return childObj[0].get_text()
            # Entrega todos los elementos del vector de cada selector
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
        registryContents = []
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
            date = self.safeGet(bs, site.dateTag)
            if title != '' and body != '':
                content = Content(topic, url, title, body, date)
                content.print()
                registryContents.append(content)
        return registryContents


def writeArticles(filename, articles, max_num_articles):
    csvFile = open(filename, 'wt+', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    articles_in_csv = 0
    try:
        for article in articles: #filas
            if articles_in_csv < max_num_articles:
                print(articles_in_csv)
                csvRow = [article.body]
                writer.writerow(csvRow)
            articles_in_csv += 1
    finally:
        csvFile.close()

crawler = Crawler()


# Base de datos de sitios web
"""
Los campos son, en orden, los siguientes:

[ Nombre, url, url de busqueda, listado de resultados,
 url de resultados, url absoluta?, tag titulo, tag contenido, tagfecha]

Todos son CSS selectors a excepcion de, url absoluta, que es booleano
"""
siteData = [
    ['El ciudadano',
     'https://www.elciudadano.com/',
     'https://www.elciudadano.com/?s=',
     'div.td_module_16 ',
     'h3.entry-title a', True, 'h1.tdb-title-text',
      'div.td-post-content p', 'time'],
    ['Gamba.cl',
     'http://www.gamba.cl/',
     'http://www.gamba.cl/?s=',
     'div.listing div.column h2',
     'a', True, 'h1',
     'div.post-content [style]:is(p):not(:has(script)):not([href="https://www.facebook.com/gambanoticias/"]), div.post-content strong:not(:has(a[href="https://www.facebook.com/gambanoticias/"])), div.post-content .twitter-tweet',
     'time.value-title']
]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3],
                         row[4], row[5], row[6], row[7], row[8]))

topics = ['Piñera', 'AFP']
max_num_articles = 50

# Se guarda cada articulo, de clase Contents
articles = []
for topic in topics:
    print("GETTING INFO ABOUT: " + topic)
    for targetSite in sites:
        articles.extend(crawler.search(topic, targetSite))

writeArticles('articulos.csv', articles, max_num_articles)
