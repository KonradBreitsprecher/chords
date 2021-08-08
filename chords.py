#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import chords2midi

# Args and defaults

if len(sys.argv) > 1:
    root = sys.argv[1]
else:
    root = 'C'

if len(sys.argv) > 2:
    scale = sys.argv[2]
else:
    scale = 'natural_minor'

if len(sys.argv) > 3:
    progression_length = int(sys.argv[3])
else:
    progression_length = 3

if len(sys.argv) > 4:
    starting_chord = int(sys.argv[4])
else:
    starting_chord = 1


RANDOM_VOICING=True

# Definitions

notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
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
    
transitions = {
        'major' :           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} , 
        'natural_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'harmonic_minor':   { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'melodic_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'dorian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'locrian':          { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'lydian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'mixolydian':       { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} ,
        'phrygian':         { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,5,6,7], 4: [1,2,5,7], 5: [1,4,6,7], 6: [2,4,5], 7: [1,5,6]} 
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
        'add9'              : [0, 2, 4, 8],         #only nine
        'add11'             : [0, 2, 4, 10],        #only eleventh
        'ninth'             : [0, 2, 4, 6, 8],      #includes the seven and nine
        'eleventh'          : [0, 2, 4, 6, 8, 10]   #includes seven and nine and eleventh
    }

# therefore having the chords in terms of half steps makes sense to me
# those can be built independent of context, having a dominant seventh whenever we want

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
    

def check_flat():
    # returns True, if the default scale with sharps has doubled note names like G and G#
    # this will only work for true diatonic scales as long as no double flats an sharps become involved
    # F# major and Gb major will break the system
    global scale_notes, notes_sharp, root_i 
    for i in range(len(scale_notes)):
        for j in range(i+1, len(scale_notes)):
            # print "i, j, notes ", i, j, notes[(root_i + scale_notes[i])%12][0], notes[(root_i + scale_notes[j])%12][0]
            if notes_sharp[(root_i + scale_notes[i])%12][0]==notes_sharp[(root_i + scale_notes[j])%12][0]:
                return True

    return False
    

def corrected_scale():
    global scale_notes, notes, scale, root_i
    correct_scale = []
    for i in scale_notes:
        correct_scale.append(notes[(root_i + i)%12])
    return correct_scale



# def seminote_to_string(seminote):
#     global scale_notes, notes
#     last_note = notes[seminote]
#     for n in scale_notes[1:]:
#         if notes[n][0] == last_note: #if consecutive note names are equal, somethings wrong
#             pass

def numeral_to_chord(n):
    global root_i, scale_notes, RANDOM_VOICING, notes
    if RANDOM_VOICING:
        voice_name, chord_notes = random.choice(list(chord_types.items()))
        
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

class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    EndCol = '\033[0m'
    Bold = '\033[1m'
    Underline = '\033[4m'
        
def print_chord(chord_semitones):
    b='█'
    w='▒'
    s = bcolors.White
    st = 0
    ri = 0
    colind = []
    close_col = False
    for i in range(14*2+1):
        if (i%14) not in [0,6]:
            if ri < len(chord_semitones) and st%12==chord_semitones[ri]:
                s += bcolors.Red
                close_col = True
                colind.append(i)
                ri += 1
            st += 1
        s += w if (i%14) in [1,3,5,7,9,11,13] else b if (i%14) in [2,4,8,10,12] else '║'
        if close_col:
            close_col = False
            s += bcolors.White

    s = (s+'\n')*2 
    close_col = False
    for i in range(14*2+1):
        if (i%14) in [1,3,5,7,9,11,13] and i in colind: # and ri < len(chord_semitones) and (st%12)==chord_semitones[ri]:
                s += bcolors.Red
                close_col = True
        s += w if (i%14) in [1,3,5,7,9,11,13] else '║'
        if close_col:
            close_col = False
            s += bcolors.White

    s += "\n"+("╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝")

    print(s)


def print_chord_tabs(notes, chord_note_names, use_flat):

    tab_strings_empty = \
'''\
-x--||----|----|----|----|
-x--||----|----|----|----|
-x--||----|----|----|----|
-x--||----|----|----|----|
-x--||----|----|----|----|
-x--||----|----|----|----|\
'''

    tab_strings_empty_list = tab_strings_empty.split('\n')
    tab_strings_empty_list.reverse()

    tab_strings_sharp = \
