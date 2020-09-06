# -*- coding: utf-8 -*-
# main url -http://quotes.toscrape.com/scroll
import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        # The response.body is json format convert it to  python dict()

        # convert
        resp = json.loads(response.body)
        # json is like dictionaries of dictionies

        # To get the json keys
        quotes = resp.get('quotes')
        for q in quotes:
            yield {
                # This is the way to get the the keys inside the keys
                'Author': q.get('author').get('name'),
                'Tags': q.get('tags'),
                'Quote': q.get('text')
            }

        # Handling Pagination

        next_page = resp.get('has_next')
        if next_page:
            next_page_number = resp.get('page') + 1

            yield scrapy.Request(url=f'http://quotes.toscrape.com/api/quotes?page={next_page_number}',
                                 callback=self.parse)
