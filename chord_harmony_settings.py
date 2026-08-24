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

cat1 = None
cat2 = None
cat3 = None
cat4 = None
cat5 = None
cat6 = None
cat7 = None

CYCLES = {
    "1": ["5th", "tritone", None],
    "2": ["major_3rd", "minor_3rd", "sus2", "sus4", None],
    "3": ["major_7th", "minor_7th", "major_6th", "minor_6th", None],
    "4": ["ninth", "eleventh", "thirteenth", None],
    "5": ["octave", None],
    "6": ["fourth_down", None],
    "7": ["octave_down", None],
}

CAT_VARS = ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6", "cat7"]

cat_indices = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}

arpeggiator_thread = None
arpeggiator_running = False

INTERVALS = {
    "5th":         7,
    "tritone":     6,
    "major_3rd":   4,
    "minor_3rd":   3,
    "sus2":        2,
    "sus4":        5,
    "major_7th":   11,
    "minor_7th":   10,
    "major_6th":   9,
    "minor_6th":   8,
    "ninth":       14,
    "eleventh":    17,
    "thirteenth":  21,
    "octave":      12,
    "fourth_down": -5,
    "octave_down": -12,
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
    "1": "ionian", "2": "dorian", "3": "phrygian",
    "4": "lydian", "5": "mixolydian", "6": "aeolian",
    "7": "locrian", "8": "harmonic_minor",
    "9": "whole_tone", "0": "diminished",
}

def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

KEY_TO_MIDI = {
    "a": 60, "w": 61, "s": 62, "e": 63,
    "d": 64, "f": 65, "t": 66, "g": 67,
    "y": 68, "h": 69, "u": 70, "j": 71,
}

def get_freq(midi_note):
    return midi_to_freq(max(0, min(127, midi_note)))

def send_note(freq):
    client.send_message("/nota", [float(freq), waveform, float(amplitude)])

def get_active_layers():
    return [v for v in [cat1, cat2, cat3, cat4, cat5, cat6, cat7] if v is not None]

def print_status():
    layers = get_active_layers()
    harmony_str = " + ".join(layers) if layers else "none"
    if mode == "chord":
        print(f"[CHORD] Oct:{octave} | Wave:{waveform} | Amp:{amplitude:.1f} | Harmony: {harmony_str}")
    else:
        ret = " + return" if scale_return else ""
        print(f"[SCALE] {scale_type} | {scale_direction}{ret} | Oct:{octave} | Wave:{waveform}")

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
        notes = notes + list(reversed(notes[:-1]))

    for midi in notes:
        if not arpeggiator_running:
            break
        send_note(get_freq(midi))
        time.sleep(NOTE_DURATION)

    arpeggiator_running = False

def trigger_arpeggio(root_midi):
    global arpeggiator_thread, arpeggiator_running
    if arpeggiator_running:
        arpeggiator_running = False
        if arpeggiator_thread:
            arpeggiator_thread.join(timeout=0.5)
    arpeggiator_thread = threading.Thread(
        target=play_scale_arpeggio, args=(root_midi,), daemon=True
    )
    arpeggiator_thread.start()

def on_key(event):
    global octave, mode, waveform, amplitude
    global scale_type, scale_direction, scale_return
    global cat1, cat2, cat3, cat4, cat5, cat6, cat7

    key = event.name.lower()

    if key == "esc":
        return

    if key == "q":
        mode = "scale" if mode == "chord" else "chord"
        print(f"Mode: {mode.upper()}")
        print_status()
        return

# Octave
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
        amplitude = min(1.0, round(amplitude + 0.1, 1))
        print(f"Amplitude: {amplitude:.1f}")
        return
    if key == "n":
        amplitude = max(0.0, round(amplitude - 0.1, 1))
        print(f"Amplitude: {amplitude:.1f}")
        return
    if key == "m":
        amplitude = 0.5
        print(f"Amplitude reset: {amplitude:.1f}")
        return

# ── SCALE MODE
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

# ── CHORD MODE
    if mode == "chord":

        if key in CYCLES:
            idx = cat_indices[key]
            cycle = CYCLES[key]
            value = cycle[idx]
            cat_indices[key] = (idx + 1) % len(cycle)

            if key == "1":   cat1 = value
            elif key == "2": cat2 = value
            elif key == "3": cat3 = value
            elif key == "4": cat4 = value
            elif key == "5": cat5 = value
            elif key == "6": cat6 = value
            elif key == "7": cat7 = value

            label = {
                "1": "Fifth/Tritone",
                "2": "Third/Sus",
                "3": "7th/6th",
                "4": "Extended",
                "5": "Octave up",
                "6": "Fourth down",
                "7": "Octave down",
            }[key]
            print(f"{label}: {value or 'OFF'}")
            return

        if key in KEY_TO_MIDI:
            base_midi = KEY_TO_MIDI[key] + (octave - 4) * 12
            base_freq = get_freq(base_midi)
            send_note(base_freq)
            played = [f"{base_freq:.2f} Hz (root)"]

            for layer in get_active_layers():
                if layer in INTERVALS:
                    h_freq = get_freq(base_midi + INTERVALS[layer])
                    send_note(h_freq)
                    played.append(f"{h_freq:.2f} Hz ({layer})")

            print(f"{key.upper()} → " + " | ".join(played))

# ─── STARTUP ──────────────────────────────────────────────────────────────────
print("=" * 55)
print("         MUSICAL KEYBOARD — chord_harmony_settings")
print("=" * 55)
print("OCTAVE   : K = down  |  L = up")
print()
print("MODE     : Q = toggle Chord / Scale")
print()
print("[CHORD MODE]  — press same key to cycle, press again to turn OFF")
print("  1 : 5th → tritone → OFF")
print("  2 : major 3rd → minor 3rd → sus2 → sus4 → OFF")
print("  3 : major 7th → minor 7th → major 6th → minor 6th → OFF")
print("  4 : 9th → 11th → 13th → OFF")
print("  5 : octave up → OFF")
print("  6 : fourth down → OFF")
print("  7 : octave down → OFF")
print()
print("[SCALE MODE]")
print("  1=Ionian  2=Dorian  3=Phrygian  4=Lydian  5=Mixolydian")
print("  6=Aeolian  7=Locrian  8=Harm.Minor  9=WholeTone  0=Diminished")
print("  P = Asc / Desc  |  O = Return to root ON/OFF")
print()
print("WAVEFORM : Z=Sine  X=Square  C=Triangle  V=Saw")
print("AMPLITUDE: B = up  |  N = down  |  M = reset")
print()
print("ESC = quit")
print("=" * 55)

bpm_input = input("BPM (press Enter for default 120): ").strip()
BPM = int(bpm_input) if bpm_input.isdigit() else 120
NOTE_DURATION = 60 / BPM
print(f"BPM set to {BPM}")
print()
print_status()

keyboard.on_press(on_key)
keyboard.wait("esc")
print("Goodbye.")