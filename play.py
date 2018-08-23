import mido


def __main__():
    port = mido.open_output()
    while True:
        notes = input()
        if notes == '':
            break;
        msg = mido.Message('note_on', note=int(notes))
        port.send(msg)
        

if __name__ == "__main__":
    __main__()
