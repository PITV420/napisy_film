from pandas import DataFrame
from cross_valid import matrix_

matrix = matrix_
digits = [0, 1, 2, 3]
gender = ['man', 'woman']
empty = []

for i in range(4):
    empty.append(" ")


def recognize(m):
    """
    :param m: rr_matrix
    :return: list of indexes that have a non-zero value,
             list of percentage recognition for each digit
    """
    recognition_idx = []
    recognition = []
    for i in range(gender):
        for j in range(digits):
            if not m[i][j] == 0:
                recognition_idx.append([i, j])
            if i == j:
                recognition.append(m[i][j])
    return recognition_idx, recognition


idx, rec = recognize(matrix)

correct = []
mistake = []

for i in range(10):
    correct.append('correct')
    mistake.append(0)

for pair in idx:
    if not pair[0] == pair[1]:
        correct[pair[0]] = 'Recognition ' + str(pair[0])+' as ' + str(pair[1])
        mistake[pair[0]] = matrix[pair[0], pair[1]]


import_ = DataFrame({'Digit': digits, '0': matrix[0], '1': matrix[1], '2': matrix[2],
                     '3': matrix[3], '4': matrix[4], '5': matrix[5], '6': matrix[6],
                     '7': matrix[7], '8': matrix[8], '9': matrix[9],
                     ' ': empty, 'Recognition [%]': rec,
                     'Wrong recognition': correct, 'Wrong rec. [%]': mistake})


import_.to_excel('recognition.xlsx', index=False, startrow=1, startcol=1)