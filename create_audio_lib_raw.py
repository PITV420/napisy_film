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
    return samples, rate, file, path

def save(data, name):
    """
    Changing data save format
    Returns data as a list of lists in following order (alphabetical):
    Name:      Traffic, Restaurant,    ...
    Number:
    0:          data    data
    1:          data    data
    2:          data    data
    ...         ...     ...
    Access elements by restructured[Number index][Name index]
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
    Reconstructing data & attaching keys to samples
    for example:
    woman00: array([samples]), ...
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
        for j in range(len(keys[i])):
            reconstructed[names[i]+'0'+keys[i][j]] = data[i][j]

    return reconstructed

def main():
    for j in range(2):
        samples = {}
        fileDirectory = ''

        if j<1:
            fileDirectory = 'files/Noises'
        else:
            fileDirectory = 'files/Speakers'

        for fileName in os.listdir(fileDirectory):
            if fileName.endswith('.wav'):
                data_ = getData(fileDirectory, fileName)
                getNum = data_[2][data_[2].find('0')+1]
                getNam = data_[2][:data_[2].find('0')]
                helper = {}
                helper[getNum] = data_[0]
                if not getNam in samples:
                    samples[getNam] = helper
                else:
                    samples[getNam].update(helper)
        if j<1:
            save(samples, 'files/samples/samplesNoises')
        else:
            save(samples, 'files/samples/samplesSpeakers')
