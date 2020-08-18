# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MotomobilesSpider(CrawlSpider):
    name = 'MotoMobiles'
    # allowed_domains = ['https://www.flipkart.com/search?q=motorola+mobiles&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_5_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_5_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=motorola+mobiles&requestId=addf7a71-aa8d-4727-a997-d727119402f7&as-backfill=on']
    start_urls = [
        'https://www.flipkart.com/search?q=motorola+mobiles&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_5_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_5_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=motorola+mobiles&requestId=addf7a71-aa8d-4727-a997-d727119402f7&as-backfill=on/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='bhgxx2 col-12-12']/div[@class='_3O0U0u']/div/div/a"),
             callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="_3fVaIS"]'))
    )

    def parse_item(self, response):

        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        name = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()
        specialPrice = response.xpath("//div[@class='_1vC4OE _3qQ9m1']/text()").get()
        if response.xpath('//div[@class="_3auQ3N _1POkHg"]/text()[2]').get() != None:
            mrpPrice = '₹' + response.xpath('//div[@class="_3auQ3N _1POkHg"]/text()[2]').get()
        else:
            mrpPrice = specialPrice

        yield {
            'Title': name,
            'Offer Price': specialPrice,
            'MRP': mrpPrice
        }
