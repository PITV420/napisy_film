from pydub import AudioSegment
import os


def make_list(file_directory):
    """ Making list of names of wave files. """

    list_ = []
    for fileName in os.listdir(file_directory):
        if fileName.endswith('.wav'):
            list_.append(fileName)
    return list_


speaker_list = make_list('files/Speakers')
noise_list = make_list('files/Noises')


def mix_waves(speakers, noises, snr):
    """ Mixing speaker and noise waves. """

    for i in range(len(speakers)):
        for j in range(len(noises)):

            speaker_wave = AudioSegment.from_file("files/Speakers/"+speakers[i])
            noise_wave = AudioSegment.from_file("files/Noises/"+noises[j])

            if snr == 1:
                """ Signal-to-noise ratio: 1/1 (Speaker and noise are equally loud). """
                mixed = speaker_wave.overlay(noise_wave)

                speaker_str = speakers[i].replace(".wav", "")
                noise_str = noises[j].replace(".wav", "")

                """ Saving mixed waves in appropriate folder """
                mixed.export("files/Mixed_snr_1_1/" + speaker_str + '_' + noise_str + ".wav", format='wav')

            elif snr == 2:
                """ Signal-to-noise ratio: 1/2 (Speaker is 2 times (6dB) louder than noise) """
                noise_wave = noise_wave - 6

                mixed = speaker_wave.overlay(noise_wave)

                speaker_str = speakers[i].replace(".wav", "")
                noise_str = noises[j].replace(".wav", "")

                """ Saving mixed waves in appropriate folder """
                mixed.export("files/Mixed_snr_1_2/" + speaker_str + '_' + noise_str + ".wav", format='wav')

            elif snr == 4:
                """ Signal-to-noise ratio: 1/4 (Speaker is 4 times (12dB) louder than noise) """
                noise_wave = noise_wave - 12

                mixed = speaker_wave.overlay(noise_wave)

                speaker_str = speakers[i].replace(".wav", "")
                noise_str = noises[j].replace(".wav", "")

                """ Saving mixed waves in appropriate folder """
                mixed.export("files/Mixed_snr_1_4/" + speaker_str + '_' + noise_str + ".wav", format='wav')

            elif snr == 8:
                """ Signal-to-noise ratio: 1/8 (Speaker is 8 times (18dB) louder than noise) """
                noise_wave = noise_wave - 18

                mixed = speaker_wave.overlay(noise_wave)

                speaker_str = speakers[i].replace(".wav", "")
                noise_str = noises[j].replace(".wav", "")

                """ Saving mixed waves in appropriate folder """
                mixed.export("files/Mixed_snr_1_8/" + speaker_str + '_' + noise_str + ".wav", format='wav')

            else:
                print("Unhandled case.")


mix_waves(speaker_list, noise_list, 1)
mix_waves(speaker_list, noise_list, 2)
mix_waves(speaker_list, noise_list, 4)
mix_waves(speaker_list, noise_list, 8)