import csv

csvFile = open('test.csv', 'wt+')

try:
    writer = csv.writer(csvFile)
    writer.writerow(('numero_natural', '2 + numero_natural', '2 x numero_natural'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()
