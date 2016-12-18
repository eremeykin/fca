__author__ = 'eremeykin'
from data_preparation import *
import pandas as pd


class Classifier(object):
    def __init__(self, learn_data):
        self.positive = learn_data[learn_data['label'] == 'e']
        self.negative = learn_data[learn_data['label'] == 'p']
        del self.positive['label']
        del self.negative['label']

    @staticmethod
    def _intersect(row1, row2):
        return row1[row1 == row2]

    @staticmethod
    def _issuper(sup, sub):
        sup[sub.index].equals(sub)

    def predict(self, target):
        positive_score = 0
        print('\n<target>')
        print(target)
        print('</target>\n')
        for index_p, row_p in self.positive.iterrows():
            intersect = Classifier._intersect(target, row_p)
            for index_n, row_n in self.negative.iterrows():
                if Classifier._issuper(row_n, intersect):
                    pass
                else:
                    positive_score += 1
        negative_score = 0
        for index_n, row_n in self.negative.iterrows():
            intersect = Classifier._intersect(target, row_n)
            for index_p, row_p in self.positive.iterrows():
                if not Classifier._issuper(row_p, intersect):
                    negative_score += 1
        print('p: ' + str(positive_score) + ' n: ' + str(negative_score))


if __name__ == '__main__':
    data = get_raw_data('data0.csv')
    train = data.iloc[:8]
    test = data.iloc[8:]
    test_label = test['label']
    del test['label']
    print(train)
    c = Classifier(train)
    predicted = pd.Series(None, index=test.index)
    print(test)
    for index, row in test.iterrows():
        c.predict(row)
        # test['predicted'] = predicted
        # print(test[['label', 'predicted']])
        # print((test['label'] == test['predicted']).sum())


