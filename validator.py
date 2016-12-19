from aggregator import Aggregator
from classifier import *
from data_preparation import *
from labels import *
from pprint import pprint
import math
import numpy as np
from time import time

__author__ = 'eremeykin'


class Validator(object):
    def __init__(self, data, classifier):
        self.data = data
        self.classifier = classifier
        self.aggregator = Aggregator()

    def validate(self, test_frame=0.1, once=False):
        start_time = time()
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
            if once:
                break
        end_time = time()
        # print('time = ' + str(end_time - start_time))


if __name__ == "__main__":
    d = get_raw_data('data.csv') #.sample(n=4000, random_state=8755)
    # c = ImplicationClassifier(1.3)
    for t in np.arange(0.85, 1, 0.01):
        print('t = '+ str(t))
        c = MyClassifier(t)
        val = Validator(d, c)
        val.validate(test_frame=0.1)
        agr = val.aggregator.get_norm_aggregate()
        pprint((agr.positive_positive+agr.negative_negative)*100.0)
        # val.aggregator.plot_3d_hist()
