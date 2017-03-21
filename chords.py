import random
import sys

root = sys.argv[1] #note string
global_scale = sys.argv[2] #string
progression_length = int(sys.argv[3])

if len(sys.argv) > 4:
    starting_chord = int(sys.argv[4])
else:
    starting_chord = 1

transitions = {
        'major' :           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} , 
        'natural_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'harmonic_minor':   { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'melodic_minor':    { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'dorian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'locrian':          { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'lydian':           { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'mixolydian':       { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
        'phrygian':         { 1: [2,3,4,5,6,7], 2: [5,7], 3: [4,6], 4: [1,5,7], 5: [1], 6: [2,4], 7: [1,5]} ,
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

def number_to_chord(number):
    global root, global_scale
    scales = {
            'major' :           [0, 2, 4, 5, 7, 9, 11],
            'natural_minor':    [0, 2, 3, 5, 7, 8, 10],
            'harmonic_minor':   [0, 2, 3, 5, 7, 8, 11],
            'melodic_minor':    [0, 2, 3, 5, 7, 9, 11],
            'dorian':           [0, 2, 3, 5, 7, 9, 10],
            'locrian':          [0, 1, 3, 5, 6, 8, 10],
            'lydian':           [0, 2, 4, 6, 7, 9, 11],
            'mixolydian':       [0, 2, 4, 5, 7, 9, 10],
            'phrygian':         [0, 1, 3, 5, 7, 8, 10],
#        'major_pentatonic': ['2', '4', '7', '9', '12'],
#        'minor_pentatonic': ['3', '5', '7', '10', '12']
    }
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    scale = scales[global_scale]
    root_index = notes.index(root)
    return notes[(root_index+scale[number-1])%12] + '-' + notes[(root_index+scale[(number+1)%7])%12] + '-' + notes[(root_index+scale[(number+3)%7])%12]
    

def create_progression(length,starting_chord):
    global global_scale
    progression = []
    progression.append(starting_chord) 
    act_chord = starting_chord
    for i in range(length-1):
        new_chord = random.choice(transitions[global_scale][act_chord])
        progression.append(new_chord)
        act_chord=new_chord
    return progression


progression = create_progression(progression_length, starting_chord)

chord_string = ""
for c in progression:
    chord_string += number_to_chord(c) + " "

print chord_string
