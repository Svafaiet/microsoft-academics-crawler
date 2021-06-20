import json
import os
from collections import defaultdict
from operator import itemgetter

from config import config
from papergraph import PaperGraph


class Hits:
    def __init__(self):
        self.out_graph = defaultdict(set)
        self.in_graph = defaultdict(set)

    def load_graph(self, filename=None):
        pg = PaperGraph()
        pg.load_graph(filename=filename)
        graph = pg.get_graph()
        authors_to_paper_id = defaultdict(set)
        papers_dict = dict()
        filename = str(filename or os.path.join(config.PAPER_PATH, 'papers.jl'))
        with open(filename, 'r') as f:
            def paper_iterator():
                if filename.lower().split(".")[-1] == "jl":
                    return (json.loads(line) for line in f)
                elif filename.lower().split(".")[-1] == "json":
                    return json.load(f)

            for index, paper in enumerate(paper_iterator()):
                papers_dict[paper['id']] = paper
                for author in paper['authors']:
                    authors_to_paper_id[author.lower()].add(paper['id'])
        for author, papers in authors_to_paper_id.items():
            for paper in papers:
                if paper not in graph:
                    continue
                for out_paper in graph[paper]:
                    for out_author in papers_dict[out_paper]['authors']:
                        self.out_graph[author].add(out_author)
                        self.in_graph[out_author].add(author)

    def _normalize_dict(self, d):
        factor = 1.0
        sum_of_values = sum(d.values())
        if sum_of_values != 0:
            factor /= sum_of_values
        return {k: v * factor for k, v in d.items()}

    def get_top_authors(self, n):
        authority = dict()
        hub = dict()
        for key in self.in_graph:
            authority[key] = 1
            hub[key] = 1
        for key in self.out_graph:
            authority[key] = 1
            hub[key] = 1
        for i in range(5):
            temp_hub = hub.copy()
            temp_authority = authority.copy()
            for key, nodes in self.in_graph.items():
                authority[key] = sum(temp_hub[neighbour] for neighbour in nodes)
            for key, nodes in self.out_graph.items():
                hub[key] = sum(temp_authority[neighbour] for neighbour in nodes)
            authority = self._normalize_dict(authority)
            hub = self._normalize_dict(hub)
        return dict(sorted(authority.items(), key=itemgetter(1), reverse=True)[:min(n, len(authority.keys()))])


if __name__ == "__main__":
    hits = Hits()
    hits.load_graph()
    print(hits.get_top_authors(5))
