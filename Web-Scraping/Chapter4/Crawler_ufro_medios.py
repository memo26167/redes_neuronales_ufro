# Crawler de noticias de ufro medios

import requests
from bs4 import BeautifulSoup
import re

def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html5lib')


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

def scrape_ufromedios(url):
    bs = getPage(url)
    title = bs.find("h1").span.text
    entry = bs.find("div", {"class", "entry"})
    lines = entry.find_all(re.compile("^(?!(div|span|script|ul|li|a)).*$"))
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


url = "http://www.ufromedios.cl/reporte-de-seremi-de-salud-informa-una-mujer-fallecida-en-renaico-y-19-contagios-nuevos-en-la-araucania/"
content = scrape_ufromedios(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)
