import json
import random
import winsound
from randomwordgenerator import randomwordgenerator
from mido import Message, MidiFile, MidiTrack
from tqdm import tqdm


# fun data to fill
min_time            = 180   # in seconds
max_time            = 300   # in seconds
min_tracks          = 1     # between 1 and 16
max_tracks          = 16    # between 1 and 16

data = {}


def __main__():
    # 0: single track, only one track
    # 1: synchronous, start at the same time
    # 2: asynchronous, independent tracks (breaks .length)
    file = MidiFile(type=1)

    # generate tracks
    track_length = random.randint(min_time, max_time)

    for i in tqdm(range(random.randint(min_tracks, max_tracks))):
        track = MidiTrack()
        file.tracks.append(track)

        load_file(i)

        track.append(Message('program_change', program=random.randint(0, 127), time=0))

        previous_note = None
        #for j in tqdm(range(1000)):
        while file.length < track_length:
            note = generate_weighted(previous_note)
            track.append(note)
            track.append(Message('note_off', note=64, velocity=127, time=0))
            previous_note = note

    name = randomwordgenerator.generate_random_words(random.randint(1, 3))
    if type(name) is list:
        name = ' '.join(name)
    file.save('created_music/' + name + '.mid')

    winsound.PlaySound('sounds/oh no.wav', winsound.SND_ALIAS)


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
    else:
        note_list = []
        for key, item in data[str(previous_note.note)]['next'].items():
            note_list += [key] * item['count']
        note_value = int(random.choice(note_list))

    time_list = []
    for key, item in data[str(note_value)]['time'].items():
        time_list += [key] * item['count']
    time_value = int(random.choice(time_list)) * 2

    return Message('note_on', note=note_value, velocity=velocity_value, time=time_value)


if __name__ == __main__():
    __main__()
