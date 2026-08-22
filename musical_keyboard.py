from pythonosc import udp_client
import keyboard

modo_acorde_mayores = False
modo_acorde_menores = False
octava = 4
client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


def freq(base_note):
    return base_note * (2 ** (octave - 4))


notes = {
    "a": 261.63,  # C4
    "w": 277.18,  # C#4
    "s": 293.66,  # D4
    "e": 311.13,  # D#4
    "d": 329.63,  # E4
    "f": 349.23,  # F4
    "t": 369.99,  # F#4
    "g": 392.00,  # G4
    "y": 415.30,  # G#4
    "h": 440.00,  # A4
    "u": 466.16,  # A#4
    "j": 493.88,  # B4
    "k": None,  # octave down
    "l": None,  # octave up
}

Major = {
    "a": [261.63, 329.63, 392.00],  # C
    "w": [277.18, 349.23, 415.30],  # C#
    "s": [293.66, 369.99, 440.00],  # D
    "e": [311.13, 392.00, 466.16],  # D#
    "d": [329.63, 415.30, 493.88],  # E
    "f": [349.23, 440.00, 261.63],  # F/C
    "t": [369.99, 466.16, 277.18],  # F#/C#
    "g": [392.00, 493.88, 293.66],  # G/D
    "y": [415.30, 261.63, 311.13],  # G#/C
    "h": [440.00, 277.18, 329.63],  # A/C#
    "u": [466.16, 293.66, 349.23],  # A#/D
    "j": [493.88, 311.13, 369.99],  # B/D#
    "k": None,  # bajar octava
    "l": None,  # subir octava
}

Minor = {
    "a": [261.63, 311.13, 392.00],  # Cm
    "w": [277.18, 329.63, 415.30],  # C#m
    "s": [293.66, 349.23, 440.00],  # Dm
    "e": [311.13, 369.99, 466.16],  # D#m
    "d": [329.63, 392.00, 493.88],  # Em
    "f": [349.23, 415.30, 261.63],  # Fm/C
    "t": [369.99, 440.00, 277.18],  # F#m/C#
    "g": [392.00, 466.16, 293.66],  # Gm/D
    "y": [415.30, 493.88, 311.13],  # G#m/C
    "h": [440.00, 261.63, 329.63],  # Am/C#
    "u": [466.16, 277.18, 349.23],  # A#m/D
    "j": [493.88, 293.66, 369.99],  # Bm/D#
    "k": None,
    "l": None,
}

print(f"=== Music KEYBOARD === Octava: {octava}")
print("O = Mayor Chords (toggle) | P = Minor Chords (toggle)")
print("K = octave down | L = octave up | ESC = salir")


def on_key(event):
    global octava, modo_acorde_mayores, modo_acorde_menores
    key = event.name.lower()

    if key == "esc":
        return False

    # toggle modes
    if key == "o":
        modo_acorde_mayores = not modo_acorde_mayores
        estado = "ON" if modo_acorde_mayores else "OFF"
        print(f"Modo acordes mayores: {estado}")
        return

    if key == "p":
        modo_acorde_menores = not modo_acorde_menores
        estado = "ON" if modo_acorde_menores else "OFF"
        print(f"Modo acordes menores: {estado}")
        return

    # control de octavas
    if key == "k":
        octava = max(1, octava - 1)
        print(f"Octava: {octava}")
        return
    elif key == "l":
        octava = min(8, octava + 1)
        print(f"Octava: {octava}")
        return

    elif key in teclas:
        if modo_acorde_mayores and key in Mayor:
            notas = Mayor[key]

            for base_f in notas:
                f_octava = base_f * (2 ** (octava - 4))
                client.send_message("/nota", float(f_octava))

            print(f"{key.upper()} → MAYOR chord [{len(notas)} notes]")

        elif modo_acorde_menores and key in Menor:
            notas = Menor[key]

            for base_f in notas:
                f_octava = base_f * (2 ** (octava - 4))
                client.send_message("/nota", float(f_octava))

            print(f"{key.upper()} → MENOR chord [{len(notas)} notes]")

        else:
            f = freq(teclas[key])
            client.send_message("/nota", float(f))
            print(f"{key.upper()} → {f:.2f} Hz")

            for base_f in notas:
                f_octava = base_f * (2 ** (octava - 4))
                client.send_message("/nota", float(f_octava))

            print(f"{key.upper()} → {tipo} chord [{len(notas)} notes]")


keyboard.on_press(on_key)
keyboard.wait("esc")
print("Saliendo...")