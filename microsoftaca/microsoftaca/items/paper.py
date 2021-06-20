# -*- coding: utf-8 -*-

import scrapy


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    date = scrapy.Field()
    authors = scrapy.Field()
    related_topics = scrapy.Field()
    citation_count = scrapy.Field()
    reference_count = scrapy.Field()
    references = scrapy.Field()
