# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    # allowed_domains = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="main"]/div/div[1]/div[2]/a'))
    )

    def parse_item(self, response):
        print('The Url', response.url)
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        title_bar = response.xpath('//div[@class="title_bar_wrapper"]')
        rating = title_bar.xpath('.//div/div/div/strong/span/text()').get()
        no_of_raters = title_bar.xpath('.//div/div/a/span/text()').get()
        title = title_bar.xpath('.//div[2]/div[2]/h1/text()').get()
        year = title_bar.xpath('.//div[2]/div[2]/h1/span/a/text()').get()
        time = response.xpath('normalize-space(//time[@datetime]/text())').get()
        # Here the normalize-space is used to remove the spaces
        yield {
            'Title': title,
            'Time': time,
            'Year': year,
            'Rating': str(rating) + '/10',
            'Rated By': str(no_of_raters) + ' People'

        }
