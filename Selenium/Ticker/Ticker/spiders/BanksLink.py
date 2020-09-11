# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time


class BankslinkSpider(scrapy.Spider):
    name = 'BanksLink'
    # allowed_domains = ['https://ticker.finology.in']
    # start_urls = ['https://ticker.finology.in/']
    # Spoofing the user agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'

    # Start the requsets with the selenuim requests as it is a  javascript website
    # And the scraping requires to type and search
    def start_requests(self):
        yield SeleniumRequest(url='https://ticker.finology.in/', callback=self.parse,
                              headers={'User-Agent': self.user_agent,
                                       "Accept-Encoding": "gzip, deflate",
                                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                       "DNT": "1",
                                       "Connection": "close",
                                       "Upgrade-Insecure-Requests": "1"
                                       })

    def parse(self, response):
        # Grab the driver object
        driver = response.request.meta['driver']

        # find the element to search
        search = driver.find_element_by_xpath('//input[@name="txtSearchComp"]')

        # To get all the links to banks type banks which gives a scroller to select
        search.send_keys('bank')
        # sleep as the links take time to pop up
        time.sleep(2)

        # Convert the page source to selector object
        resp = Selector(text=driver.page_source)

        # Grab the links
        links = resp.xpath('//div[@class="output ps active"]/a/@href').getall()

        # print(links,'links')
        # driver.save_screenshot('banks.png')

        # Request every link to get the Information
        for link in links:
            if link:
                # Convert the relative url(/company/hdfc) to Absolute url
                absolute_url = 'https://ticker.finology.in/' + link
                yield scrapy.Request(url=absolute_url, callback=self.parse_comp, headers={'User-Agent': self.user_agent,
                                                                                          "Accept-Encoding": "gzip, deflate",
                                                                                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                                                          "DNT": "1",
                                                                                          "Connection": "close",
                                                                                          "Upgrade-Insecure-Requests": "1"
                                                                                          })

    def parse_comp(self, response):
        # Get the details
        name = response.xpath('//h1/span/text()').get()
        market_cap = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][1]/p/span/text()').get()
        casa = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][2]/p/span/span/text()').get()
        pb = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][5]/p/text()').get()

        # Handle the Attribute error if the returnes value is none it cannot be stripped
        try:
            pb = pb.strip()
        except AttributeError:
            pb = pb

        bv = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][8]/p/span/text()').get()
        try:
            bv = bv.strip()
        except AttributeError:
            bv = bv

        net_intrest_income = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][9]/p/span/span/text()').get()
        try:
            net_intrest_income = net_intrest_income.strip()
        except AttributeError:
            net_intrest_income = net_intrest_income
        eps = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][12]/p/span/text()').get()
        try:
            eps = eps.strip()
        except AttributeError:
            eps = eps
        car = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][13]/p/text()').get()
        try:
            car = car.strip()
        except AttributeError:
            car = car
        roe = response.xpath(
            '//div[@id="companyessentials"]/div[2]/div[@class="col-6 col-md-4 compess"][14]/p/span/text()').get()
        try:
            roe = roe.strip()
        except AttributeError:
            roe = roe
        roa_5 = response.xpath('//*[@id="mainContent_divROA"]/div/div[2]/div[3]/span[2]/text()').get()
        npa_5 = response.xpath('//*[@id="mainContent_divNPA"]/div/div[2]/div[3]/span[2]/text()').get()
        nim_5 = response.xpath('//*[@id="mainContent_divNIM"]/div/div[2]/div[3]/span[2]/text()').get()
        advances_growth = response.xpath('//*[@id="mainContent_divAdvancesGrowth"]/div/span/span/text()').get()
        cost_of_liabalities = response.xpath('//*[@id="mainContent_divPEG"]/div/span/span/text()').get()

        # Boom here is the details requested
        yield {'Bank Name': name,
               'Market Cap': market_cap,
               'CASA %': casa,
               'P/B': pb,
               'Book Value': bv,
               'Net Intrest Income': net_intrest_income,
               'EPS': eps,
               'CAR %': car,
               'ROE %': roe,
               'ROA For 5 years': roa_5,
               'NPA For 5 years': npa_5,
               'NIM For 5 years': nim_5,
               'Advances Growth': advances_growth,
               'COST OF LIABALITIES': cost_of_liabalities

               }
