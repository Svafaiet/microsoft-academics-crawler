import csv
import os

import numpy as np


class Recovery:
    def __init__(self):
        self.pick_ratio = 0.8
        self.users = []
        self.Q = np.array([0])
        self.P = np.array([0])

    def load_profiles(self, user_topics=None):
        user_topics = user_topics or "data.csv"
        with open(user_topics) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rows = list(csv_reader)
            self.users = list(np.array(list(map(float, ((c or 0) for c in user)))) for user in rows[1:])

    def recover(self, max_iter=100, alpha=0.05):
        train = np.array(self.users[:int(self.pick_ratio * len(self.users))])
        test = np.array(self.users[int(self.pick_ratio * len(self.users)):])
        u, s, vh = np.linalg.svd(train, full_matrices=True)
        u = np.matmul(u, s)
        # for i in range(max_iter):
        #     new_u = np.array(u)
        #     new_vh = np.array(vh)
        #     reduction = train - np.matmul(u, vh)
        #     new_u = u - 2*alpha*np.multiply(, )
        #     u = new_u
        #     vh = new_vh

    def output(self, output):
        outputp = os.path.join(output, "P.txt")
        outputq = os.path.join(output, "Q.txt")
        np.savetxt(outputp, self.P)
        np.savetxt(outputq, self.Q)
