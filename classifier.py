import random

from close_by_one import *
from data_preparation import *
import numpy as np
import pandas as pd
from context import Context
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
            self.pos_dict[c] = (self.positive[c].value_counts() / self.positive[c].value_counts().sum()) ** 4
        self.neg_dict = dict()
        for c in self.negative.columns:
            self.neg_dict[c] = (self.negative[c].value_counts() / self.negative[c].value_counts().sum()) ** 4

    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
        pos = 0
        neg = 0
        for index, value in target.iteritems():
            if value == '?':
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


class MyFcaClassifier(AbstractClassifier):
    class Cache(object):
        def __init__(self):
            self.exact = dict()
            self.storage = dict()
            self.max_len = 0
            self.min_len = 10e6
            self.s0 = 0
            self.s1 = 0
            self.s2 = 0

        def check(self, hypothesis):
            # print('s0: '+str(self.s0))
            # print('s1: ' + str(self.s1))
            # print('s2: ' + str(self.s2))
            hyp = frozenset(zip(hypothesis.index, hypothesis))
            try:
                res = self.exact[hyp]
                # print('success0')
                self.s0 += 1
                return res
            except KeyError:
                pass
            L = len(hyp)
            for l in range(L, self.max_len):  # [L + 1, L + 2, L + 3, self.max_len, self.max_len - 1]:
                try:
                    for key, value in self.storage[l].items():
                        if value == 1 and key.issubset(hyp):
                            # print('success1')
                            self.s1 += 1
                            return 1
                except KeyError as e:
                    pass

            for l in range(L, self.max_len):  # [L - 1, L - 2, L - 3, self.min_len, self.min_len + 1]:
                try:
                    for key, value in self.storage[l].items():
                        # print(key, value)
                        # print(hyp)
                        # print()
                        if value == 0 and key.issuperset(hyp):
                            # print('success2')
                            self.s2 += 1
                            return 0
                except KeyError as e:
                    pass

        def add(self, new, value):
            from pprint import pprint
            # pprint(self.storage)
            new = frozenset(zip(new.index, new))
            self.exact[new] = value
            try:
                d = self.storage[len(new)]
            except KeyError:
                self.storage[len(new)] = dict()
                d = self.storage[len(new)]
            d[new] = value
            if len(new) > self.max_len:
                self.max_len = len(new)
            if len(new) < self.min_len:
                self.min_len = len(new)

    def __init__(self, threshold=1):
        super().__init__(threshold)
        self.p_cache = MyFcaClassifier.Cache()
        self.n_cache = MyFcaClassifier.Cache()

    def train(self, train_data):
        super().train(train_data)
        self.p_context = Context(self.positive)
        self.n_context = Context(self.positive)
        close_by_one(self.p_context)
        print('done')
        exit()

        self.p_cache = MyFcaClassifier.Cache()
        self.n_cache = MyFcaClassifier.Cache()

    @staticmethod
    def intersect(x, y):
        return set(zip(x.index, x.values)) & set(zip(y.index, y.values))

    def predict(self, target, num_sub=None):
        self.i = 0
        from time import time
        start = time()

        def test_hypothesis(hyp, type):
            if type == POSITIVE_LABEL:
                cache = self.p_cache
            if type == NEGATIVE_LABEL:
                cache = self.n_cache
            cache_check = cache.check(hyp)
            if cache_check is not None:
                return cache_check
            print('test' + str(self.i))
            self.i += 1
            context = self.negative if type == POSITIVE_LABEL else self.positive
            j = 0
            for index, row in context.iterrows():
                j += 1
                if issuper(row, hyp):
                    cache.add(hyp, 0)
                    # print('j=0..' + str(j))
                    return 0
            print('j=0..' + str(j))
            cache.add(hyp, 1)
            return 1

        pos_hypothesis = self.positive.apply(lambda x: intersect(x, target), axis=1)
        pos_hypothesis = pos_hypothesis.dropna(how='all')
        pos_score = pos_hypothesis.apply(lambda x: test_hypothesis(x.dropna(), POSITIVE_LABEL), axis=1).sum() / len(
            pos_hypothesis)

        print('__________negative')
        self.i = 0

        neg_hypothesis = self.negative.apply(lambda x: intersect(x, target), axis=1)
        neg_hypothesis = neg_hypothesis.dropna(how='all')
        neg_score = neg_hypothesis.apply(lambda x: test_hypothesis(x.dropna(), NEGATIVE_LABEL), axis=1).sum() / len(
            neg_hypothesis)

        end = time()
        print(end - start)
        print('ps = ' + str(pos_score))
        print('neg = ' + str(neg_score))
        if pos_score > neg_score:
            return POSITIVE_LABEL
        if neg_score > pos_score:
            return NEGATIVE_LABEL
        return UNKNOWN_LABEL


if __name__ == '__main__':
    data = get_raw_data('data.csv')
    train = data.iloc[:8]
    test = data.iloc[8:]
