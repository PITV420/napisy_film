import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
import pickle

def audio_reader(path):
    sampleRate, channel = wav.read(path)
    channel = channel/32768
    return channel, sampleRate

def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)

filenameData = 'files/Recognition/recognition_list'

with open(filenameData + '.p', 'rb') as file:
    recognition = pickle.load(file)

filenameData = 'files/Mix_S_3s_N_10s/orginal_framings'

with open(filenameData + '.p', 'rb') as file:
    basic = pickle.load(file)

licznik = 0
data = ["0dB", "6dB", "12dB", "18dB"]
figures = 1

errors = {}
averageErrors = {}

for keys in recognition:
    helper = {}
    toMean = []
    for keys2 in recognition[keys]:

        path = 'files/Mix_S_3s_N_10s/SNR_' + data[licznik] + '/' + keys2 + '.wav'
        file, fs = audio_reader(path)

        fig = plt.figure(figures, figsize=(8, 4), dpi=100)
        plt.plot(file, 'b-', recognition[keys][keys2], 'r-', basic[keys][keys2], 'g-')
        plt.ylim(-1.1, 1.1)
        plt.ylabel('Amp')
        plt.xlabel('t [s]')
        plt.xticks(np.arange(0, len(file), len(file)/20), ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5"])
        plt.title(keys2.replace('_', ', ') + ', SNR = ' + data[licznik])
        fig.savefig('files/Plots/SNR_' + data[licznik] + '/' + keys2 + '.png')
        plt.close(fig)
        figures = figures + 1

        wrongRec = np.round(np.sum(np.abs(np.subtract(recognition[keys][keys2], basic[keys][keys2])), axis=0)/len(recognition[keys][keys2]), 3)
        toMean.append(wrongRec)

        helper[keys2] = wrongRec

    errors[keys] = helper
    averageErrors[keys] = np.mean(toMean)

    figures = 1
    licznik = licznik + 1

save(errors, 'files/Recognition/errors.p')
save(averageErrors, 'files/Recognition/average_errors.p')