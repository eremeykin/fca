from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *
import random
from numpy_set_operations import *


class CachedImplicationClassifier(AbstractClassifier):
    SEED1 = 12332513
    SEED2 = 43289
    random.seed(SEED2)

    class Cache(object):

        def __init__(self):
            self.storage = dict()

        def add(self, hyp, value):
            hyp = frozenset(zip(hyp.index, hyp))
            self.storage[hyp] = value

        def check(self, hyp):
            hyp = frozenset(zip(hyp.index, hyp))
            return self.storage.get(hyp, None)

    def train(self, train_data):
        super().train(train_data)
        self.pos_cache = CachedImplicationClassifier.Cache()
        self.neg_cache = CachedImplicationClassifier.Cache()

    def predict(self, target, num_sub=None):

        target = target[:]
        del target['label']
        if num_sub is None:
            num_sub = len(target) // 2
        neg = 0
        pos = 0
        for i in range(num_sub):
            t = target.sample(n=random.randrange(len(target)),
                              random_state=CachedImplicationClassifier.SEED1)
            pcache_check = self.pos_cache.check(t)
            if pcache_check is None:
                p_delta = self.positive.apply(lambda x: int(issuper(x, t)), axis=1).sum()
                self.pos_cache.add(t, p_delta)
                pos += p_delta
            else:
                pos += pcache_check

            ncache_check = self.neg_cache.check(t)
            if ncache_check is None:
                n_delta = self.negative.apply(lambda x: int(issuper(x, t)), axis=1).sum()
                self.neg_cache.add(t, n_delta)
                neg += n_delta
            else:
                neg += ncache_check

        def score(pos, neg):
            return pos * 1. / (neg + 1)

        if score(pos, neg) > self.threshold:
            return POSITIVE_LABEL
        elif score(neg, pos) > self.threshold:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL
