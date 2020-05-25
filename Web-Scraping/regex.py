from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

#html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html.read(), 'html.parser')

patron = re.compile(r'\.\./img/gifts/img.*\.jpg')
nameList = bs.find_all('img', {'src': patron})

for name in nameList:
    print(name['src'])
