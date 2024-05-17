import scrapy
from ..items import AmazonPDPItem
from scraperapi_sdk import ScraperAPIClient
client = ScraperAPIClient('<Your Api  KEy>')
from scrapy_redis.spiders import RedisSpider

API = False

class Amazonpdp(RedisSpider):
    def __init__(self, asin=None, *args, **kwargs):
        super(Amazonpdp, self).__init__(*args, **kwargs)
        self.asin =asin
    name = "amazonpdp"
    allowed_domains = ["amazon.com"]
    redis_key = 'asins_queue:start_urls'
    redis_batch_size = 16
    max_idle_time = 10

    # def start_requests(self):
    #     if API:
    #         yield scrapy.Request(client.scrapyGet(f"https://www.amazon.com/dp/{self.asin}/ref=cm_cr_arp_d_product_top?ie=UTF8&th=1"))
    #     else:
    #         yield scrapy.Request(f"https://www.amazon.com/dp/{self.asin}/ref=cm_cr_arp_d_product_top?ie=UTF8&th=1")

    def parse(self, response):
        # item_obj = AmazonPDPItem()
        yield {
            'product_url': response.url,
            'product_name': response.css('#productTitle::text').get().strip(),
            'price': response.css('.apexPriceToPay span::text').get(),
            'shortdescription': response.css('#productFactsDesktopExpander li span::text').getall(),
            'longdescription': response.css('#productDescription span::text').get(),
            'aplus':response.css('#aplus h2::text').get()
        }