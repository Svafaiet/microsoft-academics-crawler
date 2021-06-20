# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgent(UserAgentMiddleware):

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        ua = UserAgent()
        if 'splash' not in request.meta.keys():
            request.headers['User-Agent'] = ua.random
        else:
            request.meta['splash']['args']['headers']['User-Agent'] = ua.random

