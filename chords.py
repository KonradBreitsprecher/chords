#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

RANDOM_VOICING=True
# To indicate which notes to use
# Defaults to sharps
FLAT=False
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
notes_flat=['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

scales = {
        'major' :           [0, 2, 4, 5, 7, 9, 11],
        'natural_minor':    [0, 2, 3, 5, 7, 8, 10],
        'harmonic_minor':   [0, 2, 3, 5, 7, 8, 11],
        'melodic_minor':    [0, 2, 3, 5, 7, 9, 11],
        'dorian':           [0, 2, 3, 5, 7, 9, 10],
        'locrian':          [0, 1, 3, 5, 6, 8, 10],
        'lydian':           [0, 2, 4, 6, 7, 9, 11],
        'mixolydian':       [0, 2, 4, 5, 7, 9, 10],
        'phrygian':         [0, 1, 3, 5, 7, 8, 10]
#        'major_pentatonic': ['2', '4', '7', '9', '12'],
#        'minor_pentatonic': ['3', '5', '7', '10', '12']
}

root = sys.argv[1] #note string
root_i = notes.index(root)

scale = sys.argv[2] #string
scale_notes = scales[scale]

progression_length = int(sys.argv[3])

if len(sys.argv) > 4:
    starting_chord = int(sys.argv[4])
else:
    starting_chord = 1

#Respect enharmonic shit
#notes_corrected = []
#notes_corrected.append(notes[root_i])
#for n in range(6):
#    step = scale_notes[n+1]-scale_notes[n]
#    note = notes[(root_i+scale_notes[n])%12]
#    note_next = notes[(root_i+scale_notes[n+1])%12]
#    if note[0] == note_next[0]: #if first character of consecutive note names are equal, use flat next
#        notes_corrected.append(notes[(root_i+scale_notes[n+2])%12] + 'b')
#    else:
#        notes_corrected.append(note_next)
    
    
transitions = {
        'major' :           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} , 
        'natural_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'harmonic_minor':   { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'melodic_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'dorian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'locrian':          { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'lydian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'mixolydian':       { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'phrygian':         { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} 
#       'major_pentatonic': { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} },
#       'minor_pentatonic': { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} }
}

# in terms of scale degrees
# note in this formulation the chords are build from the given scale
# every chord can be major or minor, depending on context
# this structure will always lead to chord that are in scale
chord_types = {
        'triad'             : [0, 2, 4],            #root third fifth
        'first_inv'         : [2, 4, 7],            #third fifth, root
        'sec_inv'           : [4, 7, 2],            #fifth root third
        'seventh'           : [0, 2, 4, 6],         #triad + sevents 
        'first_inv_seventh' : [2, 4, 6, 7],
        'sec_inv_seventh'   : [4, 6, 7, 2],
        'third_inv_seventh' : [6, 7, 2, 4],
        'sus2'              : [0, 1, 4],            #root second fifth
        'sus4'              : [0, 3, 4],
        'add9'              : [0, 2, 4, 6, 8],      #includes the seven
        'add11'             : [0, 2, 4, 6, 8, 10]   #includes seven and nine
    }

# therefore having the chords in terms of half steps makes sense to me
# those can be built indendent of context, having a dominant seventh whenever we want

chords_semitones = {
        'maj_triad'     : [0, 4, 7], 
        'min_triad'     : [0, 3, 7], 
        'imaj_triad'    : [4, 7, 12],
        'iimaj_triad'   : [7, 12, 16], 
        'imin_triad'    : [3, 7, 12], 
        'iimin_triad'   : [7, 12, 15], 
        'maj_seventh'   : [0, 4, 7, 11],
        'min_seventh'   : [0, 3, 7, 10],
        'dom_seventh'   : [0, 4, 7, 10],
        'dim'           : [0, 3, 6], 
        'dim_seventh'   : [0, 3, 6, 9], # fully diminished "seventh" triad, seventh is equivalent with maj 6!
        'half_dim'      : [0, 3, 6, 10],
        'sus2'          : [0, 2, 7],
        'susb2'         : [0, 1, 7], 
        'sus4'          : [0, 5, 7],
        'sus#4'         : [0, 6, 7], 
        'maj_add9'      : [0, 4, 7, 11, 14], 
        'min_add9'      : [0, 3, 7, 10, 14], 
        'maj_addb9'     : [0, 4, 7, 11, 13],
        'min_addb9'     : [0, 3, 7, 10, 13], 
        'maj_add11'     : [0, 4, 7, 11, 14, 17],
        'min_add11'     : [0, 3, 7, 10, 14, 17]
    }

def check_flat():
    # returns True, if the default scale with sharps has doubled note names like G and G#
    # this will only work for true diatonic scales as long as no double flats an sharps become involved
    # F# major and Gb major will break the system
    global scale_notes, notes, root_i 
    for i in range(len(scale_notes)):
        for j in range(i+1, len(scale_notes)):
            # print "i, j, notes ", i, j, notes[(root_i + scale_notes[i])%12][0], notes[(root_i + scale_notes[j])%12][0]
            if notes[(root_i + scale_notes[i])%12][0]==notes[(root_i + scale_notes[j])%12][0]:
                return True

    return False
    

def corrected_scale():
    global scale_notes, notes, scale, root_i, notes_flat, FLAT
    correct_scale = []
    for i in scale_notes:
        if FLAT:
            correct_scale.append(notes_flat[(root_i + i)%12])
        else:
            correct_scale.append(notes[(root_i + i)%12])
    return correct_scale



def seminote_to_string(seminote):
    global scale_notes, notes
    last_note = notes[seminote]
    for n in scale_notes[1:]:
        if notes[n][0] == last_note: #if consecutive note names are equal, somethings wrong
            pass

def numeral_to_chord(n):
    global root_i, scale_notes, chords_types, RANDOM_VOICING, notes
    if RANDOM_VOICING:
        voice_name, chord_notes = random.choice(chord_types.items())
        
        chord_semitones = []
        chord_note_names = []
        
        #cleaned this up a bit
        for i in chord_notes:
            s = (root_i+scale_notes[(n - 1 + i)%7])%12
            chord_semitones.append(s)
            chord_note_names.append(notes[s])
            
        return chord_note_names, voice_name, chord_semitones
    else:
        return notes[(root_i+scale_notes[n-1])%12] + '-' + notes[(root_i+scale_notes[(n+1)%7])%12] + '-' + notes[(root_i+scale_notes[(n+3)%7])%12]

def create_progression(length,starting_chord):
    global scale
    progression = []
    progression.append(starting_chord) 
    act_chord = starting_chord
    for i in range(length-1):
        new_chord = random.choice(transitions[scale][act_chord])
        progression.append(new_chord)
        act_chord=new_chord
    return progression


def print_chord(chord_semitones):
    s = ""
    st = 0
    ri = 0
    colind = []
    close_col = False
    for i in range(14*2+1):
        if (i%14) not in [0,6]:
            if ri < len(chord_semitones) and st%12==chord_semitones[ri]:
                s += bcolors.OKGREEN
                close_col = True
                colind.append(i)
                ri += 1
            st += 1
        s += '░' if (i%14) in [1,3,5,7,9,11,13] else '█' if (i%14) in [2,4,8,10,12] else '║'
        if close_col:
            close_col = False
            s += bcolors.ENDC

    s = (s+'\n')*2 
    close_col = False
    for i in range(14*2+1):
        if (i%14) in [1,3,5,7,9,11,13] and i in colind: # and ri < len(chord_semitones) and (st%12)==chord_semitones[ri]:
                s += bcolors.OKGREEN
                close_col = True
        s += '░' if (i%14) in [1,3,5,7,9,11,13] else '║'
        if close_col:
            close_col = False
            s += bcolors.ENDC

    s += "\n"+("╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝")

    print s



#print "check_flat ", check_flat()
FLAT=check_flat()

#Switch note table if FLAT
if FLAT:
    notes = notes_flat

#print corrected_scale()

progression = create_progression(progression_length, starting_chord)

for c in progression:
    chord_note_names, voicing, chord_semitones = numeral_to_chord(c)
    chord_root_note = notes[scales[scale][c-1]]
    
    print ""
    print "-".join(chord_note_names) + " (" + chord_root_note + " " + scale + " " + voicing + ")  "
    print_chord(chord_semitones)
    print ""


