# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys


class SherwaniSpider(scrapy.Spider):
    name = 'sherwani'

    def start_requests(self):
        yield SeleniumRequest(url='https://manyavar.com/search?q=Sherwani', callback=self.parse)

    def parse(self, response):
        driver = response.request.meta['driver']

        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        resp = Selector(text=html)
        number = int(resp.xpath('//*[@id="filterDatarow"]/div/div[2]/div/div/span/b/text()').get())
        print(number)
        element = resp.xpath('//*[@id="div-scroll"]/div/div')

        while len(element) < number:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(3)
            resp = Selector(text=driver.page_source)
            element = resp.xpath('//*[@id="div-scroll"]/div/div')

        driver.save_screenshot('start.png')

        for e in element[:-2]:
            # yield scrapy.Request(url='https://manyavar.com'+e.xpath('.//div/a/@href').get(),callback=self.parse_Product)
            yield {'URL': e.xpath('.//div/a/@href').extract()}

    def parse_Product(self, response):
        # driver2 = response.request.meta['driver']
        resp2 = Selector(text=response.body)
        features = resp2.xpath('//*[@id="accordionBlock"]/div[1]/div[1]/ul/li/p/text()').getall()
        name = resp2.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/h2/text()').get()
        code = resp2.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/span/text()').get()
        price = resp2.xpath('//*[@id="productDIv"]/div/div[2]/div[1]/div[1]/div[3]/div[1]/h2/text()').get()

        yield {
            'Name': name,
            'Price': price,
            'Product Code': code,
            # 'Features':features

        }
