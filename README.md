Musical Keyboard

Python-based chromatic keyboard with real-time synthesis via SuperCollider.

A terminal-driven musical instrument that maps keyboard keys to chromatic notes and sends them to SuperCollider via OSC. Features two main modes — Chord and Scale — with harmonic layering, arpeggiator, waveform selection, and extended harmony support.

Features

Chord Mode

Full chromatic layout across any octave (C0–C10)
Stackable harmony layers with exclusive categories:
Fifths: perfect 5th / diminished 5th (tritone)
Thirds: major, minor, sus2, sus4
Sevenths / Sixths: major 7th, minor 7th, major 6th, minor 6th
Octave doubling
Extended harmony: 9th, 11th, 13th

Scale Mode

10 scales: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian, Harmonic Minor, Whole Tone, Diminished
Arpeggiator at 120 BPM (triggered from root note)
Ascending / Descending direction toggle
Optional return to root note after scale completes

Sound Engine

4 waveforms: Sine, Square, Triangle, Saw
Real-time amplitude control
Audio routed to SuperCollider via OSC (port 57120)
Key Layout
NOTES    : A W S E D F T G Y H U J  (chromatic, one octave)
OCTAVE   : K = down  |  L = up

MODE     : Q = toggle Chord / Scale

[CHORD MODE]
  Fifths : 1 = 5th       | 2 = minor 5th
  Thirds : 3 = maj 3rd   | 4 = min 3rd  | 5 = sus2 | 6 = sus4
  7th/6th: 7 = maj 7th   | 8 = min 7th  | 9 = maj 6th | 0 = min 6th
  Octave : ' = Octave doubling
  ExtHarm: , = 9th       | . = 11th     | - = 13th

[SCALE MODE]
  Scales : 1=Ionian  2=Dorian  3=Phrygian  4=Lydian  5=Mixolydian
           6=Aeolian  7=Locrian  8=Harm.Minor  9=WholeTone  0=Diminished
  P = toggle Asc / Desc
  O = toggle Return to root ON / OFF

WAVEFORM : Z=Sine  X=Square  C=Triangle  V=Saw
AMPLITUDE: B = up  |  N = down  |  M = reset

ESC = quit
Requirements
Python 3.10+
SuperCollider (for audio output)
Dependencies:
bash
pip install python-osc keyboard
Setup

1. Boot SuperCollider and load the SynthDef:

Open musical_keyboard.scd in SuperCollider and execute the file. This boots the server and registers the OSC listener on /nota.

2. Run the keyboard:

bash
python chord_harmony_settings.py
Tech Stack
Python — keyboard input handling, OSC message routing, arpeggiator logic
SuperCollider — real-time audio synthesis
OSC (Open Sound Control) — communication bridge (port 57120)
python-osc — OSC client library
keyboard — global key event listener
Status

Active development. Extended harmony and scale arpeggiator complete. Planned: BPM control, additional scales, polyphonic sustain mode.

Developed by Nicolás De Lorenzini — GitHub
