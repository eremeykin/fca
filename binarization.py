__author__ = 'eremeykin'
import pandas as pd

headers = {
    '0': 'label',
    '1': 'cap-shape',
    '2': 'cap-surface',
    '3': 'cap-color',
    '4': 'bruises',
    '5': 'odor',
    '6': 'gill-attachment',
    '7': 'gill-spacing',
    '8': 'gill-size',
    '9': 'gill-color',
    '10': 'stalk-shape',
    '11': 'stalk-root',
    '12': 'stalk-surface-above-ring',
    '13': 'stalk-surface-below-ring',
    '14': 'stalk-color-above-ring',
    '15': 'stalk-color-below-ring',
    '16': 'veil-type',
    '17': 'veil-color',
    '18': 'ring-number',
    '19': 'ring-type',
    '20': 'spore-print-color',
    '21': 'population',
    '22': 'habitat'
}


def expand_feature(feature, dframe):
    unique_value = feature.unique()
    for value in unique_value:
        dframe[feature.name + value] = (feature == value).apply(int)
    return dframe


def get_raw_data():
    data = pd.read_csv('data_set/data.csv', index_col=False)
    label = data['label']
    del data['label']
    return data, label


def get_data():
    df, ds = get_raw_data()
    data = pd.DataFrame()
    label = pd.Series()
    for f in df.columns:
        data = expand_feature(df[f], data)
    label = expand_feature(ds, label)['labele']
    label.name = 'label'
    return data, label


def intersect(target, row):
    return target == row


if __name__ == "__main__":
    d, l = get_raw_data()
    print(l)
    print(intersect(d.loc[1], d.loc[0]))