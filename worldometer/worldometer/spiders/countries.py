# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/population/']

    def parse(self, response):

        # To scrap the title
        # title=response.xpath('//h1/text()')
        countries = response.xpath('//ul/li/a')[23:-3]
        for i, country in enumerate(countries):
            name = country.xpath(
                './/text()').get()  # whenever the selector object is used to select a different x path .// is used
            country_link = country.xpath('.//@href').get()
            # we have to join the link with the absolute host
            url = response.urljoin(country_link)
            # If the response must be accesed then use response.follow
            # Send in to different function for each link

            yield response.follow(url=url, callback=self.parse_country, meta={'country name': name})
            '''
        To pass information between two parse methods we use requests meta
        there fore meta is used
'''

    def parse_country(self, response):
        name = response.request.meta['country name']  # To get that info from previous parse method
        # Note for scrapy.Request it is upper case R

        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        # To get the rows of the table
        for e in rows:
            year = e.xpath('.//td[1]/text()').get()
            population = e.xpath('.//td[2]/strong/text()').get()
            yield {'country name': name,

                   'year': year,
                   'population': population
                   }


'''
To get the countries and its links from the site
        countries = response.xpath('//ul/li/a')[14:-3]
        for country in countries:
            name=country.xpath('.//text()').get()# whenever the selector object is used to select a different x path .// is used
            country_link=country.xpath('.//@href').get()
            yield {
                'Country Name': name,
                'countries': country_link
            }


# These settings are needed if the requests are to be done in order
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

CONCURRENT_REQUESTS = 1
This only if order is very very importent as it requests 32 at a time
'''
