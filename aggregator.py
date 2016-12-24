from pprint import *
from data_preparation import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

__author__ = 'eremeykin'


class ScoreCounter(object):
    def __init__(self):
        self.positive_positive = 0
        self.positive_negative = 0
        self.negative_positive = 0
        self.negative_negative = 0
        self.unknown = 0
        self.both = 0

    def total(self):
        return self.positive_positive + \
               self.positive_negative + \
               self.negative_positive + \
               self.negative_negative + \
               self.unknown + \
               self.both

    def count(self, example, result):
        if result == UNKNOWN_LABEL:
            self.unknown += 1
            return
        if result == BOTH_LABEL:
            self.both += 1
            return
        if example['label'] == POSITIVE_LABEL and result == POSITIVE_LABEL:
            self.positive_positive += 1
        if example['label'] == POSITIVE_LABEL and result == NEGATIVE_LABEL:
            self.positive_negative += 1
        if example['label'] == NEGATIVE_LABEL and result == POSITIVE_LABEL:
            self.negative_positive += 1
        if example['label'] == NEGATIVE_LABEL and result == NEGATIVE_LABEL:
            self.negative_negative += 1

    def __str__(self):
        return " p_p: " + str(self.positive_positive) + \
               " p_n: " + str(self.positive_negative) + \
               " n_p: " + str(self.negative_positive) + \
               " n_n: " + str(self.negative_negative) + \
               " u: " + str(self.unknown) + \
               " b: " + str(self.both)

    def __repr__(self):
        return str(self)


class Aggregator(object):
    def __init__(self):
        self.counters = []
        self.counter = ScoreCounter()

    def get_aggregate(self):
        final_counter = ScoreCounter()
        final_counter.positive_positive = np.average([x.positive_positive for x in self.counters])
        final_counter.positive_negative = np.average([x.positive_negative for x in self.counters])
        final_counter.negative_positive = np.average([x.negative_positive for x in self.counters])
        final_counter.negative_negative = np.average([x.negative_negative for x in self.counters])
        final_counter.unknown = np.average([x.unknown for x in self.counters])
        final_counter.both = np.average([x.both for x in self.counters])
        return final_counter

    def get_norm_aggregate(self):
        final_counter = self.get_aggregate()
        total = final_counter.total()
        final_counter.positive_positive /= total
        final_counter.positive_negative /= total
        final_counter.negative_positive /= total
        final_counter.negative_negative /= total
        final_counter.unknown /= total
        final_counter.both /= total
        return final_counter

    def plot_3d_hist(self, norm=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = [0.5, 0.5, 1.5, 1.5]  # x coordinates of each bar
        y = [0.5, 1.5, 0.5, 1.5]  # y coordinates of each bar
        z = [0, 0, 0, 0]  # z coordinates of each bar
        dx = [0.95, 0.95, 0.95, 0.95]  # width of each bar
        dy = [0.95, 0.95, 0.95, 0.95]  # depth of each bar
        agr = self.get_norm_aggregate()
        if not norm:
            agr = self.get_aggregate()
        dz = [agr.positive_negative, agr.positive_positive, agr.negative_negative,
              agr.negative_positive]  # height of each bar
        col = ['r', 'b', 'b', 'r']
        ax.bar3d(x, y, z, dx, dy, dz, color=col, zsort='average')
        axes = plt.gca()
        axes.set_zlim([0, 1])
        plt.show()

    def next(self):
        print('last result: '+str(self.counter))
        self.counters.append(self.counter)
        self.counter = ScoreCounter()

    def count(self, example, result):
        self.counter.count(example, result)

    def __str__(self):
        return pformat(self.counters)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    a = Aggregator()
    a.plot_3d_hist()
