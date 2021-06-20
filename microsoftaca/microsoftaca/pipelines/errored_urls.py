# -*- coding: utf-8 -*-
import datetime
import os
import shutil
from scrapy.exporters import JsonLinesItemExporter

from config import config
from microsoftaca.microsoftaca.items.paper import PaperItem


class ErroredUrlsPipeline:

    def process_item(self, item, spider):
        if isinstance(item, PaperItem):
            return item

        filename = os.path.join(config.ERRORED_URLS_PATH , 'urls.jl')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'a+') as f:
            f.write(str(item))
            f.write("\n")
        return item
