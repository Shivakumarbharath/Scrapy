# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector


class SlicksSpider(scrapy.Spider):
    name = 'slicks'

    def start_requests(self):
        yield SeleniumRequest(url='https://slickdeals.net/computer-deals/', screenshot=True, callback=self.parse)

    def parse(self, response):
        response = Selector(text=response.body)

        products = response.xpath('//ul[@class="dealTiles categoryGridDeals"]/li')

        for product in products:
            yield {

                'Name': product.xpath('.//div/div/div[1]/div[1]/div/a/text()').get(),
                'URL': 'https://slickdeals.net/computer-deals' + product.xpath(
                    './/div/div/div[1]/div[1]/div/a/@href').get(),
                "price": product.xpath('normalize-space(.//div/div/div[1]/div[2]/div[2]/div/text())').get()

            }
        next_page = response.xpath('//*[@id="fpMainContent"]/div[6]/a[@data-role="next-page"]/@href').get()
        if next_page:
            absolute_Path = f'https://slickdeals.net{next_page}'
            print(absolute_Path[-2])
            yield SeleniumRequest(url=absolute_Path, callback=self.parse)
