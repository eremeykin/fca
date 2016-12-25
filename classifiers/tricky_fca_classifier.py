from classifiers.abstract_classifier import AbstractClassifier
from data_preparation import *


class TrickyFcaClassifier(AbstractClassifier):
    def __init__(self, threshold=1):
        super().__init__(threshold)
        self.neg_tree = dict()
        self.pos_tree = dict()

    def expand_dict(self, dct):
        for key, data in dct.items():
            fract_dict = dict()
            for c in data.columns:
                fract_dict[c] = (data[c].value_counts() / data[c].value_counts().sum())
            tree = dict()
            for k, v in fract_dict.items():
                for index, row in v.iteritems():
                    value = data[data[k] == index]
                    value = value.drop(k, 1)
                    tree[(k, index)] = value
            dct[key] = tree

    def build_check_tree(self):
        pos_dict = dict()
        for c in self.positive.columns:
            pos_dict[c] = (self.positive[c].value_counts() / self.positive[c].value_counts().sum())

        for k, v in pos_dict.items():
            for index, row in v.iteritems():
                value = self.positive[self.positive[k] == index]
                value = value.drop(k, 1)
                self.pos_tree[(k, index)] = value
        self.expand_dict(self.pos_tree)

        neg_dict = dict()
        for c in self.negative.columns:
            neg_dict[c] = (self.negative[c].value_counts() / self.negative[c].value_counts().sum())

        for k, v in neg_dict.items():
            for index, row in v.iteritems():
                value = self.negative[self.negative[k] == index]
                value = value.drop(k, 1)
                self.neg_tree[(k, index)] = value
        self.expand_dict(self.neg_tree)

    def train(self, train_data):
        super().train(train_data)
        self.build_check_tree()
        print('learned')

    def predict(self, target, num_sub=None):

        def test_hypothesis(hyp, type):
            if type == POSITIVE_LABEL:
                ctx = self.negative
                tree = self.neg_tree
            if type == NEGATIVE_LABEL:
                ctx = self.positive
                tree = self.pos_tree
            if len(hyp) < 1:
                return 0
            if len(hyp) < 2:
                return int(len(ctx[ctx[hyp.index[0]] == hyp[hyp.index[0]]]) != 0)
            c1 = (hyp.index[0], hyp[hyp.index[0]])
            c2 = (hyp.index[1], hyp[hyp.index[1]])
            try:
                search_space = tree[c1][c2]
            except KeyError:
                print('1')
                return 0
            hyp = hyp.drop(hyp.index[0])
            hyp = hyp.drop(hyp.index[0])
            for index, row in search_space.iterrows():
                if issuper(row, hyp):
                    return 0
            return 1

        pos_hypothesis = self.positive.apply(lambda x: intersect(x, target), axis=1)
        pos_hypothesis = pos_hypothesis.dropna(how='all')

        # print('target: \n'+ str(target))
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
