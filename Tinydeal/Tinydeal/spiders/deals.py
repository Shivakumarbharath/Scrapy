# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['www.tinydeal.com']

    # start_urls = ['https://www.tinydeal.com/specials.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.tinydeal.com/specials.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
        })

    def parse(self, response):

        others = response.xpath('//li[@class="productListing-even"]')
        for e in others:
            name = e.xpath(".//a[2]/text()").get()
            link = e.xpath(".//a[2]/@href").get()
            price = e.xpath(".//div/span[@class='productSpecialPrice fl']/text()").get()
            mainprice = e.xpath(".//div/span[@class='normalprice fl']/text()").get()
            yield {
                'name': name,
                'link': link,
                'Special Price': price,
                "normal price": mainprice,
                'User-Agent': response.request.headers['User-Agent']  # To access the user agent
            }

            next_page = response.xpath('//a[@class="nextPage"]/@href').get()
            if next_page:  # check if there is next page and then only yield
                yield scrapy.Request(url='https://www.tinydeal.com/specials.html', callback=self.parse, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
                })
