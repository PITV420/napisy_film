from pydub import AudioSegment
import os
import random
import pickle
import numpy as np
import scipy.io.wavfile as wav

def audio_reader(path):
    sampleRate, channel = wav.read(path)
    channel = channel/32768
    return channel, sampleRate

def make_list(file_directory):
    """ Making list of names of wave files. """

    list_ = []
    for fileName in os.listdir(file_directory):
        if fileName.endswith('.wav'):
            list_.append(fileName)
    return list_


def random_silence(max_dur):
    """ Creates an audio file of silence of random length (no longer than given max duration)."""

    duration = random.randint(0, max_dur - 1)
    silence = AudioSegment.silent(duration=duration)
    return silence


def concatenate_waves(first_wav, second_wav):
    """ Returns connected waves into one wave. """

    connected = first_wav + second_wav
    return connected


def mix_waves(speaker_wav, noise_wav, snr):
    """ Returns two waves mixed into one with given SNR. """

    if snr == 1:
        pass
    elif snr == 2:
        noise_wav = noise_wav - 6
    elif snr == 4:
        noise_wav = noise_wav - 12
    elif snr == 8:
        noise_wav = noise_wav - 18
    else:
        print("Unhandled case.")
        return

    mixed = noise_wav.overlay(speaker_wav)
    return mixed


def save_mixed_waves(speakers, noises, snr, s_direct, n_direct, mix_direct):
    """ Uses previous functions to create mixed wave files and saves them in appropriate folder. """

    markers = {}
    for noiseName in noises:
        for speakerName in speakers:

            silence_wav = random_silence(7000)
            speaker_wav = AudioSegment.from_wav(s_direct + "/" + speakerName)

            silence_speaker_wav = concatenate_waves(silence_wav, speaker_wav)

            noise_wav = AudioSegment.from_wav(n_direct + "/" + noiseName)

            mixed = mix_waves(silence_speaker_wav, noise_wav, snr)

            speaker_str = speakerName.replace(".wav", "")
            noise_str = noiseName.replace(".wav", "")

            if snr == 1:
                SNR = "0dB"

            elif snr == 2:
                SNR = "6dB"
            elif snr == 4:
                SNR = "12dB"
            elif snr == 8:
                SNR = "18dB"
            else:
                print("Unhandled case.")

            frame1 = np.concatenate((np.zeros(len(silence_wav)*16), np.ones(len(speaker_wav)*16)), axis=0)

            if len(frame1) < len(noise_wav)*16:
                zeros2 = np.zeros((len(noise_wav)*16-len(frame1)))
                frame = np.concatenate((frame1, zeros2), axis=0)
            else:
                frame = frame1

            if not speaker_str + '_' + noise_str in markers:
                markers[speaker_str + '_' + noise_str] = frame
            else:
                markers[speaker_str + '_' + noise_str].update(frame)

            mixed.export(mix_direct + SNR + "/" + speaker_str + '_' + noise_str + ".wav", format='wav')

    return markers

def save(obj, name):
    file = open(name, 'wb')
    pickle.dump(obj, file)

def main():
    """ Main function. """

    s_directory = 'files/Speakers_3s'
    n_directory = 'files/Noises_10s'
    mix_directory = 'files/Mix_S_3s_N_10s/SNR_'

    speaker_list = make_list(s_directory)
    noise_list = make_list(n_directory)

    snr_tab = [1, 2, 4, 8]

    markers = {}

    for elem in snr_tab:
        mark = save_mixed_waves(speaker_list, noise_list, elem, s_directory, n_directory, mix_directory)
        if not str(elem) in markers:
            markers[str(elem)] = mark
        else:
            markers[str(elem)].update(mark)
    save(markers, 'files/Mix_S_3s_N_10s/orginal_framings.p')

main()