import os

from scrapy.utils.project import get_project_settings

from config import config

import logging

from microsoftaca.microsoftaca.extractors import MicrosoftacaExtractor

logging.getLogger(__name__)


def extractor_process(json_file_out=None):
    logging.info("extractor starts ...")
    settings_file_path = 'microsoftaca.microsoftaca.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    config.JSON_OUT_PATH = json_file_out or config.JSON_OUT_PATH
    settings = get_project_settings()
    extractor = MicrosoftacaExtractor(settings)
    extractor.extract(is_stateful=config.IS_STATEFUL)









