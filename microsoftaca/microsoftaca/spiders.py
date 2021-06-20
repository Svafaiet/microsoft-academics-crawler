# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_splash import SplashRequest
from w3lib.html import remove_tags

from config import config
from microsoftaca.microsoftaca.items.paper import PaperItem
from microsoftaca.utils import normalize

logging.getLogger(__name__)


class MicrosoftacaSpider(scrapy.Spider):
    name = 'microsoftaca_spider'

    def __init__(self, start_urls, lua=None, titles={}, allowed_domains=(),
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.lua = lua
        if allowed_domains:
            self.allowed_domains = allowed_domains
        self.page_count = 0
        self.titles = titles
        self.blocked = False

    def start_requests(self):
        for url in self.start_urls:
            yield self.generate_request(url=url, parser=self.parse)

    def generate_request(self, url, parser, parser_kwargs=None):
        request_kwargs = {
            "args": {
                'wait': 3,
                'timeout': 90.0,
                'html': 1,
                'headers':
                    {'User-Agent':
                         "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
                     }
            }}
        request_kwargs["args"]["lua_source"] = self.lua
        request_kwargs["endpoint"] = "execute"
        return SplashRequest(url, parser, meta=parser_kwargs, **request_kwargs)

    def clear_references(self, references, reference_names):
        new_names = set()
        for index, reference_name in enumerate(reference_names):
            normalized_name = normalize(reference_name)
            if normalized_name not in self.titles:
                if normalized_name not in new_names:
                    yield references[index]
            else:
                yield self.titles[normalized_name]
            new_names.add(normalized_name)

    def parse(self, response):
        if len(self.titles.keys()) >= config.MAX_PAGE:
            if not self.blocked:
                raise CloseSpider()
            return
        paper_id = str(response.url.split('/')[-2])
        single_fields_selectors = {
            "title": "#mainArea > router-view > div > div > div > div > h1.name",
            "abstract": "#mainArea > router-view > div > div > div > div > p",
            "citation_count": "#mainArea > router-view > div > div > div > div > div.stats > ma-statistics-item:nth-child(1) > div.ma-statistics-item.au-target > div.data > div.count",
            "reference_count": "#mainArea > router-view > div > div > div > div > div.stats > ma-statistics-item:nth-child(2) > div.ma-statistics-item.au-target > div.data > div.count",
            "date": "#mainArea > router-view > div > div > div > div > a > span.year",
        }
        single_fields = dict(list((key, remove_tags(response.css(value).extract_first()).strip())
                                  for key, value in single_fields_selectors.items()))

        if normalize(single_fields['title']) in self.titles:
            return
        else:
            self.titles[normalize(single_fields['title'])] = paper_id
        list_fields_selectors = {
            "authors": "#mainArea > router-view > div > div > div > div > ma-author-string-collection > div > div > div > a.au-target.author.link",
            "related_topics": "div.tag-cloud > ma-link-tag > a > div.text.au-target",
        }
        list_fields = dict(list(
            (key, list(remove_tags(value).strip() for value in response.css(value_list).extract()))
            for key, value_list in list_fields_selectors.items()))

        references = list(url.split("/")[1] for url in
                          response.css(
                              "#mainArea > router-view > router-view > ma-edp-serp > div > div.results > div > compose > div > div.results > ma-card > div > compose > div > div.primary_paper > a.title.au-target::attr(href)").extract())

        reference_names = list(remove_tags(value).strip() for value in
                               response.css(
                                   "#mainArea > router-view > router-view > ma-edp-serp > div > div.results > div > compose > div > div.results > ma-card > div > compose > div > div.primary_paper > a.title.au-target > span").extract())

        references = list(set(self.clear_references(references, reference_names)))
        logging.debug(reference_names)
        yield PaperItem(
            id=paper_id,
            references=references,
            **{**single_fields, **list_fields},
        )
        reference_count = min(10, len(references))
        for paper in references[:reference_count]:
            yield self.generate_request(f"https://academic.microsoft.com/paper/{paper}/", self.parse)

        if len(self.titles.keys()) >= config.MAX_PAGE:
            raise CloseSpider()
