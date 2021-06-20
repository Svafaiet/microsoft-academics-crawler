# -*- coding: utf-8 -*-

class RemoveCookieMiddleware:
    def process_request(self, request, spider):

        if 'splash' not in request.meta.keys():
            request.cookies = {}
            request.headers['cookies'] = ''
        else:
            request.meta['splash']['args']['headers']['cookies'] = ''

    def process_exception(self, request, exception, spider):
        if 'splash' not in request.meta.keys():
            request.cookies = {}
            request.headers['cookies'] = ''
        else:
            request.meta['splash']['args']['headers']['cookies'] = ''
