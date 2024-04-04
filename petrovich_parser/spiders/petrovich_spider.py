import os
from time import sleep

import scrapy
from scrapy.http import FormRequest

from ..items import PetrovichParserItem


LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
BASE_LINK = 'https://petrovich.ru'


class PetrovichSpiderSpider(scrapy.Spider):
    name = 'petrovich_spider'
    start_urls = ['https://petrovich.ru/']

    def start_login(self, response):

        button = response.css('a.header-button.auth-header-button')
        button_url = button.css('::attr(href)').extract_first()
        if button_url:
            yield response.follow(button_url, callback=self.login)

    def login(self, response):

        sleep(1)
        email_form_response = response.css('#pt-input-id-5')
        password_form_response = response.css('#pt-input-id-6')
        return FormRequest(self.start_urls,
                           formdata={email_form_response: LOGIN,
                                     password_form_response: PASSWORD},
                           callback=self.start_scraping)

    def start_requests(self):

        estimates_url = 'https://petrovich.ru/cabinet/estimates/'
        yield scrapy.Request(estimates_url, callback=self.start_scraping)

    def start_scraping(self, response):

        for link in response.css('a.title.pt-wrap').attrib['href']:
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
