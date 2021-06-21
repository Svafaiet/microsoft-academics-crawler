from operator import itemgetter

from papergraph import PaperGraph
import csv
import numpy as np


def make_profile(profile_str):
    def to_float(item):
        item = item.strip()
        item = item or "0"
        return float(item)

    profile_str = str(profile_str).strip()
    if str().startswith("["):
        profile_str = profile_str[1:-1]
    profile_str.replace("\"", "")
    return list(map(to_float, profile_str.split(",")))


class Recommender:
    def __init__(self):
        self.paper_topics = {}
        self.topic_to_index = {}
        self.users = []

    @staticmethod
    def cosine_similarity(a, b):
        assert len(a) == len(b)
        norm_size = (np.linalg.norm(a) * np.linalg.norm(b)) or 1
        return np.dot(a, b) / norm_size

    def load_profiles(self, user_topics=None):
        user_topics = user_topics or "data.csv"
        with open(user_topics) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rows = list(csv_reader)
            self.topic_to_index = dict((column.lower().strip(), index) for index, column in enumerate(rows[0]))
            self.users = list(np.array(list(map(float, ((c or 0) for c in user)))) for user in rows[1:])

    def load_papers(self, paper_file=None):
        for paper in PaperGraph.paper_iterator(paper_file):
            topic_list = list(
                filter(lambda topic: (topic.lower().strip() in self.topic_to_index), paper['related_topics']))
            topic_indices = list(
                self.topic_to_index[topic.lower().strip()] for topic in topic_list
            )
            self.paper_topics[paper['id']] = np.array(list(
                int(i in topic_indices) for i in range(len(self.topic_to_index))
            ))

    def suggest_article(self, user_vector, n=10):
        user = np.array(user_vector)
        papers_scores = {k: self.cosine_similarity(user, v) for k, v in self.paper_topics.items()}
        return dict(
            sorted(papers_scores.items(), key=itemgetter(1), reverse=True)[:min(n, len(self.paper_topics.keys()))])

    def suggest_profile(self, user_vector, n=10):
        user = np.array(user_vector)
        user_scores = {k: self.cosine_similarity(user, v) for k, v in enumerate(self.users)}
        best_users = list(
            sorted(user_scores.items(), key=itemgetter(1), reverse=True)[:min(n, len(user_scores.keys()))])
        best_user_profiles = [self.users[i] for i in dict(best_users)]
        normalized_profile = np.sum(best_user_profiles, axis=0) / len(best_user_profiles)
        best_users_score_profile = list(
            (best_users[i][0], best_users[i][1], best_user_profiles[i]) for i in range(len(best_users)))
        return normalized_profile, best_users_score_profile
