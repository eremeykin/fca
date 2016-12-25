from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *


class CachedFcaClassifier(AbstractClassifier):
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
            hyp = frozenset(zip(hypothesis.index, hypothesis))
            try:
                res = self.exact[hyp]
                self.s0 += 1
                return res
            except KeyError:
                pass
            L = len(hyp)
            for l in range(L, self.max_len):
                try:
                    for key, value in self.storage[l].items():
                        if value == 1 and key.issubset(hyp):
                            # print('success1')
                            self.s1 += 1
                            return 1
                except KeyError as e:
                    pass

            for l in range(L, self.max_len):
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
        self.p_cache = CachedFcaClassifier.Cache()
        self.n_cache = CachedFcaClassifier.Cache()

    def train(self, train_data):
        super().train(train_data)
        self.p_cache = CachedFcaClassifier.Cache()
        self.n_cache = CachedFcaClassifier.Cache()

    @staticmethod
    def intersect(x, y):
        return set(zip(x.index, x.values)) & set(zip(y.index, y.values))

    def predict(self, target, num_sub=None):

        def test_hypothesis(hyp, type):
            if type == POSITIVE_LABEL:
                cache = self.p_cache
            if type == NEGATIVE_LABEL:
                cache = self.n_cache
            cache_check = cache.check(hyp)
            if cache_check is not None:
                return cache_check
            context = self.negative if type == POSITIVE_LABEL else self.positive
            j = 0
            for index, row in context.iterrows():
                j += 1
                if issuper(row, hyp):
                    cache.add(hyp, 0)
                    return 0
            cache.add(hyp, 1)
            return 1

        pos_hypothesis = self.positive.apply(lambda x: intersect(x, target), axis=1)
        pos_hypothesis = pos_hypothesis.dropna(how='all')
        pos_score = pos_hypothesis.apply(lambda x: test_hypothesis(x.dropna(),
                                                                   POSITIVE_LABEL), axis=1).sum() / len(pos_hypothesis)

        neg_hypothesis = self.negative.apply(lambda x: intersect(x, target), axis=1)
        neg_hypothesis = neg_hypothesis.dropna(how='all')
        neg_score = neg_hypothesis.apply(lambda x: test_hypothesis(x.dropna(),
                                                                   NEGATIVE_LABEL), axis=1).sum() / len(neg_hypothesis)

        if pos_score > neg_score:
            return POSITIVE_LABEL
        if neg_score > pos_score:
            return NEGATIVE_LABEL
        return UNKNOWN_LABEL
