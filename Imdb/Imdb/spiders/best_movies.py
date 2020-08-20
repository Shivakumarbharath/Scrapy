# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    # allowed_domains = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'

    # To spoof the user agen in the starting url
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc/', headers={
                'User-Agent': self.user_agent})

    def Start_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']"), callback='parse_item', follow=True,
             process_request='Start_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="main"]/div/div[1]/div[2]/a'), process_request='Start_user_agent')
    )

    def parse_item(self, response):
        print('The Url', response.url)
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        title_bar = response.xpath('//div[@class="title_bar_wrapper"]')
        rating = title_bar.xpath('.//div/div/div/strong/span/text()').get()
        no_of_raters = title_bar.xpath('.//div/div/a/span/text()').get()
        title = title_bar.xpath('.//div[2]/div[2]/h1/text()').get().encode('ascii', 'ignore').decode('utf-8')
        # here the encode and decode is to remove the unicode charecters
        year = title_bar.xpath('.//div[2]/div[2]/h1/span/a/text()').get()
        time = response.xpath('normalize-space(//time[@datetime]/text())').get()
        # Here the normalize-space is used to remove the spaces
        yield {
            'Title': title,
            'Time': time,
            'Year': year,
            'Rating': str(rating) + '/10',
            'Rated By': str(no_of_raters) + ' People',
            'User-Agent': response.request.headers['User-Agent']

        }
