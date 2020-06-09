# Codigo que captura una tabla de un sitio web y lo guarda en un csv

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html5lib')

#Primera tabla
table = bs.findAll('table')[0]
#Las filas están bajo la etiqueta tr
rows = table.findAll('tr')

#nombre del archivo, escritura, codificacion del sitio(se encuentra bajo la primera etiqueta del HEAD)
csvFile = open('editors1.csv', 'wt+', encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
	#las celdas estan bajo td y th
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()

import pandas as pd
df = pd.read_csv('editors1.csv')

#tamaño
df.shape
#primerafila
df[:0]

#mostrar sin la primera fila
df=pd.read_csv('editors1.csv', header=1)