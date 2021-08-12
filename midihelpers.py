import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from midiutil import MIDIFile

def play_midifile(filename):

    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

    # listen for interruptions
    try:
        # use the midi file you just saved
        clock = pygame.time.Clock()
        pygame.mixer.music.load(filename)

        pygame.mixer.music.play(loops=1)
        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished

    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


def write_midifile(progression_semitones, filename):

    track    = 0
    channel_lead  = 0
    channel_bass  = 1
    channel_drums = 9
    time     = 0   # In beats
    tempo    = 60  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track automatically created)
    MyMIDI.addTempo(track, time, tempo)

    MyMIDI.addProgramChange(track, channel_lead, 0, 0)      # Piano
    MyMIDI.addProgramChange(track, channel_bass, 0, 32)     # Acoustic Bass
    MyMIDI.addProgramChange(track, channel_drums, 0, 0)     # Drums Channel

    WITH_DRUMS = False
    pitch_bassdrum = 35
    pitch_snaredrum = 38
    pitch_hihat = 42
    duration_drums = 1

    p_C1 = 24
    p_C2 = 36
    p_C3 = 48
    start_pitch = p_C3

    duration_bass = 4
    durations_lead = [1] * (len(progression_semitones) - 1)
    durations_lead.append(4)

    for i, chord_semitones in enumerate(progression_semitones):

        # The chord
        for semitone in chord_semitones:
            pitch_lead = start_pitch + semitone
            MyMIDI.addNote(track, channel_lead, pitch_lead, time, durations_lead[i], volume)

        # Bass note
        pitch_bass = start_pitch - 12 + chord_semitones[0]
        MyMIDI.addNote(track, channel_bass, pitch_bass, time, duration_bass, volume)

        if WITH_DRUMS:
            if time % 2 == 0: 
                MyMIDI.addNote(track, channel_drums, pitch_bassdrum, time, duration_drums, volume)
            if time % 2 == 1: 
                MyMIDI.addNote(track, channel_drums, pitch_snaredrum, time, duration_drums, volume)
            for i in [1,2,3,4]:
                MyMIDI.addNote(track, channel_drums, pitch_hihat, time + (i-1)/4.0, duration_drums, volume)

        time = time + 1

    with open(filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)