# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector


class SoloSpider(scrapy.Spider):
    name = 'solo'

    def start_requests(self):
        yield SeleniumRequest(url='https://manyavar.com/Lush-Gajaree-', callback=self.parse)

    def parse(self, response):
        driver = response.request.meta['driver']
        resp = Selector(text=driver.page_source)
        features = resp.xpath('//*[@id="accordionBlock"]/div[1]/div[1]/ul/li/p/text()').getall()
        name = resp.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/h2/text()').get()
        code = resp.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/span/text()').get()
        price = resp.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/div[3]/div[1]/h2/text()').get()
        driver.execute_script("window.scrollTo(0, 500)")
        driver.save_screenshot('page.png')
        yield {
            'Name': name,
            'Price': price,
            'Product Code': code,
            'Features': features

        }
