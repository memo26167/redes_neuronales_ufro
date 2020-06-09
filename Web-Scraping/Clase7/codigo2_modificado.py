'''
Éste codigo inicia el webdriver geckodriver de firefox
con la libreria selenium, ingresa a una pagina dinámica con Ajax
Obtiene el resultado en base al codigo fuente con la libreria BeautifulSoup
'''

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

firefox_options = Options()
#firefox_options.add_argument("--headless")
driver = webdriver.Firefox(executable_path='../Webdriver/geckodriver', options=firefox_options)


driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')

# El codigo fuente de la pagina
pageSource = driver.page_source

bs = BeautifulSoup(pageSource, 'html.parser')
print(bs.find(id='content').get_text())

time.sleep(5)
pageSource = driver.page_source

bs = BeautifulSoup(pageSource, 'html.parser')
print(bs.find(id='content').get_text())
driver.close()
