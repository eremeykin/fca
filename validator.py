from aggregator import Aggregator
from classifier import AbstractClassifier, ImplicationClassifier
from data_preparation import *
from labels import *
from pprint import pprint
import math

__author__ = 'eremeykin'


class Validator(object):
    def __init__(self, data, classifier):
        self.data = data
        self.classifier = classifier
        self.aggregator = Aggregator()

    def test(self, test_frame=0.1):
        frame_l = math.floor(len(self.data) * test_frame)
        last = 0
        while last + frame_l < len(self.data):
            last += frame_l
            print(str(last)+'/'+str(len(self.data)))
            test_data = self.data[last - frame_l:last]
            train_data = pd.DataFrame().append(self.data[:last - frame_l]). \
                append(self.data[last:])
            self.classifier.train(train_data)
            self.aggregator.next()
            for index, example in test_data.iterrows():
                print(str(index))
                p_result = self.classifier.predict(example)
                self.aggregator.count(example, p_result)


if __name__ == "__main__":
    d = get_raw_data('data.csv')[:200]
    c = ImplicationClassifier(1.5)
    val = Validator(d, c)
    val.test(test_frame=0.1)
    pprint(val.aggregator.get_aggregate())
    val.aggregator.plot_3d_hist()
