import os

import scrapy
from scrapy.http import FormRequest

from ..items import PetrovichParserItem


LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
BASE_LINK = 'https://petrovich.ru'


class PetrovichSpiderSpider(scrapy.Spider):
    name = 'petrovich_spider'

    def login(self, response):

        login_url = 'https://petrovich.ru/cabinet/profile/'
        return FormRequest(login_url,
                           formdata={'email': LOGIN, 'password': PASSWORD},
                           callback=self.start_scraping)

    def start_requests(self):

        estimates_url = 'https://petrovich.ru/cabinet/estimates/'
        yield scrapy.Request(estimates_url, callback=self.start_scraping)

    def start_scraping(self, response):

        for link in response.css('title pt-wrap a[href^="cabinet/estimate/"]'):
            yield response.follow(
                link, callback=self.parse_estimate
            )

    def parse_estimate(self, response):

        products_title = response.css('span.pt-typography____JqPt[data-test="product-title"]::text').getall()
        link = response.css('a.sc-eqUAAy::attr(href)').getall()
        products_amount = response.css('input[data-test="product-counter"]::attr(value)').getall()
        products_link = BASE_LINK + link

        for product_title, product_amount, product_link in zip(products_title, products_amount, products_link):
            yield PetrovichParserItem(
                name=product_title,
                amount=product_amount,
                link=product_link,
            )
