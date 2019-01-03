import pickle
import os
import scipy.io.wavfile as wav

def audio_reader(path):
    sampleRate, channel = wav.read(path)
    channel = channel/32768
    return channel, sampleRate

def getData(directory, file):
    path = directory + '/' + file
    samples, rate = audio_reader(path)
    file = file[:file.find('.')]
    gender = file[:file.find('_')]
    noise = file[file.find('_')+1:]

    return samples, rate, gender, noise, path

def save(data, name):
    """
    Changing data save format

    Returns data as a list of lists in following order (alphabetical):

    Noise:      crowd00, crowd01, jazz01,    ...
    Gender:
    man00:      data     data     data
    man01:      data     data     data
    man02:      data     data     data
    ...         ...      ...      ...

    First array in "keys" file is a name of gender (first column)
    Access elements by restructured[Gender index][Noise index]
    """
    createObj = []
    keys = []
    dataSorted = sorted(data)

    for i in dataSorted:
        createObj.append([])
        keys.append([])

    keys.append([])

    number = 0
    for j in dataSorted:
        keys[0].append(j)
        dataSorted2 = sorted(data[j])
        for k in dataSorted2:
            createObj[number].append(data[j][k])
            keys[number+1].append(k)
        number += 1

    file = open(name+'.p', 'wb')
    pickle.dump(createObj, file)

    fileKeys = open(name+'_keys.p', 'wb')
    pickle.dump(keys, fileKeys)

def reconstruct(filenameData):
    """
    Reconstructing data & attaching noise's keys to samples and than to the speakers

    for example:

    woman00: {traffic00: array([samples]) ...}, ...

    Access elements using keys
    """
    with open(filenameData+'.p', 'rb') as file:
        data = pickle.load(file)
    with open(filenameData+'_keys.p', 'rb') as keys:
        keys = pickle.load(keys)
    names = keys[0]
    keys = keys[1:]
    reconstructed = {}
    for i in range(len(keys)):
        helper = {}
        for j in range(len(keys[i])):
            helper[keys[i][j]] = data[i][j]
            if not names[i] in reconstructed:
                reconstructed[names[i]] = helper
            else:
                reconstructed[names[i]].update(helper)

    return reconstructed

def main():
    SNRS = [1, 2, 4, 8]
    for j in SNRS:
        samples = {}

        fileDirectory = 'files/Mixed_snr_1_' + str(j)


        for fileName in os.listdir(fileDirectory):
            if fileName.endswith('.wav'):
                data_ = getData(fileDirectory, fileName)
                helper = {}
                helper[data_[3]] = data_[0]
                if not data_[2] in samples:
                    samples[data_[2]] = helper
                else:
                    samples[data_[2]].update(helper)
        save(samples, 'files/samplesMixed_snr_1_' + str(j))