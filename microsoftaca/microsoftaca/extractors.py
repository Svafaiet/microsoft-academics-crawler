from scrapy.crawler import Crawler, CrawlerProcess

import logging

from config import config
from microsoftaca.loaders.papers import load_titles_from_jl, load_start_urls
from microsoftaca.microsoftaca.spiders import MicrosoftacaSpider

logging.getLogger(__name__)


class MicrosoftacaExtractor:
    def __init__(self, settings):
        self.settings = settings

    def extract(self, is_stateful=False):
        runner = CrawlerProcess(self.settings)
        settings = self.settings.copy()
        lua=""
        with open("microsoftaca/microsoftaca.lua") as f:
            lua = "\n".join(f.readlines())
        start_urls = load_start_urls()

        kwargs = {
            "start_urls": start_urls,
            "allowed_domains": ["academic.microsoft.com"],
            "lua": lua,
        }
        if is_stateful is True:
            settings.update({'JOBDIR': config.STATE_PATH})
            titles_dict = load_titles_from_jl()
            kwargs["titles"] = titles_dict
            if titles_dict:
                kwargs["start_urls"] = []

        crawler = Crawler(MicrosoftacaSpider, settings)
        runner.crawl(crawler, **kwargs)
        runner.start()
