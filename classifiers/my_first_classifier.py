import numpy as np

from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *


class MyFirstClassifier(AbstractClassifier):
    def __init__(self, threshold):
        super().__init__(threshold)

    def train(self, train_data):
        super().train(train_data)
        self.neg_dict = dict()
        self.pos_dict = dict()
        for c in self.positive.columns:
            self.pos_dict[c] = (self.positive[c].value_counts() / self.positive[c].value_counts().sum()) ** 4
        for c in self.negative.columns:
            self.neg_dict[c] = (self.negative[c].value_counts() / self.negative[c].value_counts().sum()) ** 4

    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
        pos = 0
        neg = 0
        for index, value in target.iteritems():
            delta_neg, delta_pos = 0, 0
            if value == '?':
                continue
            if index in self.pos_dict.keys() and value in self.pos_dict[index].keys():
                delta_pos = self.pos_dict[index][value]
            if index in self.neg_dict.keys() and value in self.neg_dict[index].keys():
                delta_neg = self.neg_dict[index][value]
            pos += delta_pos
            neg += delta_neg

        def score(pos, neg):
            if pos < 0: pos = 0
            if neg < 0: neg = 0
            return pos * 1. / neg if neg != 0 else np.infty

        if score(pos, neg) > self.threshold:
            return POSITIVE_LABEL
        elif score(neg, pos) > self.threshold:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL
