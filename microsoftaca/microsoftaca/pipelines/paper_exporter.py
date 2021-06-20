# -*- coding: utf-8 -*-
import datetime
import os
import shutil
from scrapy.exporters import JsonLinesItemExporter

from config import config


class PaperExporterPipeline:

    def open_spider(self, spider):
        self.exporter = None

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.exporter.file.close()

    def _get_exporter(self):
        if not self.exporter:
            filename = os.path.join(config.PAPER_PATH, 'papers.jl')
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if not config.IS_STATEFUL:
                with open(filename, 'wb'):
                    pass
            f = open(filename, "ab")

            self.exporter = JsonLinesItemExporter(f)
            self.exporter.start_exporting()

        return self.exporter

    def process_item(self, item, spider):
        exporter = self._get_exporter()
        exporter.export_item(item)
        return item
