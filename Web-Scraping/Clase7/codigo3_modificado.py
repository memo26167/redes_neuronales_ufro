'''
Éste codigo inicia el webdriver geckodriver de firefox
con la libreria selenium, ingresa a una pagina dinámica con Ajax,
en ves de esperar tiempo para recibir nuevas solicitudes
espera que el servidor presente nuevas condiciones con la libreria expected_conditions
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

firefox_options = Options()
#firefox_options.add_argument("--headless")

# Abre navegador
driver = webdriver.Firefox(executable_path='../Webdriver/geckodriver', options=firefox_options)

# Solicita pagina
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')

# Espera a que el servidor entregue el elemento de boton
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadedButton')))
finally:
    print(driver.find_element_by_id('content').text)
    driver.close()
