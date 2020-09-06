# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    imgnum = 1

    def start_requests(self):
        yield SeleniumRequest(url='https://www.amazon.in/', callback=self.parse, headers={'User-Agent': self.user_agent,
                                                                                          "Accept-Encoding": "gzip, deflate",
                                                                                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                                                          "DNT": "1",
                                                                                          "Connection": "close",
                                                                                          "Upgrade-Insecure-Requests": "1"
                                                                                          })

    def parse(self, response):

        try:
            driver = response.request.meta['driver']
            driver.save_screenshot('amzn.png')
            search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
            search.send_keys('HP laptops')

            search.send_keys(Keys.ENTER)
            driver.save_screenshot('check.png')

            resp = Selector(text=driver.page_source)
        except KeyError:
            resp = Selector(text=response.body)

        prods = resp.xpath('''(//span[@data-cel-widget="MAIN-SEARCH_RESULTS"])/div[@class
        ="s-include-content-margin s-border-bottom s-latency-cf-section"]''')
        print(len(prods), 'This is products elements')

        if prods:

            for e in prods:

                name = e.xpath('.//div/div[2]/div[2]/div/div/div/div/div/h2/a/span/text()').get()
                if e.xpath('.//div/div[2]/div[2]/div/div/div/div/div/h2/a/@href').get():
                    url = 'https://www.amazon.in' + e.xpath('.//div/div[2]/div[2]/div/div/div/div/div/h2/a/@href').get()
                else:
                    url = None
                price = e.xpath(
                    './/div/div[2]/div[2]/div/div[2]/div/div/div/div[@class="a-row a-size-base a-color-base"]/div/a/span[1]/span/text()').get()
                mrp = e.xpath(
                    './/div/div[2]/div[2]/div/div[2]/div/div/div/div[@class="a-row a-size-base a-color-base"]/div/a/span[2]/span/text()').get()
                yield {
                    'Name': name,
                    'Url': url,
                    'Offer Price': price,
                    'MRP': mrp,

                }
                # yield scrapy.Request(url=url,callback=self.parse_item,headers={'User-Agent':self.user_agent,
                #                                                                    "Accept-Encoding": "gzip, deflate",
                #                                                                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                #                                                                            "DNT": "1",
                #                                                                            "Connection": "close",
                #                                                                            "Upgrade-Insecure-Requests": "1"
                #                                                                            },dont_filter=False)

                next_page = resp.xpath('//li[@class="a-last"]/a/@href').get()
                print(next_page)
                if next_page:
                    next_url = 'https://www.amazon.in' + next_page
                    print(next_url)
                    yield scrapy.Request(url=next_url[:], callback=self.parse, headers={'User-Agent': self.user_agent,
                                                                                        "Accept-Encoding": "gzip, deflate",
                                                                                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                                                        "DNT": "1",
                                                                                        "Connection": "close",
                                                                                        "Upgrade-Insecure-Requests": "1"
                                                                                        }, dont_filter=False)
        else:
            print('Amazon did not allow pagination', response.url)  # [:-1]+str(int(response.url[-1])+1))

    def parse_item(self, response):

        # driver=response.request.meta['driver']
        # driver.find_element_by_xpath('//*[@id="feature-bullets"]/div/a/span').click()
        self.imgnum += 1
        # driver.save_screenshot(f'getprod{self.imgnum}.png')

        resp = Selector(text=response.body)
        name = resp.xpath('//span[@id="productTitle"]/text()').get().replace('\n', '')
        price = resp.xpath('//span[@id="priceblock_ourprice"]/text()').get()
        mrp = resp.xpath('//span[@class="priceBlockStrikePriceString a-text-strike"]/text()').get()

        save = resp.xpath('//td[@class="a-span12 a-color-price a-size-base priceBlockSavingsString"]/text()').get()
        features = resp.xpath('//div[@id="feature-bullets"]/ul/li/span[@class="a-list-item"]/text()').getall()

        # self.driver.get(response.url)
        # self.driver.find_element_by_xpath('//div[@class="a-row a-expander-container a-expander-inline-container"]/a').click()
        # #features2=Selector(text=self.driver.page_source).xpath('//div[@id="feature-bullets"]/div/div[@aria-expanded="true"]/ul/li/span/text()').getall()
        featuresscrapy = resp.xpath(
            '//div[@id="feature-bullets"]/div/div[@aria-expanded="false"]/ul/li/span/text()').getall()

        yield {

            'Name': name,
            'Price': price,
            'MRP': mrp,
            'Save': save,
            "features ": features,
            "features expanded": featuresscrapy
        }

        # def close(spider, reason):
        #     self.driver.close()
