import json
import os

from config import config
from microsoftaca.utils import normalize


def load_titles_from_jl():
    title_dict = dict()
    filename = os.path.join(config.PAPER_PATH, 'papers.jl')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'r') as f:
        for line in f:
            paper = json.loads(line)
            title_dict[normalize(paper['title'])] = paper['id']
    return title_dict


def load_start_urls():
    with open(os.path.join(config.START_URLS)) as f:
        return list((line[:-1] + "/") for line in f.readlines())
