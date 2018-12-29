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
    position = file.find('0')
    return samples, rate, file[position+1] + '_' + file[:position], path

def save(data, name, number):
    """
    Changing data save format

    Returns data as a list of lists in following order (oposit-alphabetical):

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
    for i in range(number):
        createObj.append([])
        keys.append([])

    for key in data:
        createObj[int(key[0])].append(data[key])
        position = key.find('_')
        keys[int(key[0])].append(key[position+1:]+'0'+key[position-1])


    file = open(name+'.p', 'wb')
    pickle.dump(createObj, file)

    fileKeys = open(name+'_keys.p', 'wb')
    pickle.dump(keys, fileKeys)

def reconstruct(filenameData):
    """
    Reconstructing data & attaching keys to samples

    for example:

    woman00: array([samples]), man00: array([samples]), ...

    Access elements using keys
    """
    with open(filenameData+'.p', 'rb') as file:
        data = pickle.load(file)
    with open(filenameData+'_keys.p', 'rb') as keys:
        keys = pickle.load(keys)
    reconstructed = {}
    for i in range(len(keys)):
        for j in range(len(keys[i])):
            reconstructed[keys[i][j]] = data[i][j]

    print(reconstructed['woman00'])
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
                samples[data_[2]] = data_[0]
                print(samples)
        if j < 1:
            save(samples, 'files/samplesNoise', 2)
        else:
            save(samples, 'files/samplesSpeaker', 5)
