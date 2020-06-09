from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print('Tiempo de espera después de 10 segundos y regreso')
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name('html')
        except StaleElementReferenceException:
            return
        
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\Alejandro-PC\Desktop\Cursos\Web Scraping y NLP\chromedriver',options=chrome_options)
driver.get('http://pythonscraping.com/pages/javascript/redirectDemo1.html')
waitForLoad(driver)
print(driver.page_source)