import scrapy
from bs4 import BeautifulSoup
from moyo.SeleniumRequest import SeleniumRequest
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.http import JsonRequest
from scrapy.utils.serialize import ScrapyJSONEncoder

from moyo.items import MoyoItem

class MoyoSpider(scrapy.Spider):
    name = 'moyo'
    allowed_domains = ['www.moyo.ua']
    BASE_URL = 'https://www.moyo.ua'
    start_urls = ['https://www.moyo.ua/comp-and-periphery/notebooks/']
    encode = ScrapyJSONEncoder().encode
    temporary_item = {}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        last_page = int(soup.find(class_="pagination js-catalog-pagination").find_all('li')[-1].find('a').getText())
        print(last_page)
        for i in range(1, last_page + 1):
            yield scrapy.Request(
                url=f'https://www.moyo.ua/comp-and-periphery/notebooks/?page={i}',
                callback=self.parse_notebooks
            )


    def parse_notebooks(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        catalog = soup.find(class_="catalog_products js-products-list").find_all(class_="product-item")

        for notebook in catalog:
            content = notebook.find(class_="product-item_content")
            content_wrapper = content.find(class_="product-item_content_wrap")
            model = content_wrapper.find('a').getText()
            link = content_wrapper.find('a').get('href')
            price = content.find(class_="product-item_price").find(class_="product-item_price_current").getText()
            image = notebook.find(class_="product-item_img").find(class_="first-image").get('src')

            self.temporary_item = {
                "model": model.strip(),
                "price": price.replace('\xa0', ' ').strip(),
                "link": f'{self.BASE_URL}{link}',
                "image_url": image,
            }

            yield MoyoItem(
                model=model.strip(),
                price=price.replace('\xa0', ' ').strip(),
                link=f'{self.BASE_URL}{link}',
                image_url=image
            )


    def create_item(self, failure):
        return JsonRequest(
            url='http://localhost:3000/item',
            method='POST',
            body=self.encode(self.temporary_item),
            dont_filter=True
        )

    def update_item(self, responce):
        return JsonRequest(
            url='http://localhost:3000/item',
            method='PUT',
            body=self.encode(self.temporary_item),
            dont_filter=True
        )