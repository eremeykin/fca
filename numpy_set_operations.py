import pandas as pd


def intersect(row1, row2):
    if not isinstance(row1, pd.Series) or not isinstance(row2, pd.Series):
        raise Exception('Wrong type: sup-> ' + str(type(sup)) +
                        ' sub-> ' + str(type(sub)) +
                        ' Must be pandas.Series')
    row1 = row1[row2.index]
    return row1[row1 == row2]


def issuper(sup, sub):
    if not isinstance(sup, pd.Series) or not isinstance(sub, pd.Series):
        raise Exception('Wrong type: sup-> ' + str(type(sup)) +
                        ' sub-> ' + str(type(sub)) +
                        ' Must be pandas.Series')
    sub = sub.dropna()
    return sup[sub.index].equals(sub)



if __name__ == "__main__":
    import pandas as pd

    df1 = pd.Series(['x', 'y', 'z', 'u', 'i', 'p'], index=['a', 'b', 'c', 'd', 'e', 'f'])
    import numpy as np
    df2 = pd.Series(['x', 'y', 'z', 'u', 'i', np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])
    print(df1)
    print(df2)
    print(issuper(df1, df2))
    print(intersect(df1, df2))
