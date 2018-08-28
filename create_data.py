import mido
from tqdm import tqdm
import os


def __main__():
    with open('Data/data.txt', 'w+') as outfile:
        for file in tqdm(os.listdir('music')):
            port = mido.open_output()
            mid = mido.MidiFile('music/' + file)
            for i, track in enumerate(mid.tracks):
                for x in range(16):
                    for msg in track:
                        if msg is None:
                            continue

                        outfile.write(str(msg.bytes()) + '\n')

            port.close()


if __name__ == '__main__':
    __main__()