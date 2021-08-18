import itertools
import re

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
        
def chord_to_claviature(chord_semitones):
    b = '█'
    w = '▒'

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

    return s


def chord_to_tabs(chords_semitones, four_bars):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chord_note_names = []
    for s in chords_semitones:
        chord_note_names.append(notes[s])
    
    if four_bars:
        tab_strings_empty = \
'''\
-x-||---|---|---|---|
-x-||---|---|---|---|
-x-||---|---|---|---|
-x-||---|---|---|---|
-x-||---|---|---|---|
-x-||---|---|---|---|\
'''
    else:
        tab_strings_empty = \
'''\
-x-||---|---|---|
-x-||---|---|---|
-x-||---|---|---|
-x-||---|---|---|
-x-||---|---|---|
-x-||---|---|---|\
'''

    tab_strings_empty_list = tab_strings_empty.split('\n')
    tab_strings_empty_list.reverse()

    if four_bars:
        tab_strings = \
'''\
-E-||-F-|-F#-|-G-|-G#-|
-B-||-C-|-C#-|-D-|-D#-|
-G-||-G#-|-A-|-A#-|-B-|
-D-||-D#-|-F-|-F#-|-G-|
-A-||-A#-|-B-|-C-|-C#-|
-E-||-F-|-F#-|-G-|-G#-|\
'''
    else:
        tab_strings = \
        '''\
-E-||-F-|-F#-|-G-|
-B-||-C-|-C#-|-D-|
-G-||-G#-|-A-|-A#-|
-D-||-D#-|-F-|-F#-|
-A-||-A#-|-B-|-C-|
-E-||-F-|-F#-|-G-|\
'''

    tab_strings_list = tab_strings.split('\n')
    tab_strings_list.reverse()

    if four_bars:
        tab_notes =[\
        ['E','F','F#','G','G#'],
        ['B','C','C#','D','D#'],
        ['G','G#','A','A#','B'],
        ['D','D#','F','F#','G'],
        ['A','A#','B','C','C#'],
        ['E','F','F#','G','G#']]
    else:
        tab_notes =[\
        ['E','F','F#','G'],
        ['B','C','C#','D'],
        ['G','G#','A','A#'],
        ['D','D#','F','F#'],
        ['A','A#','B','C'],
        ['E','F','F#','G']]

    tab_notes.reverse()

    tab_strings_final = ['','','','','','']
    string_filled = [False,False,False,False,False,False]
    
    # Find a spot for each note from low to high strings
    for chord_note in chord_note_names:
        found_pos = False
        for string_i, string in enumerate(tab_strings_list):
            if not string_filled[string_i]:
                if chord_note in tab_notes[string_i]:
                    string_filled[string_i] = True
                    found_pos = True
                    tab_strings_final[string_i] = string_with_note(string_i, string, chord_note, tab_notes)
                    break

        if not found_pos:
            print("ERROR: Could not place", chord_note)
    
    # Now each note got distributed once (or we get the error)
    # but some strings still could be empty
    # Go through all empty strings and try to place a note
    for string_i, string in enumerate(tab_strings_final):
        if string == '':
            found_pos=False
            for chord_note in chord_note_names:
                if chord_note in tab_notes[string_i]:
                    found_pos=True
                    tab_strings_final[string_i] = string_with_note(string_i, tab_strings_list[string_i], chord_note, tab_notes)
                    break
            if not found_pos:
                tab_strings_final[string_i] = tab_strings_empty_list[string_i]

    # Replace note names with 'o'
    for string_i, string in enumerate(tab_strings_final):
        for note in notes:
            if len(note) == 1:
                string = string.replace(note + '-', 'o', 1)    
            else:
                string = string.replace(note, 'o', 1)    

        tab_strings_final[string_i] = string

    # We scan low->high but print high->low
    tab_strings_final.reverse()
    return '\n'.join(tab_strings_final)

def string_with_note(string_i, string, chord_note, tab_notes):
    tab_notes_wo_chord_note = []
    tab_notes_wo_chord_note.extend(tab_notes[string_i])
    tab_notes_wo_chord_note.remove(chord_note)
    cleared_string = string
    for note_not_played in tab_notes_wo_chord_note:
        cleared_string = cleared_string.replace(note_not_played + '-', '--',1)
    if len(chord_note) == 1:
        cleared_string = cleared_string.replace(chord_note + '-', chord_note + '--',1)
    return cleared_string


def print_progression(progression, scale, large_hands, horizontal):
    progression_results = []
    for i, chord in enumerate(progression.chords):
        s = ""
        s += str(i+1) + ") " + chord.root_note + " " + scale + " " + chord.voicing + "\n"
        s += "   " + "-".join(chord.note_names) + "\n"
        s += "\n"
        s += chord_to_claviature(chord.semitones) + "\n"
        s += "\n"
        s += chord_to_tabs(chord.semitones, large_hands) + "\n"
        s += "\n\n"
        progression_results.append(s)

    if horizontal:
        strings_by_column = [s.split("\n") for s in progression_results]
        strings_by_line = zip(*strings_by_column)

        def len_without_colors(s) -> int:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            return len(ansi_escape.sub('', s))

        maxl = min(max([len_without_colors(s) for s in col_strings]) for col_strings in strings_by_column)

        for parts in strings_by_line:
            padded_strings = [
                parts[i].ljust(maxl)
                for i in range(len(parts))
            ]
            print('        '.join(padded_strings))
    else:
        for s in progression_results:
            print(s)

