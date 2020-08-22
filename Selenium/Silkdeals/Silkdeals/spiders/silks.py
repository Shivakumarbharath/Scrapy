# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

from selenium.webdriver.common.keys import Keys


class SilksSpider(scrapy.Spider):
    name = 'silks'

    def start_requests(self):
        yield SeleniumRequest(url='https://duckduckgo.com', screenshot=True, callback=self.parse)

    def parse(self, response):
        # To take a screenshot
        # img=response.request.meta['screenshot']
        #
        # with open('sc.png','wb') as f:
        #     f.write(img)

        # To get the driver object from the start request
        driver = response.request.meta['driver']

        search = driver.find_element_by_id('search_form_input_homepage')
        search.send_keys('Hello World')

        # Using the Enter key in keyboard
        search.send_keys(Keys.ENTER)
        # driver.find_element_by_id('search_button_homepage').click()

        # To take a screenchot
        driver.save_screenshot('after_search.png')

        # To get the links and to select the xpaths
        # Conversion to selector object
        html = Selector(text=driver.page_source)

        links = html.xpath("//a[@class='result__a']")

        for e in links:
            yield {
                "Url": e.xpath('.//@href').get()
            }
