import mido
import json
from tqdm import tqdm   
import os


def __main__():
    channel = [{},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {},
               {}]
    print(channel)
    for file in tqdm(os.listdir('music')):
        port = mido.open_output()
        mid = mido.MidiFile('music/' + file)
        current_note = None
        next_note = None
        for i, track in enumerate(mid.tracks):
            for x in range(16):    
                for msg in track:
                    if msg is None or msg.type != 'note_on' or msg.velocity == 0:
                        continue
                    if current_note is None:
                        current_note = msg
                        continue
                    if msg is not None:
                        next_note = msg

                    if current_note.note not in channel[x]:
                        channel[x][current_note.note] = {'count': 0, 'time': {}, 'next': {}}
                    channel[x][current_note.note]['count'] += 1
                    
                    if current_note.time not in channel[x][current_note.note]['time']:
                        channel[x][current_note.note]['time'][current_note.time] = {'count': 0}
                    channel[x][current_note.note]['time'][current_note.time]['count'] += 1
                        
                    if next_note.note not in channel[x][current_note.note]['next']:
                        channel[x][current_note.note]['next'][next_note.note] = {'count': 0}
                    channel[x][current_note.note]['next'][next_note.note]['count'] += 1
                    
                    current_note = next_note
                    
        port.close()
        
    to_file(channel)
    print_channels(channel)

    
def to_file(channel):
    for x in range(len(channel)):
        with open('Data/data' + str(x) + '.json', 'w+') as outfile:
            json.dump(channel[x], outfile)
            outfile.close()
            
            
def print_channels(channel):
    for x in range(len(channel)):
        print('CHANNEL ' + str(x))

        for key, item in channel[x].items():
            print(str(key) + ' | ' + str(item))
    
    
if __name__ == '__main__':
    __main__()