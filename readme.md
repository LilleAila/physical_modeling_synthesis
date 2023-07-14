# Physical modeling synthesis

This project uses the karplus-strong algorithm to synthesize the sounds of plucked strings, like in a guitar.

## Dependencies

This needs `numpy`, `scipy`, `sounddevice` and `soundfile`:
```
python3 -m pip install numpy scipy sounddevice soundfile
```

## Usage

Run `advanced_modeling.py`:
```
python3 advanced_modeling.py
```
Input a midi note number and press enter to play a sound.
Tweak the parameters in `advanced_modeling.py` to change the sound.

Midi notes go up one for each semitone on the piano.
### Examples:
C major scale:
60 62 64 65 67 69 71 72

Octave: +/- 12

Guitar strings (EADGHE)
52 - E
57 - A
62 - D
67 - G
71 - H (B)
76 - E