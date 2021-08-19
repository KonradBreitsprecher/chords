`python progression.py -k "F" -s "mixolydian" -ph -p`

Create a random chord progression.\
Print claviature and tabs.\
Generate a midifile.\
Play the midifile.


```
1) F mixolydian sus2              2) D mixolydian add11             3) G mixolydian ninth             4) C mixolydian ninth        
   F-G-C                             D-F-A-G                           G-Bb-D-F-A                        C-Eb-G-Bb-D

║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║
║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║     ║▒█▒█▒║▒█▒█▒█▒║▒█▒█▒║▒█▒█▒█▒║
║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║     ║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║     ║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║     ║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║▒║
╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝     ╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝     ╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝     ╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝

---||-o-|---|---|                 ---||-o-|---|---|                 ---||-o-|---|---|                 ---||---|---|-o-|
---||-o-|---|---|                 ---||---|---|-o-|                 ---||---|---|-o-|                 ---||---|---|-o-|
-o-||---|---|---|                 -o-||---|---|---|                 ---||---|-o-|---|                 ---||---|---|-o-|
---||---|-o-|---|                 -o-||---|---|---|                 -o-||---|---|---|                 ---||-o-|---|---|
---||---|---|-o-|                 -o-||---|---|---|                 ---||-o-|---|---|                 ---||---|---|-o-|
---||-o-|---|---|                 ---||-o-|---|---|                 ---||---|---|-o-|                 ---||---|---|-o-|
```

```
usage: progression.py [-h] [-k KEY] [-s SCALE] [-n NUM_CHORDS] [-f FIRST] [-v VOICING] [-m MIDIFILE] [-p] [-l] [-ph]

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Key of the chord progression: C | C# | D | D# | E | F | F# | G | G# | A | A# | B
  -s SCALE, --scale SCALE
                        Scale of the chord progression: major | natural_minor | harmonic_minor | melodic_minor | dorian | locrian | lydian | mixolydian | phrygian
  -n NUM_CHORDS, --num-chords NUM_CHORDS
                        Number of chords in the progression
  -f FIRST, --first FIRST
                        Numerical starting chord of the progression
  -v VOICING, --voicing VOICING
                        Voicing to use: triad | first_inv | sec_inv | seventh | first_inv_seventh | sec_inv_seventh | third_inv_seventh | sus2 | sus4 | add9 | add11 | ninth | eleventh | random
  -m MIDIFILE, --midifile MIDIFILE
                        Specify output midifile
  -p, --play            Play the generated midifile via pygame
  -l, --large-hands     Suggest tabs using four bars instead of three. Warning: Only for large hands!
  -ph, --print-horizontal
                        Print the progression horizontally
```
