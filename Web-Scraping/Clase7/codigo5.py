from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\Alejandro-PC\Desktop\Cursos\Web Scraping y NLP\chromedriver',options=chrome_options)
driver.get('http://pythonscraping.com/pages/javascript/redirectDemo1.html')
try:
    bodyElement = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, '//body[contains(text(), "This is the page you are looking for!")]')))
    print(bodyElement.text)
except TimeoutException:
    print('No se encontró el elemento')