'''\
-E-||-F-|-F#-|-G-|-G#-|
-B-||-C-|-C#-|-D-|-D#-|
-G-||-G#-|-A-|-A#-|-B-|
-D-||-D#-|-F-|-F#-|-G-|
-A-||-A#-|-B-|-C-|-C#-|
-E-||-F-|-F#-|-G-|-G#-|\
'''

    tab_strings_flat = \
'''\
-E-||-F-|-Gb-|-G-|-Ab-|
-B-||-C-|-Db-|-D-|-Eb-|
-G-||-Ab-|-A-|-Bb-|-B-|
-D-||-Eb-|-F-|-Gb-|-G-|
-A-||-Bb-|-B-|-C-|-Db-|
-E-||-F-|-Gb-|-G-|-Ab-|\
'''

    if use_flat:
        tab_strings = tab_strings_flat
    else:
        tab_strings = tab_strings_sharp

    tab_strings_list = tab_strings.split('\n')
    tab_strings_list.reverse()

    tab_notes_sharp =[\
    ['E','F','F#','G','G#'],
    ['B','C','C#','D','D#'],
    ['G','G#','A','A#','B'],
    ['D','D#','F','F#','G'],
    ['A','A#','B','C','C#'],
    ['E','F','F#','G','G#']]

    tab_notes_flat =[\
    ['E','F','Gb','G','Ab'],
    ['B','C','Db','D','Eb'],
    ['G','Ab','A','Bb','B'],
    ['D','Eb','F','Gb','G'],
    ['A','Bb','B','C','Db'],
    ['E','F','Gb','G','Ab']]

    if use_flat:
        tab_notes = tab_notes_flat
    else:
        tab_notes = tab_notes_sharp

    tab_notes.reverse()

    tab_strings_final = ['','','','','','']
    string_filled = [False,False,False,False,False,False]
    
    for chord_note_i, chord_note in enumerate(chord_note_names):
        found_pos = False
        for string_i, string in enumerate(tab_strings_list):
            if not string_filled[string_i]:
                if chord_note in tab_notes[string_i]:
                    string_filled[string_i] = True
                    found_pos = True

                    tab_notes_wo_chord_note = []
                    tab_notes_wo_chord_note.extend(tab_notes[string_i])
                    tab_notes_wo_chord_note.remove(chord_note)
                    cleared_string = string
                    for note_not_played in tab_notes_wo_chord_note:
                        cleared_string = cleared_string.replace(note_not_played + '-', '---',1)
                    if len(chord_note) == 1:
                        cleared_string = cleared_string.replace(chord_note + '-', chord_note + '--',1)
                        
                    tab_strings_final[string_i] = cleared_string
                    break

        if not found_pos:
            print("ERROR: Could not place", chord_note)

    # Empty strings
    for string_i, string in enumerate(tab_strings_final):
        if string == '':
            tab_strings_final[string_i] = tab_strings_empty_list[string_i]


    # Replace nontes with 'o'
    for string_i, string in enumerate(tab_strings_final):
        for note in notes:
            if len(note) == 1:
                string = string.replace(note + '-', 'o-', 1)    
            else:
                string = string.replace(note, 'o-', 1)    

        tab_strings_final[string_i] = string


    tab_strings_final.reverse()
    print('\n'.join(tab_strings_final))



if root in notes_flat:
    root_i = notes_flat.index(root)
else:
    root_i = notes_sharp.index(root)

scale_notes = scales[scale]

#Switch note table if FLAT
use_flat=check_flat()
if use_flat:
    notes = notes_flat
else:
    notes = notes_sharp


#print corrected_scale()

# tab_notes = ['E', 'A', 'D', 'G', 'B', 'e']
# tab_semitones = [4,9,3,7,11,4]


progression = create_progression(progression_length, starting_chord)
progression_semitones =[]

for c in progression:
    chord_note_names, voicing, chord_semitones = numeral_to_chord(c)
    chord_root_note = notes[(root_i+scales[scale][c-1])%12]
    

    chord_semitones_rising = []
    last_semitone = -1
    for semitone in chord_semitones:
        while semitone < last_semitone:
            semitone += 12
        last_semitone = semitone
        chord_semitones_rising.append(semitone)
    
    progression_semitones.append(chord_semitones_rising)


    print("")
    print(chord_root_note + " " + scale + " " + voicing)
    print_chord(chord_semitones)
    print("-".join(chord_note_names))
    
    print("")
    print_chord_tabs(notes, chord_note_names, use_flat)
    print("")

    print("")

chords2midi.write_midi_file(progression_semitones)