#!/usr/bin/env python
# -*- coding: utf-8 -*-

# System imports
# ====================================================

import random
import sys
import difflib
import argparse

# Extention imports
# ====================================================

import printhelpers
import midihelpers
import chorddefinitions as d

# Command line arguments
# ====================================================

help_join_operator = ' | '
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', help="Key of the chord progression: " + help_join_operator.join(d.note_names_sharp) , default="C")
parser.add_argument('-s', '--scale', help="Scale of the chord progression: " + help_join_operator.join(list(d.scales.keys())), default="major")
parser.add_argument('-n', '--num-chords', help="Number of chords in the progression", default=4)
parser.add_argument('-f', '--first', help="Numerical starting chord of the progression", default=1)
parser.add_argument('-v','--voicing', help="Voicing to use: " +  help_join_operator.join(list(d.chord_types.keys())), default="random")
parser.add_argument('-m','--midifile', help="Specify output midifile", default="random_progression.mid")
parser.add_argument('-p','--play', action='store_true', help='Play the generated midifile via pygame')
parser.add_argument('-l','--large-hands', action='store_true', help='Suggest tabs using four bars instead of three. Warning: Only for large hands!')
parser.add_argument('-ph','--print-horizontal', action='store_true', help='Print the progression horizontally')

args = parser.parse_args()

def did_you_mean(keyword, choices) -> str:
    matches = difflib.get_close_matches(keyword, choices)
    if matches:
        return "Did you mean '" + matches[0] + "'?\n"

    return ""

def args_valid(args) -> bool:
    reason = ""
    valid = True

    if args.key not in d.note_names_sharp and args.key not in d.notes_names_flat:
        reason += "Unknown root note: " + args.key + "\n\n"
        valid = False

    if args.scale not in d.scales:
        reason += "Unknown scale: " + args.scale + "\n"
        reason += did_you_mean(args.scale, d.scales)
        reason += "Available scales:\n" +  help_join_operator.join(list(d.scales.keys())) + "\n\n"
        valid = False

    if args.voicing not in d.chord_types:
        reason += "Unknown voicing: " + args.voicing + "\n"
        reason += did_you_mean(args.voicing, d.chord_types)
        reason += "Available voicings:\n" +  help_join_operator.join(list(d.chord_types.keys())) + "\n\n"
        valid = False

    return valid, reason 

valid, reason = args_valid(args)
if not valid:
    print(reason)
    exit()

# Classes
# ====================================================

class Chord():

    def __init__(self, chord_numeral, scale, voicing):
        self.voicing = voicing
        self.semitones = []
        self.semitones_rising = []
        self.note_names = []

        self.root_note = note_names[(root_i+d.scales[scale][chord_numeral-1])%12]

        last_semitone = -1
        for semitones_in_scale in d.chord_types[voicing]:
            semitone = (root_i + scale_semitones[(chord_numeral - 1 + semitones_in_scale) % 7]) % 12
            self.semitones.append(semitone)
            self.note_names.append(note_names[semitone])
            
            semitone_rising = semitone
            while semitone_rising < last_semitone:
                semitone_rising += 12
            last_semitone = semitone_rising
            self.semitones_rising.append(semitone_rising)

    
class Progression():
    def __init__(self, chords):
        self.chords = chords
        self.chords_rising_semitones = [chord.semitones_rising for chord in chords]

# Functions
# ====================================================

def check_flat():
    # returns True, if the default scale with sharps has doubled note names like G and G#
    # this will only work for true diatonic scales as long as no double flats an sharps become involved
    # F# major and Gb major will break the system
    for i in range(len(scale_semitones)):
        for j in range(i+1, len(scale_semitones)):
            # print "i, j, notes ", i, j, notes[(root_i + scale_notes[i])%12][0], notes[(root_i + scale_notes[j])%12][0]
            if d.note_names_sharp[(root_i + scale_semitones[i])%12][0]==d.note_names_sharp[(root_i + scale_semitones[j])%12][0]:
                return True

    return False

def chooce_voicing():
    if args.voicing == "random":
        return random.choice(list(d.chord_types.keys())[:-1])
    else:
        return args.voicing


def create_random_transitions(scale, length, starting_chord):
    transitions_numeral = []
    transitions_numeral.append(starting_chord) 
    act_chord = starting_chord
    for i in range(length-1):
        new_chord_numeral = random.choice(d.chord_transitions[scale][act_chord])
        transitions_numeral.append(new_chord_numeral)
        act_chord = new_chord_numeral
    return transitions_numeral

def create_progression(scale, length, starting_chord):

    # Generate random transitions
    transitions_numeral = create_random_transitions(scale, length, starting_chord)

    # Put the transitions in scale, choose voicing and create the progression
    progression = [Chord(chord_numeral, scale, chooce_voicing()) for chord_numeral in transitions_numeral]

    return progression

# Init
# ====================================================

# Get root note index
if args.key in d.notes_names_flat:
    root_i = d.notes_names_flat.index(args.key)
else:
    root_i = d.note_names_sharp.index(args.key)

# Get scale notes
scale_semitones = d.scales[args.scale]

#Switch note table if flat
use_flat = check_flat()
if use_flat:
    note_names = d.notes_names_flat
else:
    note_names = d.note_names_sharp

# Generation
# ====================================================

progression = Progression(create_progression(args.scale, args.num_chords, args.first))

# Print
# ====================================================

printhelpers.print_progression(progression, args.scale, args.large_hands, args.print_horizontal)

# Midi
# ====================================================

if args.midifile != "":
    midihelpers.write_midifile(progression.chords_rising_semitones, args.midifile)
    if args.play:
        midihelpers.play_midifile(args.midifile)
    
