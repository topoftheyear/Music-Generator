import json
import random
import winsound
from randomwordgenerator import randomwordgenerator
from mido import Message, MidiFile, MidiTrack
from tqdm import tqdm


data = {}


def __main__():
    # 0: single track, only one track
    # 1: synchronous, start at the same time
    # 2: asynchronous, independent tracks (breaks .length)
    file = MidiFile(type=1)

    # generate tracks
    track_length = random.randint(10, 10)

    for i in tqdm(range(random.randint(1, 1))):
        track = MidiTrack()
        file.tracks.append(track)

        load_file(i)

        track.append(Message('program_change', program=12, time=0))
        while file.length < track_length:
            note = generate_weighted()
            track.append(note)
            #track.append(Message('note_off', note=64, velocity=127, time=1))

    name = randomwordgenerator.generate_random_words(random.randint(1, 3))
    if type(name) is list:
        name = ' '.join(name)
    file.save('created_music/' + name + '.mid')


def load_file(number):
    global data
    with open('data/data' + str(number) + '.json') as f:
        data = json.load(f)


def generate_weighted(previous_note=None):
    note_value = 0
    velocity_value = 64
    time_value = 32

    if previous_note is None:
        note_list = []
        for key, item in data.items():
            note_list += [key] * item['count']
        note_value = int(random.choice(note_list))

        time_list = []
        for key, item in data[str(note_value)]['time'].items():
            time_list += [key] * item['count']
        time_value = int(random.choice(time_list))



    return Message('note_on', note=note_value, velocity=velocity_value, time=time_value)


if __name__ == __main__():
    __main__()
