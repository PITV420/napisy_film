import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
import os
import pickle


directory = 'files/Speakers'


def make_list(file_directory):
    """ Making list of names of wave files. """

    list_ = []
    for fileName in os.listdir(file_directory):
        if fileName.endswith('.wav'):
            list_.append(fileName)
    return list_



speaker_list = make_list(directory)


def audio_reader(path):
    """ Reading data and sample rate from wav file. """

    sample_rate, data = wav.read(path)
    data = data/32768
    return sample_rate, data


def framing(sound, rate, t_length, t_step):
    """ Function, which energetically calculates mean of samples in given length of the frame
     and decides where is a speech in the given sound. """

    sound = 10 * (np.log10((np.sqrt(sound ** 2))))
    tab = []

    s_length = len(sound) / ((len(sound) / rate) * (1 / (t_length / 1000)))
    s_step = len(sound) / ((len(sound) / rate) * (1 / (t_step / 1000)))
    s_length = int(s_length)
    s_step = int(s_step)

    ctr = -s_step

    for i in range(int(len(sound) / s_step) - 1):

        ctr += s_step
        s_sum = 0

        for j in range(ctr, ctr + s_length):
            s_sum += 10**(0.1 * sound[j])

        mean = 10*np.log10(s_sum / s_length)

        if mean > -15:
            """ 1 - if in this part there is a speech. """

            for k in range(s_step):
                tab.append(1)

        else:
            """ 0 - if in this part there is no speech. """

            for k in range(s_step):
                tab.append(0)

    for j in range(s_step):
        tab.append(0)

    return tab


def whole_framing(speakers, t_length, t_step):
    """ Uses the 'framing' function to create list of values (0 or 1) for each speaker. """

    tab_result = []

    for i in range(len(speakers)):

        rate, sound = audio_reader(directory + "/" + speakers[i])

        tab = framing(sound, rate, t_length, t_step)
        tab_result.append(tab)

    return tab_result


speakers_tab = whole_framing(speaker_list, 400, 200)



def plotting(sounds, results):
    """ Plotting sound wave and result of framing function of each sound to compare. """

    for i in range(len(sounds)):

        rate, sound = audio_reader(directory + "/" + sounds[i])

        plt.figure(i+1)
        plt.subplot(211)
        plt.plot(sound)
        plt.title(speaker_list[i])
        plt.subplot(212)
        plt.plot(results[i])


plotting(speaker_list, speakers_tab)

plt.show()