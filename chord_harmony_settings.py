from pythonosc import udp_client
import keyboard
import threading
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

octave = 4
mode = "chord"
waveform = "sine"
amplitude = 0.5

scale_type = "ionian"
scale_direction = "asc"
scale_return = False

active_fifth = None
active_third = None
active_seventh = None
active_octave = None
active_extended = None

arpeggiator_thread = None
arpeggiator_running = False

def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

KEY_TO_MIDI = {
    "a": 60,  # C
    "w": 61,  # C#
    "s": 62,  # D
    "e": 63,  # D#
    "d": 64,  # E
    "f": 65,  # F
    "t": 66,  # F#
    "g": 67,  # G
    "y": 68,  # G#
    "h": 69,  # A
    "u": 70,  # A#
    "j": 71,  # B
}

INTERVALS = {
    "5th":        7,
    "minor_5th":  6,
    "major_3rd":  4,
    "minor_3rd":  3,
    "sus2":       2,
    "sus4":       5,
    "major_7th":  11,
    "minor_7th":  10,
    "major_6th":  9,
    "minor_6th":  8,
    "octave": 12,
    "ninth": 14,
    "eleventh": 17,
    "thirteenth": 21
}

SCALES = {
    "ionian":         [0, 2, 4, 5, 7, 9, 11, 12],
    "dorian":         [0, 2, 3, 5, 7, 9, 10, 12],
    "phrygian":       [0, 1, 3, 5, 7, 8, 10, 12],
    "lydian":         [0, 2, 4, 6, 7, 9, 11, 12],
    "mixolydian":     [0, 2, 4, 5, 7, 9, 10, 12],
    "aeolian":        [0, 2, 3, 5, 7, 8, 10, 12],
    "locrian":        [0, 1, 3, 5, 6, 8, 10, 12],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11, 12],
    "whole_tone":     [0, 2, 4, 6, 8, 10, 12],
    "diminished":     [0, 3, 6, 9, 12],
}

SCALE_KEYS = {
    "1": "ionian",
    "2": "dorian",
    "3": "phrygian",
    "4": "lydian",
    "5": "mixolydian",
    "6": "aeolian",
    "7": "locrian",
    "8": "harmonic_minor",
    "9": "whole_tone",
    "0": "diminished",
}

def get_freq(midi_note):
    midi_note = max(0, min(127, midi_note))
    return midi_to_freq(midi_note)

def send_note(freq):
    client.send_message("/nota", [float(freq), waveform, float(amplitude)])

def print_status():
    harmony = []
    if active_fifth:    harmony.append(active_fifth)
    if active_third:    harmony.append(active_third)
    if active_seventh:  harmony.append(active_seventh)
    if active_octave:   harmony.append(active_octave)
    if active_extended: harmony.append(active_extended)
    harmony_str = " + ".join(harmony) if harmony else "none"

    if mode == "chord":
        print(f"[CHORD] Octave: {octave} | Wave: {waveform} | Amp: {amplitude:.1f} | Harmony: {harmony_str}")
    else:
        dir_str = f"{scale_direction}" + (" + return" if scale_return else "")
        print(f"[SCALE] {scale_type} | {dir_str} | Octave: {octave} | Wave: {waveform} | Amp: {amplitude:.1f}")

BPM = 120
NOTE_DURATION = 60 / BPM

def play_scale_arpeggio(root_midi):
    global arpeggiator_running

    arpeggiator_running = True
    intervals = SCALES.get(scale_type, SCALES["ionian"])

    notes = [root_midi + i for i in intervals]

    if scale_direction == "desc":
        notes = list(reversed(notes))

    if scale_return:
        if scale_direction == "asc":
            notes = notes + list(reversed(notes[:-1]))
        else:
            notes = notes + list(reversed(notes[:-1]))

    for midi in notes:
        if not arpeggiator_running:
            break
        freq = get_freq(midi)
        send_note(freq)
        time.sleep(NOTE_DURATION)

    arpeggiator_running = False

def trigger_arpeggio(root_midi):
    global arpeggiator_thread, arpeggiator_running

    if arpeggiator_running:
        arpeggiator_running = False
        if arpeggiator_thread:
            arpeggiator_thread.join(timeout=0.5)

    arpeggiator_thread = threading.Thread(target=play_scale_arpeggio, args=(root_midi,), daemon=True)
    arpeggiator_thread.start()

