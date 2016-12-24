import random

from data_preparation import *
import numpy as np
import pandas as pd

from numpy_set_operations import *
from pprint import pprint
__author__ = 'eremeykin'


class AbstractClassifier(object):
    def __init__(self, threshold):
        self.trained = False
        self.positive = None
        self.negative = None
        self.threshold = threshold

    def train(self, train_data):
        self.positive = train_data[train_data['label'] == POSITIVE_LABEL]
        self.negative = train_data[train_data['label'] == NEGATIVE_LABEL]
        del self.positive['label']
        del self.negative['label']
        self.trained = len(self.positive) > 0 and len(self.negative) > 0

    def predict(self, target):
        raise Exception('abstract method')


class ImplicationClassifier(AbstractClassifier):
    SEED1 = 12332513
    SEED2 = 43289
    random.seed(SEED2)

    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
        if not self.trained:
            raise Exception('The classifier is not trained yet')
        if num_sub is None:
            num_sub = len(target) // 2
        neg = 0
        pos = 0
        for i in range(num_sub):
            t = target.sample(n=random.randrange(len(target)),
                              random_state=ImplicationClassifier.SEED1)
            pos += self.positive.apply(lambda x: int(issuper(x, t)), axis=1).sum()
            neg += self.negative.apply(lambda x: int(issuper(x, t)), axis=1).sum()

        def score(pos, neg):
            return pos * 1. / (neg + 1)

        if score(pos, neg) > self.threshold:
            return POSITIVE_LABEL
        elif score(neg, pos) > self.threshold:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL


class MyClassifier(AbstractClassifier):
    def __init__(self, threshold):
        super().__init__(threshold)

    def train(self, train_data):
        super().train(train_data)
        self.pos_dict = dict()
        for c in self.positive.columns:
            self.pos_dict[c] = self.positive[c].value_counts() / self.positive[c].value_counts().sum()
        self.neg_dict = dict()
        for c in self.negative.columns:
            self.neg_dict[c] = self.negative[c].value_counts() / self.negative[c].value_counts().sum()
        self.pos_max = 0
        self.neg_max = 0
        for key, value in self.pos_dict.items():
            self.pos_max += value.max()
        for key, value in self.neg_dict.items():
            self.neg_max += value.max()

    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
        pos = 0
        neg = 0
        for index, value in target.iteritems():
            if index in self.pos_dict.keys() and value in self.pos_dict[index].keys():
                delta_pos = self.pos_dict[index][value]
            else:
                delta_pos = -self.neg_dict[index][value]
            if index in self.neg_dict.keys() and value in self.neg_dict[index].keys():
                delta_neg = self.neg_dict[index][value]
            else:
                delta_neg = -self.pos_dict[index][value]
            pos += delta_pos
            neg += delta_neg

        pos /= self.pos_max
        neg /= self.neg_max

        def score(pos, neg):
            return pos * 1. / neg if neg != 0 else np.infty

        if score(pos, neg) > self.threshold:
            return POSITIVE_LABEL
        elif score(neg, pos) > self.threshold:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL


class MyClassifier2(AbstractClassifier):
    def __init__(self, threshold):
        super().__init__(threshold)

    def train(self, train_data):
        super().train(train_data)
        self.pos_dict = dict()
        for c in self.positive.columns:
            self.pos_dict[c] = (self.positive[c].value_counts() / self.positive[c].value_counts().sum())**4
        self.neg_dict = dict()
        for c in self.negative.columns:
            self.neg_dict[c] = (self.negative[c].value_counts() / self.negative[c].value_counts().sum())**4


    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
        pos = 0
        neg = 0
        for index, value in target.iteritems():
            if value=='?':
                continue
            if index in self.pos_dict.keys() and value in self.pos_dict[index].keys():
                delta_pos = self.pos_dict[index][value]
            else:
                delta_pos = -2
            if index in self.neg_dict.keys() and value in self.neg_dict[index].keys():
                delta_neg = self.neg_dict[index][value]
            else:
                delta_neg = -2
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
            print('UNKNOWN_LABEL, pos = ' + str(pos))
            print('UNKNOWN_LABEL, neg = ' + str(neg))
            return UNKNOWN_LABEL




if __name__ == '__main__':
    data = get_raw_data('data.csv')
    train = data.iloc[:8]
    test = data.iloc[8:]
