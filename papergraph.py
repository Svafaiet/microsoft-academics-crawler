import json
import logging
import os

from config import config
import numpy as np

logging.getLogger(__name__)


class PaperGraph:
    def __init__(self):
        self.graph = {}
        self.gmatrix = None
        self.alpha = 0.1
        self.threshhold = 0.001

    def get_graph(self):
        return self.graph.copy()

    def _normalize(self, v):
        v = np.array(v)
        norm = np.sum(v)
        if norm == 0:
            return v
        return v / norm

    def load_graph(self, filename=None):
        filename = filename or os.path.join(config.PAPER_PATH, 'papers.jl')
        node_mapping = {}
        node_order = []
        with open(filename, 'r') as f:
            for index, line in enumerate(f):
                paper = json.loads(line)
                node_mapping[paper['id']] = index
                self.graph[paper['id']] = set(paper['references'])
                node_order.append(paper['id'])
        page_count = len(node_order)
        self.gmatrix = [0]*page_count
        for node_id in self.graph:
            self.graph[node_id] = set(filter(lambda paper_id: paper_id in self.graph, self.graph[node_id]))
        for index, node_id in enumerate(node_order):
            neighbour_indices = list(
                node_mapping[neighbour] for neighbour in self.graph[node_id]
            )
            self.gmatrix[index] = self._normalize(np.array(list(
                int(i in neighbour_indices) for i in range(page_count)
            )))
            self.gmatrix[index] = (1 - self.alpha) * self.gmatrix[index] + self.alpha * np.ones(page_count) / page_count
        self.gmatrix = np.array(self.gmatrix)

    def get_pagerank(self):
        x0 = np.ones(len(self.gmatrix)) / len(self.gmatrix)
        x = x0
        p_n = np.linalg.matrix_power(self.gmatrix, 4)
        iterations = 0
        while True:
            iterations += 1
            new_x = self._normalize(np.matmul(x, p_n))
            if np.linalg.norm(new_x - x) < self.threshhold/len(self.gmatrix):
                break
            x = new_x
        logging.info(f"Calculated page rank after {iterations} iterations")
        print(f"Calculated page rank after {iterations} iterations")
        return x


if __name__ == '__main__':
    pg = PaperGraph()
    pg.load_graph()
    print(pg.get_pagerank())
    print(pg._normalize(np.matmul(pg.get_pagerank(), pg.gmatrix)))




