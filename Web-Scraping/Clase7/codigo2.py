from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\Alejandro-PC\Desktop\Cursos\Web Scraping y NLP\chromedriver', options=chrome_options)
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
pageSource = driver.page_source
time.sleep(3)
bs = BeautifulSoup(pageSource, 'html.parser')
print(bs.find(id='content').get_text())
driver.close()