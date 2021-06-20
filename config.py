import logging

from grift import BaseConfig, EnvLoader, ConfigProperty
from schematics.types import StringType, IntType, BooleanType


class Config(BaseConfig):

    PAPER_PATH = ConfigProperty(property_type=StringType(), default='papers')
    ERRORED_URLS_PATH = ConfigProperty(property_type=StringType(), default='/tmp/errored-urls')
    STATE_PATH = ConfigProperty(property_type=StringType(), default='crawler-state')
    LOG_LEVEL = ConfigProperty(property_type=IntType(), default=logging.DEBUG)
    DEBUG = ConfigProperty(property_type=BooleanType(), default=True)
    IS_STATEFUL = ConfigProperty(property_type=BooleanType(), default=True)
    MAX_PAGE = ConfigProperty(property_type=IntType(), default=2000)
    START_URLS = ConfigProperty(property_type=StringType(), default='start.txt')
    JSON_OUT_PATH = ConfigProperty(property_type=StringType(), default='.')



loaders = [EnvLoader()]
config = Config(loaders)
