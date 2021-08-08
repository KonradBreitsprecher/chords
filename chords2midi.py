from midiutil import MIDIFile

def write_midi_file(progression_semitones, filename):

    track    = 0
    channel  = 0
    time     = 0   # In beats
    duration = 1   # In beats
    tempo    = 60  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track automatically created)
    MyMIDI.addTempo(track, time, tempo)

    p_C1 = 24
    p_C2 = 36
    p_C3 = 48
    start_pitch = p_C3

    for chord_semitones in progression_semitones:

        for semitone in chord_semitones:
            pitch = start_pitch + semitone
            MyMIDI.addNote(track, channel, pitch, time, duration, volume)

        time = time + 1

    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)