# -*- coding: utf-8 -*-
import scrapy


class DebtratioSpider(scrapy.Spider):
    name = 'debtratio'
    allowed_domains = ['https://worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows:
            name = row.xpath('.//td/a/text()').get()
            link = row.xpath('.//td/a/@href').get()
            dgratio = row.xpath('.//td[2]/text()').get()
            population = row.xpath('.//td[3]/text()').get()

            yield {
                'Country Name': name,
                'Link': response.urljoin(link),
                'Debt to Gdp Ratio': dgratio,
                'Population': population
            }
