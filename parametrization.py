from python_speech_features import mfcc, delta
import scipy.io.wavfile as wav
import numpy as np
import os
import pickle


def audio_reader(path):
    sample_rate, channel = wav.read(path)
    channel = channel/32768
    return channel, sample_rate


def load_config(path):
    try:
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        cfg = {}
        for line in lines:
            key, value = line.replace('\n', '').split('=')
            cfg[key] = value

        cfg['window_length'] = float(cfg['window_length'])
        cfg['window_step'] = float(cfg['window_step'])
        cfg['cepstrum_number'] = int(cfg['cepstrum_number'])
        cfg['filter_number'] = int(cfg['filter_number'])
        cfg['preemphasis_filter'] = float(cfg['preemphasis_filter'])
        cfg['delta_sample'] = int(cfg['delta_sample'])
        cfg['delta_delta_sample'] = int(cfg['delta_delta_sample'])
        if cfg['window_function'] == 'bartlett':
            cfg['window_function'] = np.bartlett
        elif cfg['window_function'] == 'blackman':
            cfg['window_function'] = np.blackman
        elif cfg['window_function'] == 'hanning':
            cfg['window_function'] = np.hanning
        elif cfg['window_function'] == 'kaiser':
            cfg['window_function'] = np.kaiser
        else:
            cfg['window_function'] = np.hamming

    except Exception as e:
        print('Error:', e, '// using default config')
        cfg = {
            'window_length': 0.025,
            'window_step': 0.01,
            'cepstrum_number': 13,
            'filter_number': 26,
            'preemphasis_filter': 0.97,
            'window_function': 'hamming',
            'delta_sample': 2,
            'delta_delta_sample': 2
        }

    return cfg


def computeMFCC(data, fs, cfg):
    fft_size = 2
    while fft_size < cfg['window_length'] * fs:
        fft_size *= 2

    data_mfcc = mfcc(data, samplerate=fs, nfft=fft_size, winlen=cfg['window_length'], winstep=cfg['window_step'],
                     numcep=cfg['cepstrum_number'], nfilt=cfg['filter_number'], preemph=cfg['preemphasis_filter'],
                     winfunc=cfg['window_function'])

    return data_mfcc


def getData(directory, file):
    path = directory + '/' + file
    samples, rate = audio_reader(path)
    file = file[:file.find('.')]
    return samples, rate, file, path


def restructure(data):
    """
    Changing data save format

    Returns data as a list of lists in following order:

    Sex:   Man,      Woman
    Digits:
    0:          data    data
    1:          data    data
    2:          data    data
    ...         ...     ...

    Access elements by restructured[Digit index][Speaker index]
    IMPORTANT: Both keys are string values!

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
            keys[number + 1].append(k)
        number += 1

    return createObj, keys


def compute_deltas(data, num):
    deltas = []
    for row in data:
        new_row = []
        for item in row:
            new_row.append(delta(item, num))
        deltas.append(new_row)

    return deltas


def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)


config = load_config('config/mfcc.cfg')

parameters = {}

file_directory = 'Speakers'
for filename in os.listdir(file_directory):
    if filename.endswith('.wav'):
        data_ = getData(file_directory, filename)
        getNum = data_[2][data_[2].find('0') + 1]
        getNam = data_[2][:data_[2].find('0')]
        helper = {}
        helper[getNum] = computeMFCC(data_[0], data_[1], config)
        if not getNam in parameters:
            parameters[getNam] = helper
        else:
            parameters[getNam].update(helper)

data_, keys = restructure(parameters)
save(data_, 'files/parametrized.p')
save(keys, 'files/parametrized_keys.p')

deltas_ = compute_deltas(data_, config['delta_sample'])
for i in range(len(data_)):
    for j in range(len(data_[i])):
        data_[i][j] = np.concatenate((data_[i][j], deltas_[i][j]), axis=1)
save(data_, 'files/parametrized_delta.p')

delta_deltas_ = compute_deltas(deltas_, config['delta_delta_sample'])
for i in range(len(data_)):
    for j in range(len(data_[i])):
        data_[i][j] = np.concatenate((data_[i][j], delta_deltas_[i][j]), axis=1)
save(data_, 'files/parametrized_delta_delta.p')
save(keys, 'files/parametrized_delta_delta_keys.p')

print(data_)
