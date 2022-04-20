import scrapy


class MoyoItem(scrapy.Item):
    model = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    image_url = scrapy.Field()
