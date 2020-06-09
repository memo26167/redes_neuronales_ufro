#Clase 6
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img')
#imageLocation = bs.find('a', {'id': 'logo'}).find('img')['src']
i = 0
for image in images:
    i = i + 1
    urlretrieve(image['src'], 'image{}.jpg'.format(i))
