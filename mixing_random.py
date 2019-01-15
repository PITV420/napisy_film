from pydub import AudioSegment
import os
import random


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

    for i in range(len(noises)):
        for j in range(len(speakers)):

            silence_wav = random_silence(7000)
            speaker_wav = AudioSegment.from_wav(s_direct + "/" + speakers[j])
            silence_speaker_wav = concatenate_waves(silence_wav, speaker_wav)

            noise_wav = AudioSegment.from_wav(n_direct + "/" + noises[i])

            mixed = mix_waves(silence_speaker_wav, noise_wav, snr)

            speaker_str = speakers[j].replace(".wav", "")
            noise_str = noises[i].replace(".wav", "")

            if snr == 1:
                mixed.export(mix_direct + "0dB/" + speaker_str + '_' + noise_str + ".wav", format='wav')
            elif snr == 2:
                mixed.export(mix_direct + "6dB/" + speaker_str + '_' + noise_str + ".wav", format='wav')
            elif snr == 4:
                mixed.export(mix_direct + "12dB/" + speaker_str + '_' + noise_str + ".wav", format='wav')
            elif snr == 8:
                mixed.export(mix_direct + "18dB/" + speaker_str + '_' + noise_str + ".wav", format='wav')
            else:
                print("Unhandled case.")


def main():
    """ Main function. """

    s_directory = 'files/Speakers_3s'
    n_directory = 'files/Noises_10s'
    mix_directory = 'files/Mix_S_3s_N_10s/SNR_'

    speaker_list = make_list(s_directory)
    noise_list = make_list(n_directory)

    snr_tab = [1, 2, 4, 8]

    for elem in snr_tab:
        save_mixed_waves(speaker_list, noise_list, elem, s_directory, n_directory, mix_directory)


main()

