"""
Parametrize vocal samples from training set
"""


from python_speech_features import mfcc, delta
import scipy.io.wavfile as wav
import numpy as np
import os
import pickle


def audio_reader(path):
    sampleRate, channel = wav.read(path)
    channel = channel/32768
    return channel, sampleRate


def loadConfig(path):

    try:
        with open(path, 'r') as file:
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
            cfg['use_delta'] = bool(cfg['use_delta'])
            cfg['delta_sample'] = int(cfg['delta_sample'])
            cfg['use_delta_delta'] = bool(cfg['use_delta_delta'])
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
            'use_delta': True,
            'delta_delta_sample': 2,
            'use_delta_delta': True
        }

    return cfg


def computeMFCC(data, fs, cfg):
    """
    :param data: audio file as an array of samples
    :param fs: sample rate of the audio file
    :param cfg: config file for parametrization
    :return: mfcc matrix
    """

    fft_size = 2
    while fft_size < cfg['window_length'] * fs:
        fft_size *= 2

    data_mfcc = mfcc(data, samplerate=fs, nfft=fft_size, winlen=cfg['window_length'], winstep=cfg['window_step'],
                     numcep=cfg['cepstrum_number'], nfilt=cfg['filter_number'], preemph=cfg['preemphasis_filter'],
                     winfunc=cfg['window_function'])

    if cfg['use_delta'] or cfg['use_delta_delta']:
        data_mfcc = np.concatenate((data_mfcc, delta(data_mfcc, cfg['delta_sample'])), axis=1)

    if cfg['use_delta_delta']:
        data_mfcc = np.concatenate(((data_mfcc, delta(data_mfcc, cfg['delta_delta_sample']))), axis=1)

    return data_mfcc


def getData(directory, file):
    path = directory + '/' + file
    samples, rate = audio_reader(path)
    return samples, rate, file[6] + '_' + file[:5], path


def restructure(data):
    """
    Changing data save format

    Returns data as a list of lists in following order:

    Speakers:   0,      1,      2,      ...
    Digits:
    0:          data    data    data    ...
    1:          data    data    data    ...
    2:          data    data    data    ...
    ...         ...     ...     ...     ...

    Access elements by restructured[Digit index][Speaker index]
    """
    restructured = []
    for i in range(10):
        restructured.append([])

    for key in data:
        restructured[int(key[0])].append(data[key])

    print(restructured)
    return restructured


def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)


def main():
    """
    Parametrize train set using mfcc algorithm

    :save: data to parametrized.p
    """

    config = loadConfig('config/mfcc.cfg')

    parameters = {}

    file_directory = 'train'
    for filename in os.listdir(file_directory):
        if filename.endswith('.wav'):
            data_ = getData(file_directory, filename)
            parameters[data_[2]] = computeMFCC(data_[0], data_[1], config)

    data_ = restructure(parameters)
    save(data_, 'files/parametrized.p')

main()