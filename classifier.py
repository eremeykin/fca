__author__ = 'eremeykin'
from data_preparation import get_data
import pandas as pd

class Classifier(object):
    def __init__(self, learn_data):
        self.positive = learn_data[learn_data['label'] == 1]
        self.negative = learn_data[learn_data['label'] == 0]

    def hamming(self, row1, row2):
        n = len(row1)
        res = 0
        for i in range(n):
            row1v = row1[i]
            row2v = row2[i]
            if row1v != row2v:
                res += 1
        return res

    def predict(self, entity):
        score_p = 0
        score_n = 0
        for index, row in self.positive.iterrows():
            score_p += self.hamming(row, entity)
        for index, row in self.negative.iterrows():
            score_n += self.hamming(row, entity)
        return score_p / len(self.positive) < score_n / len(self.negative)


if __name__ == '__main__':
    data = get_data()
    train = data.iloc[:100]
    test = data.iloc[100:180]
    print(len(train))
    print(len(test))
    c = Classifier(train)
    predicted = pd.Series(None, index=test.index)
    for index, row in test.iterrows():
        predicted[index] = c.predict(row)
        print(index)
    test['predicted'] = predicted
    print(test[['label', 'predicted']])
    print((test['label']==test['predicted']).sum())


