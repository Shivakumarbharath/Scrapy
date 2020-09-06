# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class SilkdealsPipeline(object):

    def open_spider(self, spider):
        self.db = sqlite3.connect('computers.db')
        self.c = self.db.cursor()
        self.c.execute('''
        
        CREATE TABLE computers(
        Name TEXT,
        URL TEXT,
        Price text
        )
        
        ''')
        self.db.commit()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.c.execute('''
        INSERT INTO computers (Name,URL,Price) VALUES(?,?,?)
        
        ''', (item['Name'], item['URL'], item['price']))
        self.db.commit()

        return item
