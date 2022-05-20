import scrapy


class HotlineItem(scrapy.Item):
    model = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
