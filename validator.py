from aggregator import Aggregator
from classifier import *
from data_preparation import *
from pprint import pprint
import math
import numpy as np
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
            last += frame_l
            test_data = self.data[last - frame_l:last]
            train_data = pd.DataFrame().append(self.data[:last - frame_l]). \
                append(self.data[last:])
            self.classifier.train(train_data)
            for index, example in test_data.iterrows():
                p_result = self.classifier.predict(example)
                self.aggregator.count(example, p_result)
            self.aggregator.next()


def try_one():
    d = get_raw_data('data.csv')
    print('Enter example with format:' + str(d.columns))
    inp = input('>>')
    target = pd.Series(data=inp.split(','), index=d.columns)
    c = MyClassifier2(1)
    c.train(d[:100])
    print(c.predict(target))


def validate():
    d = get_raw_data('data.csv')[:]  # .sample(n=4000, random_state=8755)
    c = MyClassifier2(0.95)
    val = Validator(d, c)
    val.validate(test_frame=0.1)
    agr = val.aggregator.get_norm_aggregate()
    pprint('quality: ' + str((agr.positive_positive + agr.negative_negative) * 100.0))
    val.aggregator.plot_3d_hist()

if __name__ == "__main__":
    MODE = 'VALIDATE'
    if MODE == 'TRY ONE':
        try_one()
    elif MODE == 'VALIDATE':
        validate()
