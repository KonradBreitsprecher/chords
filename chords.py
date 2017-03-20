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
