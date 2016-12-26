from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *
import random
from numpy_set_operations import *


class HeuristicsClassifier(AbstractClassifier):
    SEED1 = 12332513
    SEED2 = 43289
    random.seed(SEED2)

    def train(self, train_data):
        super().train(train_data)
        self.neg_dict = dict()
        self.pos_dict = dict()
        for c in self.positive.columns:
            self.pos_dict[c] = (self.positive[c].value_counts() / self.positive[c].value_counts().sum())
        for c in self.negative.columns:
            self.neg_dict[c] = (self.negative[c].value_counts() / self.negative[c].value_counts().sum())



    def predict(self, target, num_sub=None):
        target = target[:]
        del target['label']

        def test_hypothesis(hyp, type):
            if type == POSITIVE_LABEL:  # positive hypothesis, check in negative context
                score_dict = self.neg_dict
            else:  # negative hypothesis, check in positive context
                score_dict = self.pos_dict
            sc = 0
            max_score = 0
            for index, item in hyp.items():
                col_scores = score_dict[index]
                max_score += col_scores.max()
                try:
                    sc += col_scores[item]
                except KeyError:
                    pass
            if sc/max_score > self.threshold:
                return 0  # hypothesis holds in inverse context with high probability, no points for that
            else:
                return 1  # hypothesis does not hold in inverse context with high probability, 1 point earned

        pos_hypothesis = self.positive.apply(lambda x: intersect(x, target), axis=1)
        pos_hypothesis = pos_hypothesis.dropna(how='all')
        pos_score = pos_hypothesis.apply(lambda x: test_hypothesis(x.dropna(),
                                                                   POSITIVE_LABEL), axis=1).sum() / len(pos_hypothesis)

        neg_hypothesis = self.negative.apply(lambda x: intersect(x, target), axis=1)
        neg_hypothesis = neg_hypothesis.dropna(how='all')
        neg_score = neg_hypothesis.apply(lambda x: test_hypothesis(x.dropna(),
                                                                   NEGATIVE_LABEL), axis=1).sum() / len(neg_hypothesis)

        def score(pos, neg):
            return pos * 1. / (neg + 1)

        if score(pos_score, neg_score) > 0.1:
            return POSITIVE_LABEL
        elif score(neg_score, pos_score) > 0.1:
            return NEGATIVE_LABEL
        else:
            return UNKNOWN_LABEL
