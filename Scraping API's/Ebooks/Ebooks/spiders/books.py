# -*- coding: utf-8 -*-
# Main url - https://openlibrary.org/subjects/picture_books
import scrapy
import json


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12/']

    def parse(self, response):
        works = json.loads(response.body).get('works')
        for work in works:
            yield {
                "Title": work.get('title'),
                'Subject': work.get('subject')
            }


'''
Code from the course

# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json


class EbooksSpider(scrapy.Spider):
    name = 'ebooks'

    INCREMENTED_BY = 12
    # starts from  
    offset = 0

    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12']

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider('Reached last page...')

        resp = json.loads(response.body)
        ebooks = resp.get('works')
        for ebook in ebooks:
            yield {
                'title': ebook.get('title'),
                'subject': ebook.get('subject')
            }
        
        self.offset += self.INCREMENTED_BY
        yield scrapy.Request(
            url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
            callback=self.parse
        )

'''
