from pandas import DataFrame
import pickle
import parametrization


def recognize(m):
    """"
    :param m: rr_matrix
    :return: list of indexes that have a non-zero value,
         list of percentage recognition for each digit
    """

    recognition_idx = []
    recognition = []
    for i in range(len(MFCC_labels)):
        for j in range(len(MFCC_labels[0])):
            if not m[i][j] == 0:
                recognition_idx.append([i, j])
            if i == j:
                recognition.append(m[i][j])
    return recognition_idx, recognition

toLoop = [-1, 0, 1, 2, 4, 8]
""""
for k in toLoop:
    if k == -1:
        name = 'Speakers'
    elif k == 0:
        name = 'Noises'
    else:
        name = 'Mixed_snr_1_' + str(k)
    MFCC = parametrization.reconstruct('files/parametrization/parametrized_' + name)

    MFCC_labels = []

    with open('files/cross_val/crossVal_'+name+'.p', 'rb') as file:
        matrix1 = pickle.load(file)
        matrix = []
    for i in range(len(matrix1)):
        helper = []
        for k in range(len(matrix1[i])):
            helper.append(matrix1[i][k][0])
        matrix.append(helper)

    
"""

with open('files/Recognition/errors.p', 'rb') as file:
    matrix1 = pickle.load(file)
    print(matrix1)

matrix2 = []
names = []
toSave = []

for key in matrix1:
    helper = []
    for key2 in matrix1[key]:
        gender = key2[:key2.find("_")]

        helper.append(matrix1[key][key2])
    toSave.append(helper)
    names.append(key)
    names.append(helper)

names.append(matrix2)
import_ = DataFrame(toSave)


import_.to_excel('recognition_errors.xlsx', index=False, startrow=1, startcol=1)