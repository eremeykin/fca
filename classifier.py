import random

from data_preparation import *
from labels import *
import pandas as pd

from numpy_set_operations import *

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
    def predict(self, target, num_sub=None):
        print('predict: ' + str(target))
        if not self.trained:
            raise Exception('The classifier is not trained yet')
        if num_sub is None:
            num_sub = len(target) // 2
        neg = 0
        pos = 0
        for i in range(num_sub):
            t = target.sample(n=random.randrange(len(target)))
            p = self.positive.map(lambda x: issuper(x, t))
            for index, j in self.positive.iterrows():
                if issuper(j, t):
                    pos += len(t)
            for index, k in self.negative.iterrows():
                if issuper(k, t):
                    neg += len(t)

        def score(pos, neg):
            return pos * 1. / (neg + 1)

        threshold = 1.1
        if score(pos, neg) > threshold:
            return POSITIVE_LABEL
        elif score(neg, pos) > threshold:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL

if __name__ == '__main__':
    data = get_raw_data('data.csv')
    train = data.iloc[:8]
    test = data.iloc[8:]
