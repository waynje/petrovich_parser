import scrapy


class PetrovichParserItem(scrapy.Item):
    name = scrapy.Field()
    amount = scrapy.Field()
    link = scrapy.Field()
