from python_speech_features import mfcc
import os
import numpy as np
from sklearn.mixture import GaussianMixture
import scipy.io.wavfile as wav
import parametrization
import computing_gmm
import pickle

def audio_reader(path):
    sampleRate, channel = wav.read(path)
    channel = channel/32768
    return channel, sampleRate

def recognize(data, cfg, gmm_model, Fs=16000, window_length=0.02, window_step=0.01):
    samplesInWindow = Fs*window_length
    step = Fs*window_step
    fft_size = 2
    timeMarkers = []
    while fft_size < cfg['window_length'] * Fs:
        fft_size *= 2
    recog = np.zeros(len(data), dtype=int)
    for k in range(int(len(data)/step)-1):
        MFCC = mfcc(data[int(k*step):int(k*step+samplesInWindow)], samplerate=Fs, nfft=fft_size, winlen=cfg['window_length'], winstep=cfg['window_step'],
                     numcep=cfg['cepstrum_number'], nfilt=cfg['filter_number'], preemph=cfg['preemphasis_filter'],
                     winfunc=cfg['window_function'])
        res = gmm_model.score(MFCC)
        if res >= -54:
            recog[int(k*step):int(k*step+samplesInWindow)]=1
            timeMarkers.append(k*step/Fs)
    return recog, timeMarkers

def averaging(data, Fs, window_step=0.5):
    samplesInWindow = Fs*window_step
    averaged = np.zeros(len(data), dtype=int)
    timeMarkers = []
    for k in range(int(len(data)/samplesInWindow)-1):
        if np.mean(data[int(k*samplesInWindow):int((k+1)*samplesInWindow)]) >= 0.8:
            averaged[int(k*samplesInWindow):int((k+1)*samplesInWindow)] = 1
            timeMarkers.append(k*samplesInWindow/Fs)

    return averaged, timeMarkers

def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)

def main(modelfile, configfile, samplesDirectory):

    config = parametrization.load_config(configfile)
    gmm = computing_gmm.load_data(modelfile)

    calc = {}
    markers = {}
    for fileName in os.listdir(samplesDirectory):
        if fileName.endswith('.wav'):
            data, fs = audio_reader(samplesDirectory + '/' + fileName)
            recog, time1 = recognize(data, config, gmm, fs)
            averaged, time2 = averaging(recog, fs)
            name = fileName[:fileName.find('.')]
            if not name in calc:
                calc[name] = averaged
                markers[name] = time2
            else:
                calc[name].update(averaged)
                markers[name].update(time2)
    return calc, markers

snrs = [0, 6, 12, 18]
dataAll = {}
markersAll = {}
licznik = 1
for i in snrs:
    directory = "files/Mix_S_3s_N_10s/SNR_" + str(i) + 'dB'
    currentData, currentMarkers = main("files/gmm/Speakers_gmm.p", "files/config/mfcc.cfg", directory)
    dataAll[str(licznik)] = currentData
    markersAll[str(licznik)] = currentMarkers
    licznik = licznik*2
save(dataAll, "files/Recognition/recognition_list.p")
save(markersAll, "files/Recognition/markers_list.p")