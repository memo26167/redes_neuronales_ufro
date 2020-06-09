from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\Alejandro-PC\Desktop\Cursos\Web Scraping y NLP\chromedriver', options=chrome_options)
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
#time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()