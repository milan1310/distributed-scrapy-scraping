# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonDistributionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AmazonPDPItem(scrapy.Item):
    title = scrapy.Field()
    total_rating = scrapy.Field()
    num_images = scrapy.Field()
    brand = scrapy.Field()
    is_variation = scrapy.Field() 
    bulletings = scrapy.Field()
    buy_box_winner = scrapy.Field()
    price = scrapy.Field()
    asin_number = scrapy.Field()
    product_url = scrapy.Field()