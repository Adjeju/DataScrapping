from bs4 import BeautifulSoup
from requests import get

LINK = 'https://www.moyo.ua/comp-and-periphery/notebooks/'

page = get(LINK)

soup = BeautifulSoup(page.content, 'html.parser')
catalog = soup.find(class_="catalog_products js-products-list").find_all(class_="product-item")

for c in catalog:
    content = c.find(class_="product-item_content")
    content_wrapper = content.find(class_="product-item_content_wrap")
    model = content_wrapper.find('a').getText()
    print(model)