def on_key(event):
    global octave, mode, waveform, amplitude
    global scale_type, scale_direction, scale_return
    global active_fifth, active_third, active_seventh, active_octave, active_extended

    key = event.name.lower()

    if key == "esc":
        return

    if key == "q":
        mode = "scale" if mode == "chord" else "chord"
        print(f"Mode: {mode.upper()}")
        print_status()
        return

    if key == "k":
        octave = max(0, octave - 1)
        print_status()
        return
    if key == "l":
        octave = min(10, octave + 1)
        print_status()
        return

    waveform_map = {"z": "sine", "x": "square", "c": "triangle", "v": "saw"}
    if key in waveform_map:
        waveform = waveform_map[key]
        print(f"Waveform: {waveform}")
        return

    if key == "b":
        amplitude = min(1.0, amplitude + 0.1)
        print(f"Amplitude: {amplitude:.1f}")
        return
    if key == "n":
        amplitude = max(0.0, amplitude - 0.1)
        print(f"Amplitude: {amplitude:.1f}")
        return
    if key == "m":
        amplitude = 0.5
        print(f"Amplitude reset: {amplitude:.1f}")
        return

#scale mode:
    if mode == "scale":
        if key in SCALE_KEYS:
            scale_type = SCALE_KEYS[key]
            print(f"Scale: {scale_type}")
            return

        if key == "p":
            scale_direction = "desc" if scale_direction == "asc" else "asc"
            print(f"Direction: {scale_direction}")
            return

        if key == "o":
            scale_return = not scale_return
            print(f"Return to root: {'ON' if scale_return else 'OFF'}")
            return

        if key in KEY_TO_MIDI:
            base_midi = KEY_TO_MIDI[key] + (octave - 4) * 12
            print(f"{key.upper()} → {scale_type} from {get_freq(base_midi):.2f} Hz [{scale_direction}]")
            trigger_arpeggio(base_midi)
        return

#chord mode
    if mode == "chord":

        fifth_map = {"1": "5th", "2": "minor_5th"}
        if key in fifth_map:
            chosen = fifth_map[key]
            active_fifth = None if active_fifth == chosen else chosen
            print(f"Fifth: {active_fifth or 'OFF'}")
            return

        third_map = {"3": "major_3rd", "4": "minor_3rd", "5": "sus2", "6": "sus4"}
        if key in third_map:
            chosen = third_map[key]
            active_third = None if active_third == chosen else chosen
            print(f"Third: {active_third or 'OFF'}")
            return

        seventh_map = {"7": "major_7th", "8": "minor_7th", "9": "major_6th", "0": "minor_6th"}
        if key in seventh_map:
            chosen = seventh_map[key]
            active_seventh = None if active_seventh == chosen else chosen
            print(f"Seventh/Sixth: {active_seventh or 'OFF'}")
            return

        octave_map = {"'": "octave"}
        if key in octave_map:
            chosen = octave_map[key]
            active_octave = None if active_octave == chosen else chosen
            print(f"Octave: {active_octave or 'OFF'}")
            return

        extended_map = {",": "ninth", ".": "eleventh", "-": "thirteenth"}
        if key in extended_map:
            chosen = extended_map[key]
            active_extended = None if active_extended == chosen else chosen
            print(f"Extended Harmony: {active_extended or 'OFF'}")
            return

        if key in KEY_TO_MIDI:
            base_midi = KEY_TO_MIDI[key] + (octave - 4) * 12
            base_freq = get_freq(base_midi)
            send_note(base_freq)

            played = [f"{base_freq:.2f} Hz (root)"]

            for layer in [active_fifth, active_third, active_seventh, active_octave, active_extended]:
                if layer and layer in INTERVALS:
                    harmony_midi = base_midi + INTERVALS[layer]
                    harmony_freq = get_freq(harmony_midi)
                    send_note(harmony_freq)
                    played.append(f"{harmony_freq:.2f} Hz ({layer})")

            print(f"{key.upper()} → " + " | ".join(played))

#STARTUP
print("=" * 55)
print("         MUSICAL KEYBOARD")
print("=" * 55)
print("NOTES    : A W S E D F T G Y H U J  (chromatic)")
print("OCTAVE   : K = down  |  L = up")
print()
print("MODE     : Q = toggle Chord / Scale")
print()
print("[CHORD MODE]")
print("  Fifths : 1 = 5th       | 2 = minor 5th")
print("  Thirds : 3 = maj 3rd   | 4 = min 3rd  | 5 = sus2 | 6 = sus4")
print("  7th/6th: 7 = maj 7th   | 8 = min 7th  | 9 = maj 6th | 0 = min 6th")
print("  Octave : ' = Octave up")
print("  ExtHarm: , = 9th       | . = 11th     | - = 13th")
print()
print("[SCALE MODE]")
print("  Scales : 1=Ionian 2=Dorian 3=Phrygian 4=Lydian 5=Mixolydian")
print("           6=Aeolian 7=Locrian 8=Harm.Minor 9=WholeTone 0=Diminished")
print("  P = toggle Asc / Desc")
print("  O = toggle Return to root ON / OFF")
print()
print("WAVEFORM : Z=Sine X=Square C=Triangle V=Saw")
print("AMPLITUDE: B = up  |  N = down  |  M = reset")
print()
print("ESC = quit")
print("=" * 55)
print_status()

keyboard.on_press(on_key)
keyboard.wait("esc")
print("Ciao.")