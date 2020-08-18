# -*- coding: utf-8 -*-
import scrapy


class SpecsSpider(scrapy.Spider):
    name = 'specs'
    # allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        all = response.xpath('//div[@class="col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center"]')

        for e in all:

            url = e.xpath('.//div[@class="product-img-outer"]/a/@href').get()
            if url is not None:
                yield response.follow(url=url, callback=self.parse_each, meta={'url': url})

        nextpage = response.xpath('(//a[@class="page-link"])')[-1]
        if nextpage:
            yield response.follow(url=nextpage, callback=self.parse)

    def parse_each(self, response):
        imgs = response.xpath('//img[@class="img-fluid product-banner"]/@src').getall()
        url = response.request.meta['url']
        title = response.xpath('//h1[@class="product-info-title"]/text()').get()
        price = response.xpath('//span[@class="product-price-original"]/text()').get()

        yield {
            'Image links': imgs,
            'Url': url,
            'Title': title,
            'Price ': price
        }
