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
    position2 = file.find('.')
    return samples, rate, file[position+1] + '_' + file[:position], path


def saveSpeakers(data, name):
    """
    Changing data save format

    Returns data as a list of lists in following order:

    Gender:     Man,    Woman,
    Number:
    1:          data    data
    2:          data    data
    3:          data    data
    ...         ...     ...

    Access elements by restructured[Digit index][Gender index]
    """
    createObj = []
    for i in range(4):
        createObj.append([])

    for key in data:
        createObj[int(key[0])].append(data[key])

    file = open(name, 'wb')
    pickle.dump(createObj, file)

def saveNoise(data, name):
    """
    Changing data save format

    Returns data as a list of lists in following order (alphabetically):

    Name:       Crowd,   Jazz,    ...
    Number:
    1:          data    data
    2:          data    data
    3:          data    data
    ...         ...     ...

    Access elements by restructured[Digit index][Gender index]
    """
    createObj = []
    for i in range(2):
        createObj.append([])

    for key in data:
        createObj[int(key[0])].append(data[key])

    file = open(name, 'wb')
    pickle.dump(createObj, file)

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

        if j < 1:
            saveNoise(samples, 'files/samplesNoise.p')
        else:
            saveSpeakers(samples, 'files/samplesSpeaker.p')

main()
