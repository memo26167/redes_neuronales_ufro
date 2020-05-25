# Tarea 1 version 2 para el ramo Curso Redes Neuronales de aprendizaje profundo
# Entrega el texto en negrita de la pagina web
# http://www.pythonscraping.com/pages/warandpeace.html
# Autores: Paz Esparza
#          Guillermo Fonseca
# Cargamos librerias
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Recibimos la informacion de la pagina
html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
# Generamos el objeto Beautifulsoup pero usando el parser html5lib
# ya que preserva la estructura original
bs = BeautifulSoup(html.read(), 'html5lib')


# Funcion que muestra si un tag está en verde o rojo
def verde_o_rojo(tag):
    '''
    Busca si el tag posee una el atributo class.
    Si no lo tiene, estará en negrita y entregamos "False".
    Si lo tiene, entregamos "True" si el atributo es igual a verde o rojo y 
    '''
    if not tag.has_attr('class'):
        return False
    else:
        return tag['class'] == ['green'] or tag['class'] == ['red']

# Buscamos todos los tags que entreguen True a la funcion verde_o_rojo y los eliminamos
for tag in bs.find_all(verde_o_rojo):
    tag.decompose()
print(bs.get_text())
