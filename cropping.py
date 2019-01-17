from pydub import AudioSegment
import random
import os



def make_list(file_directory):
    """ Making list of names of wave files. """

    list_ = []
    for fileName in os.listdir(file_directory):
        if fileName.endswith('.wav'):
            list_.append(fileName)
    return list_


def cut_waves(sound_list, time, name):
    """ Cuts the wave to the specified length from random moment. """

    for i in range(len(sound_list)):

        sound = AudioSegment.from_file("files/" +name+ "/" + sound_list[i])

        if time == 3:
            """ When we want it to last 3 seconds. """

            t1 = random.randint(0, 13000)
            t2 = t1 + 3000
            cropped = sound[t1:t2]

            """ Saving cropped waves in appropriate folder """
            cropped.export("files/"+name+"_3s/" + sound_list[i], format='wav')

        elif time == 6:
            """ When we want it to last 6 seconds. """

            t1 = random.randint(0, 10000)
            t2 = t1 + 6000
            cropped = sound[t1:t2]

            """ Saving cropped waves in appropriate folder """
            cropped.export("files/"+name+"_6s/" + sound_list[i], format='wav')

        elif time == 10:
            """ When we want it to last 10 seconds. """

            t1 = random.randint(0, 6000)
            t2 = t1 + 10000
            cropped = sound[t1:t2]

            """ Saving cropped waves in appropriate folder """
            cropped.export("files/"+name+"_10s/" + sound_list[i], format='wav')

        else:
            print("Unhandled case.")

for i in range(2):
    if i == 1:
        name = 'Noises'
    else:
        name = 'Speakers'

    noise_list = make_list('files/' + name)
    cut_waves(noise_list, 3, name)
    cut_waves(noise_list, 6, name)
    cut_waves(noise_list, 10, name)