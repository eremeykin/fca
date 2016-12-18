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

    SEED1 = 12332513
    SEED2 = 43289
    random.seed(SEED2)

    def predict(self, target, num_sub=None):
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

if __name__ == '__main__':
    data = get_raw_data('data.csv')
    train = data.iloc[:8]
    test = data.iloc[8:]
