# Explorar documentacion de BeautifulSoup

from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')


#### BeautifulSoup Objects, tipos de objetos
# Tag objects, tambien con find
tag = soup.body.p
type(tag)
# Name, the name of the tag
tag.name
# Attributes of the tag
tag['class']  # maybe output giftList
tag.attrs  # the dictionary, {id : giftList}

### NavigableString
type(tag.string)

### Bs instances
soup
type(soup)

#******** Navigating Tree ***********#

### First tag of type
soup.head
soup.title
### The first b tag beneath body
soup.body.b

### If we need all "a" tags
soup.find_all('a')

### Contents: tag's childrens in a vector
head_tag = soup.head
head_tag.contents # list of tag objects
title_tag = head_tag.contents[0]
title_tag.contents # gives contents of title_tag

soup.contents[1].name # gives the name of the tag

text = title_tag.contents[0]
#text.contents # Gives ERROR because it is a NavigableString

### Instead of getting a list, we can iterate over the tag's children
for child in soup.children:
    type(child)
    child.name
    # A child could be a Tag or  NavigableString

### Descendants, contents and children only consider direct children
# But a child could contain a children
for child in head_tag.descendants:
    print(child)

### Método string, si un tag tiene un sólo hijo NavigableString
# El string se devuelve con .string
title_tag.string

# Si un tag tiene un sólo hijo que es un tag
# Y éste tiene un sólo hijo NavigableString
head_tag.string # su hijo es title_tag

# Si un tag tiene más de un solo hijo, se devuelve None!!!
print(soup.html.string)
# Pero aun así se pueden buscar strings
for string in soup.strings:
    print(repr(string))

### Método Parent, va al padre de el tag actual
title_tag.parent # su padre es head_tag
# El parent de <html> es BeautifulSoup, y el padre de este es None
# Podemos iterar en los padres, hasta llegar a el objeto BeautifulSoup
link = soup.a
for parent in link.parents:
    if parent is None:
        print(parent)
    else:
        print(parent.name)
    print(type(parent)) # El tipo puede ser un tag o BeautifulSoup

### Método Siblings, podemos ir a los lados, en tags del mismo nivel
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2<d>text3</d></c></b></a>")
print(sibling_soup.b.next_sibling)

link = soup.a # Hay 3 <a href=..> juntos
print(link.next_sibling) # Sin embargo, el hermano de un a, no es otro a, es la coma y \n que separa el uno del otro
# Tambien existe previous_sibling, para el hermano anterior

# Se puede iterar en los siguientes hermanos
for sibling in soup.a.next_siblings:
    print(sibling.name, repr(sibling))
# Tambien se puede iterar en los anteriores hermanos con previous_siblings

### Método next_element, nos entrega el siguiente objeto, tag o string, sin importar si esta dentro de una jerarquia, es decir, lee lineas
last_a_tag = soup.find("a", id="link3")
# Entrega el tag hermano de a
print(last_a_tag.next_sibling)
# Entrega el contenido siguiente de <a>
print(last_a_tag.next_element)
# Existe previous_element
# Tambien podemos iterar con next_elements y previous_elements

#******* Searching the tree *******#
# find_all y find
# Lista de todos los b
soup.find_all('b')

# Con regex
import re
# Imprime todos los tags que empiezan con b
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

# Podemos pasarle una lista a find_all
soup.find_all(["a", "b"])

# Imprime todo lo que puede, excepto texto sin tag
for tag in soup.find_all(True):
    print(tag.name)

# Podemos pasarle una funcion, que entrege True si el argumento satisface, y False si no

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
soup.find_all(has_class_but_no_id)
# Toma los <p> ya que no tienen id, no toma html porq no son class, no toman los <a> porq tienen id
# La función puede ser tan complicada como se quiera
