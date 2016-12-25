from close_by_one import *
from numpy_set_operations import intersect, issuper

__author__ = 'eremeykin'
import pandas as pd


class Context(object):
    def __init__(self, matrix):
        self.df = matrix
        self.g_size = self.df.shape[0]
        self.m_size = self.df.shape[1]

    def g_to_d(self, objects):
        if len(objects) < 1:
            return None
        res = self.df.loc[objects[0]]
        for obj in objects[1:]:
            res = intersect(res, self.df.loc[obj])
        return res

    @staticmethod
    def fit(what, description):
        if description is None:
            return True
        return what[description.index].equals(description)

    def d_to_g(self, descr):
        meets = self.df.apply(lambda x: Context.fit(x, descr), axis=1)
        return list(self.df[meets].index)

    def objects_names(self):
        return sorted(list(self.df.index))

    def attributes_names(self):
        return sorted(list(self.df.columns))

    def transpose(self):
        self.df = self.df.transpose()
        self.g_size = self.df.shape[0]
        self.m_size = self.df.shape[1]

    def __str__(self):
        return str(self.df)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return True  # self.df == other.df


if __name__ == "__main__":
    df = pd.DataFrame(data=[[1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 0], [0, 1, 1, 1]], index=['g1', 'g2', 'g3', 'g4'],
                      columns=['m1', 'm2', 'm3', 'm4'])
    c = Context(df)

    df = pd.DataFrame(data=[['x', 's', 'n', 't'],
                            ['x', 's', 'y', 't'],
                            ['b', 's', 'w', 't'],
                            ['x', 'y', 'w', 't'],
                            ['x', 's', 'g', 'f'],
                            ['x', 'y', 'y', 't'],
                            ['b', 's', 'w', 't'],
                            ['b', 'y', 'w', 't']], index=['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'],
                      columns=['m1', 'm2', 'm3', 'm4'])

    df = pd.DataFrame(data=[['x', 's', 'n', 't'],
                            ['x', 's', 'y', 't'],
                            ['b', 's', 'w', 't'],
                            ['x', 'y', 'w', 't'],
                            ['b', 'y', 'w', 't']], index=['g1', 'g2', 'g3', 'g4', 'g5'],
                      columns=['m1', 'm2', 'm3', 'm4'])
    c = Context(df)
    print(c)
    print()

    from pprint import pprint
    print(len(close_by_one(c)))
    for concept in close_by_one(c):
        print()
        pprint(concept)

