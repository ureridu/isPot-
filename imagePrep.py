# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 06:31:03 2018

@author: Ureridu
"""

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.utils import to_categorical
from collections import defaultdict, UserDict
import numpy as np
import pandas as pd
import os


class mDict(UserDict):
    def __missing__(self, key):
        self.data[key] = mDict()
        return self.data[key]

    def __add__(self, i):
        self.safety(i)
        self.data = type(i)() + i
        return self.data

    def append(self, i):
        self.safety(i)
        self.data = [i]
        return self.data

    def safety(self, i):
        if self.data:
            raise TypeError('Cannot Overwrite Existing Data')




def loadData(file):
    ''' Load DB Downloads '''
    if '.tsv' not in file:
        raise TypeError('File must be .TSV (Tab Delim)')

    ' Open file and dump into dataframe '
    with open(file, 'r') as infile:
        data = infile.read()

    data = [[cell for cell in lines.split('\t')] for lines in data.split('\n')]
    ''' The full DB download gives me an extra column not included as a header column
        DF conversion is handled this way to keep it robust '''
    data = pd.DataFrame(data)
    data.columns = data.loc[0, :]
    data.drop(0, axis=0, inplace=True)

    ' Clean the data up just a little bit, Vase Num will be used as the index, so we only want records that have it '
    if 'Vase Number' not in data.columns:
        data['Vase Number'] = [nam.split(' ')[-1] if nam != None else None for nam in data['Record Title']]
    ' the full db download has a None col that needs to be removed '
    if None in data.columns:
        data = data[data.columns[:-1]]

    data = data[pd.to_numeric(data['Vase Number'], errors='coerce').notnull()]
    data['Vase Number'] = data['Vase Number'].astype(int)

    return data


def oneHot(arr):
    ' one hot encode y '

    ' Simplify category types '

    ' create a dictionary of string labels to numerical labels '
    key = set(arr)
    key = {k: i for i, k in enumerate(key)}

    ' create array of numerical labels '
    arr = np.array([key[x] for x in arr])
    return to_categorical(arr), key




def makeData(yCol='Shape Name', removeFrag=True, simplify=True, dropQuest=True):
    ''' Funk takes desired yCol and flag for removing incomplete vases
        and outputs train & test data '''

    ' Load and merge the 2 db files '
    data = pd.concat([loadData('db.tsv').set_index('Vase Number'),
                      loadData('db abr.tsv').set_index('Vase Number')],
                      join='inner', axis=1)

    ' drop duplicated columns  '
    data = data.loc[:, ~data.columns.duplicated()]
    ' Make sure user chosen Y value is a valid column '
    if yCol not in data.columns:
        raise TypeError('yCol not found, please select from: %s' % ', '.join(set(data.columns)))

    ' Quick Cleanup on the y Column '
    data = data[data[yCol] != '']
    data = data[data[yCol].notnull()]

    ' limit df to only complete items '
    if removeFrag:
        data = data[~data['Shape Name Condition'].str.contains('FRAGMENT')]
        data = data[~data['Shape Name'].str.contains('FRAGMENT')]

    ' remove labels that are "uncertain" '
    if dropQuest:
        data = data[~data[yCol].str.contains('?', regex=False)]
    data = data[~data[yCol].str.contains('UNKNOWN')]

    ' grab only the first word from a comma sep list (eg: Amphora, Neck) '
    if simplify:
         data[yCol] = [x.split(', ')[0] for x in data[yCol]]

    ' Create X & y '
    X = np.array(data.index)
    y, key = oneHot(data[yCol])


    return train_test_split(X, y, test_size=.33, random_state=42), key, data


def perPic(inter_x, inter_y):
#    y = np.array([None] * len(inter_y[0])).reshape(1, 168)
    y = []
    x = []
#    x = np.array([None])
#    yy_train = np.array([list(np.tile(y_train[i], (count[str(vase)], 1))) for i, vase in enumerate(X_train)])

    for i, vase in enumerate(inter_x):
#        print(i)
        c = count[str(vase)]
#        z = np.tile(inter_y[i], (c, 1))
#        print(z)
#        y = np.concatenate((y, z), axis=0)
        y += [inter_y[i]] * c
        x += [vase] * c
#        x = np.concatenate((x, np.repeat(vase, c)), axis = 0)
    return np.array(x), np.array(y)


(inter_X_train, inter_X_test, inter_y_train, inter_y_test), key, data = makeData()

imgPath = os.getcwd() + '/images/'
z=np.ndarray([])
images = [[x.split('__')[0], x] for x in os.listdir(imgPath) if 'BEIL' not in x and 'FIG' not in x and 'NOTE' not in x]


#count = mDict()
count=defaultdict(int)
imgLookup = mDict()
for vaseNo, imgName in images:
    count[vaseNo] += 1
    imgLookup[vaseNo] += imgName

x_train, y_train = perPic(inter_X_train, inter_y_train)

#imgArr = (img_to_array(load_img(imgPath + img)) for img in images[:])
#bad = []
#for img in images[:]:
#    try:
#        ld = load_img(imgPath + img)
#        ldAr = img_to_array(ld)
##        z = np.append(z, [ldAr])
#    except:
##        os.remove(imgPath + img)
#        bad.append(img)

'BEIL, FIG, NOTE'