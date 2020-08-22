# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from shutil import which


class CoinSpider(scrapy.Spider):
    name = 'coin'
    # allowed_domains = ['https://www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']

    def __init__(self):
        # path=which('chromedriver')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path="C:\Webdrivers\chromedriver.exe", options=chrome_options)
        driver.get('https://www.livecoin.net/en/')
        driver.set_window_size(1920, 1080)
        usd = driver.find_element_by_xpath('//div[@class="filterPanelItem___2z5Gb "][3]')
        usd.click()
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        cols = resp.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS ")]')
        # cols=resp.xpath('//div[@class="ReactVirtualized__Table__row tableRow___3EtiS "]')
        for e in cols:
            yield {
                'Currency': e.xpath('.//div[@aria-colindex="1"]/div/text()').get(),
                'Volume': e.xpath('.//div[@aria-colindex="2"]/span/text()').get(),
            }
