import math
from pprint import pprint

from aggregator import Aggregator
from classifiers.abstract_classifier import *
from classifiers import *
from classifiers.cached_implication_classifier import CachedImplicationClassifier
from classifiers.implication_classifier import ImplicationClassifier
from classifiers.my_classifier import MyClassifier
from classifiers.heuristics_classifier import HeuristicsClassifier
from data_preparation import *

__author__ = 'eremeykin'


class Validator(object):
    def __init__(self, data, classifier):
        self.data = data
        self.classifier = classifier
        self.aggregator = Aggregator()

    def validate(self, test_frame=0.1):
        frame_l = math.floor(len(self.data) * test_frame)
        last = 0
        while last + frame_l < len(self.data):
            print(str(last) + "/" + str(len(self.data)))
            last += frame_l
            test_data = self.data[last - frame_l:last]
            train_data = pd.DataFrame().append(self.data[:last - frame_l]). \
                append(self.data[last:])
            self.classifier.train(train_data)
            for index, example in test_data.iterrows():
                p_result = self.classifier.predict(example)
                print(index)
                self.aggregator.count(example, p_result)
            self.aggregator.next()


def try_one():
    c.train(d[:])
    print('Enter example with format:' + str(' '.join(d.columns[1:])))
    inp = input('>>')
    target = pd.Series(data=inp.split(','), index=d.columns)
    print(c.predict(target))


def validate():
    val = Validator(d, c)
    val.validate(test_frame=0.1)
    agr = val.aggregator.get_norm_aggregate()
    pprint('quality: ' + str((agr.positive_positive + agr.negative_negative) * 100.0))
    val.aggregator.plot_3d_hist()


if __name__ == "__main__":
    MODE = 'VALIDATE'
    d = get_raw_data('data.csv')[:500]
    c = HeuristicsClassifier(0.8)
    if MODE == 'TRY ONE':
        try_one()
    elif MODE == 'VALIDATE':
        from time import time
        start = time()
        validate()
        end = time()
        print(start-end)