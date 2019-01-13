import os

filedirectory = 'files/Man'
number = 4
for filename in os.listdir(filedirectory):
    if filename.endswith('.flac'):
        pos = filename.find('.')
        os.rename('files/Man/' + filename, 'files/Man/man0' + str(number) + '.wav')
        number = number + 1