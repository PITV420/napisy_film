from sklearn.mixture import GaussianMixture
import numpy as np
import pickle


def load_data(path):
    file = open(path, 'rb')
    return pickle.load(file)


def load_config(path):
    try:
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        cfg = {}
        for line in lines:
            key, value = line.replace('\n', '').split('=')
            cfg[key] = value

        cfg['components'] = int(cfg['components'])
        cfg['max_iterations'] = int(cfg['max_iterations'])
        cfg['toleration'] = float(cfg['toleration'])
        if not cfg['covariance_type'] == 'diag' or\
           not cfg['covariance_type'] == 'full' or\
           not cfg['covariance_type'] == 'tied' or\
           not cfg['covariance_type'] == 'spherical':
            cfg['covariance_type'] = 'diag'

    except Exception as e:
        print('Error:', e, '// using default config')
        cfg = {
            'components': 8,
            'max_iterations': 30,
            'toleration': 0.001,
            'covariance_type': 'diag',
        }

    return cfg


def compute_gmm(data, cfg):
    return GaussianMixture(n_components=cfg['components'], covariance_type=cfg['covariance_type'],
                               max_iter=cfg['max_iterations'], tol=cfg['toleration']).fit(data)


def eachDigitGMM(data, cfg):

    """
    Creates a dictionary consisting of connected matrices of MFCC for every speaker,
    into one matrix for particular digit:
        man: [[MFCC_man_digit_0]
              [MFCC_man_digit_1]
              .
              .
              .
              [MFCC_man_digit_n]]
        woman: [[MFCC_woman_digit_0]
                [MFCC_woman_digit_1]
                .
                .
                .
                [MFCC_woman_digit_n]]
        Returns GMM for matrix for gender separately.
    """

    data_gmm = {}
    data_mfcc = {}
    data_mfcc2 = {}
    licznik = 0
    for key1 in data:
        for key2 in data[key1]:
            if licznik == 0:
                data_mfcc2 = data[key1][key2]
                licznik = 2
            else:
                data_mfcc2 = np.concatenate((data_mfcc2, data[key1][key2]), axis=0)
            if key2 == list(data[key1].keys())[0]:
                data_mfcc = data[key1][key2]
            elif key2 > list(data[key1].keys())[0]:
                data_mfcc = np.concatenate((data_mfcc, data[key1][key2]), axis=0)

        data_gmm[key1] = compute_gmm(data_mfcc, cfg)
    data_gmm2 = compute_gmm(data_mfcc2, cfg)

    return data_gmm, data_gmm2

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

def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)

def main():
    config = load_config('files/config/gmm.cfg')
    toLoop = [-1, 0, 1, 2, 4, 8]
    for k in toLoop:
        if k == -1:
            name = 'Speakers'
        elif k == 0:
            name = 'Noises'
        else:
            name = 'Mixed_snr_1_' + str(k)
        parametrized_data = reconstruct('files/parametrization/parametrized_' + name)
        data1, data2 = eachDigitGMM(parametrized_data, config)
        if k == 0:
            save(data1, 'files/gmm/genders_gmm.p')
        save(data2, 'files/gmm/'+ name + '_gmm.p')