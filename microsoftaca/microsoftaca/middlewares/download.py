# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import IgnoreRequest

from config import config
from microsoftaca.loaders.papers import load_titles_from_jl
from microsoftaca.microsoftaca import settings


class MicrosoftacaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.blocked = False

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.process_request, signal=signals.request_reached_downloader)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        if spider.blocked:
            raise IgnoreRequest()
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if any([request.url.endswith('.'+item) for item in settings.IGNORED_EXTENSIONS]):
            raise IgnoreRequest()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.


        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        if spider.blocked:
            spider.crawler.engine.slot.scheduler.close("end of crawl")

