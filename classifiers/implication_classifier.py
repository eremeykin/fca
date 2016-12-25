from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *
import random
from numpy_set_operations import *

class ImplicationClassifier(AbstractClassifier):
    SEED1 = 12332513
    SEED2 = 43289
    random.seed(SEED2)

    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']
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
