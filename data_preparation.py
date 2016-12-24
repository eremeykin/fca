__author__ = 'eremeykin'
import pandas as pd

POSITIVE_LABEL = 'e'
NEGATIVE_LABEL = 'p'
UNKNOWN_LABEL = 'u'
BOTH_LABEL = 'b'


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


def _expand_feature(feature, dframe):
    """ expand feature from multi-valued to several 0/1 valued features"""
    unique_value = feature.unique()
    for value in unique_value:
        dframe[feature.name + value] = (feature == value).apply(int)
    return dframe

def get_raw_data(file_name):
    """ returns data as is, in multi-valued form """
    data = pd.read_csv('data_set/' + file_name, index_col=False)
    data = data.sample(frac=1, random_state=22362 )
    return data


def get_data(file_name):
    """ returns expended data in 0/1 form """
    df = get_raw_data(file_name)
    data = pd.DataFrame()
    label = pd.Series()
    label = _expand_feature(df['label'], label)['labele']
    label.name = 'label'
    data['label'] = label
    for f in df.columns[1:]:
        data = _expand_feature(df[f], data)
    return data



if __name__ == "__main__":
    d = get_data('data0.csv')
    print(d)
