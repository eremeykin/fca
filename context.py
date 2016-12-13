__author__ = 'eremeykin'
import pandas as pd


class Context(object):
    def __init__(self, matrix):
        self.df = matrix
        self.g_size = self.df.shape[0]
        self.m_size = self.df.shape[1]

    def m_to_g(self, attributes):
        mask = pd.Series(data=True, index=self.df.index)
        for a in attributes:
            mask = mask & self.df[a]
        return list(mask[mask].index)

    def g_to_m(self, objects):
        mask = pd.Series(data=True, index=self.df.columns)
        for o in objects:
            mask = mask & self.df.loc[o]
        return list(mask[mask].index)

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
        return True# self.df == other.df


if __name__ == "__main__":
    df = pd.DataFrame(data=[[1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 0], [0, 1, 1, 1]], index=['g1', 'g2', 'g3', 'g4'],
                      columns=['m1', 'm2', 'm3', 'm4'])
    c = Context(df)
    print(c)
    print(c.m_to_g(['m1', 'm3']))
    print(c.g_to_m(['g1']))