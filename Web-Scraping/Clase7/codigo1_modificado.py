'''
Éste codigo inicia el webdriver geckodriver de firefox
con la libreria selenium, ingresa a una pagina dinámica con Ajax
e imprime diferentes resultados esperando la respuesta del servidor
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


# Se carga el webdriver de firefox con opciones de arranque
firefox_options = Options()
#firefox_options.add_argument("--headless")
driver = webdriver.Firefox(executable_path='../Webdriver/geckodriver', options=firefox_options)

# Se solicita pagina
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
print(driver.find_element_by_id('content').text)
# Se espera e imprime otra ves las mismas etiquetas, cambió la pagina?
time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()
