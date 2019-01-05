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

        0: [[MFCC_Speaker_1_digit_0]
            [MFCC_Speaker_2_digit_0]
            .
            .
            .
            [MFCC_Speaker_22_digit_0]]
        .
        .
        .
        9: [[MFCC_Speaker_1_digit_9]
            [MFCC_Speaker_2_digit_9]
            .
            .
            .
            [MFCC_Speaker_22_digit_9]]

        Returns GMM for matrix for each digit separately.
    """

    data_gmm = {}
    data_mfcc = {}
    for key1 in data:
        for key2 in data[key1]:
            if key2 == list(data[key1].keys())[0]:
                data_mfcc = data[key1][key2]
            elif key2 > list(data[key1].keys())[0]:
                data_mfcc = np.concatenate((data_mfcc, data[key1][key2]), axis=0)
        data_gmm[key1] = compute_gmm(data_mfcc, cfg)

    return data_gmm
"""
def reconstruct(filenameData):
    """ """
    Reconstructing data & attaching keys to samples
    for example:
    woman00: array([samples]), ...
    Access elements using keys
    """ """
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
"""

def save(obj):
    file = open('files/digits_gmm.p', 'wb')
    pickle.dump(obj, file)


parametrized_data = load_data('files/parametrized.p')
config = load_config('config/gmm.cfg')

data = eachDigitGMM(parametrized_data, config)

save(data)
