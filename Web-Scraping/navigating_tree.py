from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

# Print items of the first category below table, doesnt separate items inside childrens
for child in bs.find('table', {'id': 'giftList'}).children:
    print(child)

# Print items of all categorys below table
for descendant in bs.find('table', {'id': 'giftList'}).descendants:
    print(descendant)

# Print those tr items next from the first item inside the table (excluding the first)
for sibling in bs.find('table', {'id': 'giftList'}).tr.next_siblings:
    print(sibling)
# It also exist previous_siblings

# If we need to find and item above of another children's item, we can
# 1. Find the children
# 2. Go to the parent
# 3. Go to previous sibling
print(bs.find('img', {'src': '../img/gifts/img1.jpg'})
      .parent.previous_sibling.get_text())

