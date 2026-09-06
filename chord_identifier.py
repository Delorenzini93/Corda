NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
#         0     1    2     3    4    5    6     7     8    9    10    11
CUERDAS_AL_AIRE = {
    6: 4,
    5: 9,
    4: 2,
    3: 7,
    2: 11,
    1: 4,
}

ACORDES = {
"C mayor" : (0, 4, 7),
"C minor" : (0, 3, 7),
"Cmaj7"   : (0, 4, 7, 11),
"C7"      : (0, 4, 7, 10),
"Csus2"   : (0, 2, 7),
"Csus4"   : (0, 5, 7),
"Cdim"    : (0, 3, 6),
"Cdim7"   : (0, 3, 6, 10),
"C+"      : (0, 4, 8),
"Cm(maj7)": (0, 3, 7, 11),
"C6"      : (0, 4, 7, 9),
"Cm6"     : (0, 3, 7, 9),
#==========================================================
"C# mayor" : (1, 5, 8),
"C# minor" : (1, 4, 8),
"C#maj7"   : (1, 5, 8, 0),
"C#7"      : (1, 5, 8, 11),
"C#sus2"   : (1, 3, 8),
"C#sus4"   : (1, 6, 8),
"C#dim"    : (1, 4, 7),
"C#dim7"   : (1, 4, 7, 11),
"C#+"      : (1, 5, 9),
"C#m(maj7)": (1, 4, 8, 0),
"C#6"      : (1, 5, 8, 10),
"C#m6"     : (1, 4, 8, 10),
#==========================================================
"D mayor" : (2, 6, 9),
"D minor" : (2, 5, 9),
"Dmaj7"   : (2, 6, 9, 1),
"D7"      : (2, 6, 9, 0),
"Dsus2"   : (2, 4, 9),
"Dsus4"   : (2, 7, 9),
"Ddim"    : (2, 5, 8),
"Ddim7"   : (2, 5, 8, 0),
"D+"      : (2, 6, 10),
"Dm(maj7)": (2, 5, 9, 1),
"D6"      : (2, 6, 9, 11),
"Dm6"     : (2, 5, 9, 11),
#==========================================================
"D# mayor" : (3, 7, 10),
"D# minor" : (3, 6, 10),
"D#maj7"   : (3, 7, 10, 2),
"D#7"      : (3, 7, 10, 1),
"D#sus2"   : (3, 5, 10),
"D#sus4"   : (3, 8, 10),
"D#dim"    : (3, 6, 9),
"D#dim7"   : (3, 6, 9, 1),
"D#+"      : (3, 7, 11),
"D#m(maj7)": (3, 6, 10, 2),
"D#6"      : (3, 7, 10, 0),
"D#m6"     : (3, 6, 10, 0),
#==========================================================
"E mayor" : (4, 8, 11),
"E minor" : (4, 7, 11),
"Emaj7"   : (4, 8, 11, 3),
"E7"      : (4, 8, 11, 2),
"Esus2"   : (4, 6, 11),
"Esus4"   : (4, 9, 11),
"Edim"    : (4, 7, 10),
"Edim7"   : (4, 7, 10, 2),
"E+"      : (4, 8, 0),
"Em(maj7)": (4, 7, 11, 3),
"E6"      : (4, 8, 11, 1),
"Em6"     : (4, 7, 11, 1),
#==========================================================
"F mayor" : (5, 9, 0),
"F minor" : (5, 8, 0),
"Fmaj7"   : (5, 9, 0, 4),
"F7"      : (5, 9, 0, 3),
"Fsus2"   : (5, 7, 0),
"Fsus4"   : (5, 10, 0),
"Fdim"    : (5, 8, 11),
"Fdim7"   : (5, 8, 11, 3),
"F+"      : (5, 9, 1),
"Fm(maj7)": (5, 8, 0, 4),
"F6"      : (5, 9, 0, 2),
"Fm6"     : (5, 8, 0, 2),
#==========================================================
"F# mayor" : (6, 10, 1),
"F# minor" : (6, 9, 1),
"F#maj7"   : (6, 10, 1, 5),
"F#7"      : (6, 10, 1, 4),
"F#sus2"   : (6, 8, 1),
"F#sus4"   : (6, 11, 1),
"F#dim"    : (6, 9, 0),
"F#dim7"   : (6, 9, 0, 4),
"F#+"      : (6, 10, 2),
"F#m(maj7)": (6, 9, 1, 5),
"F#6"      : (6, 10, 1, 3),
"F#m6"     : (6, 9, 1, 3),
#==========================================================
"G mayor" : (7, 11, 2),
"G minor" : (7, 10, 2),
"Gmaj7"   : (7, 11, 2, 6),
"G7"      : (7, 11, 2, 5),
"Gsus2"   : (7, 9, 2),
"Gsus4"   : (7, 0, 2),
"Gdim"    : (7, 10, 1),
"Gdim7"   : (7, 10, 1, 5),
"G+"      : (7, 11, 3),
"Gm(maj7)": (7, 10, 2, 6),
"G6"      : (7, 11, 2, 4),
"Gm6"     : (7, 10, 2, 4),
#==========================================================
"G# mayor" : (8, 0, 3),
"G# minor" : (8, 11, 3),
"G#maj7"   : (8, 0, 3, 7),
"G#7"      : (8, 0, 3, 6),
"G#sus2"   : (8, 10, 3),
"G#sus4"   : (8, 1, 3),
"G#dim"    : (8, 11, 2),
"G#dim7"   : (8, 11, 2, 6),
"G#+"      : (8, 0, 4),
"G#m(maj7)": (8, 11, 3, 7),
"G#6"      : (8, 0, 3, 5),
"G#m6"     : (8, 11, 3, 5),
#==========================================================
"A mayor" : (9, 1, 4),
"A minor" : (9, 0, 4),
"Amaj7"   : (9, 1, 4, 8),
"A7"      : (9, 1, 4, 7),
"Asus2"   : (9, 11, 4),
"Asus4"   : (9, 2, 4),
"Adim"    : (9, 0, 3),
"Adim7"   : (9, 0, 3, 7),
"A+"      : (9, 1, 5),
"Am(maj7)": (9, 0, 4, 8),
"A6"      : (9, 1, 4, 6),
"Am6"     : (9, 0, 4, 6),
#==========================================================
"A# mayor" : (10, 2, 5),
"A# minor" : (10, 1, 5),
"A#maj7"   : (10, 2, 5, 9),
"A#7"      : (10, 2, 5, 8),
"A#sus2"   : (10, 0, 5),
"A#sus4"   : (10, 3, 5),
"A#dim"    : (10, 1, 4),
"A#dim7"   : (10, 1, 4, 8),
"A#+"      : (10, 2, 6),
"A#m(maj7)": (10, 1, 5, 9),
"A#6"      : (10, 2, 5, 7),
"A#m6"     : (10, 1, 5, 7),
#==========================================================
"B mayor" : (11, 3, 6),
"B minor" : (11, 2, 6),
"Bmaj7"   : (11, 3, 6, 10),
"B7"      : (11, 3, 6, 9),
"Bsus2"   : (11, 1, 6),
"Bsus4"   : (11, 4, 6),
"Bdim"    : (11, 2, 5),
"Bdim7"   : (11, 2, 5, 9),
"B+"      : (11, 3, 7),
"Bm(maj7)": (11, 2, 6, 10),
"B6"      : (11, 3, 6, 8),
"Bm6"     : (11, 2, 6, 8),
}

def nota_en_traste(cuerda, traste):
    if traste == "x":
        return None
    valor = (CUERDAS_AL_AIRE[cuerda] + int(traste)) % 12
    return valor

def identificar_acorde(valores, bajo):
    candidatos = []
    for nombre, intervalos in ACORDES.items():
        if set(intervalos) == valores:
            candidatos.append((nombre, intervalos))

    if not candidatos:
        return "Acorde no identificado"

    for nombre, intervalos in candidatos:
        if intervalos[0] == bajo:
            return nombre

    return candidatos[0][0]

while True:
    entrada = input("Enter chord fingering from lowest string to highest string: ")
    acorde = list(entrada)

    valores_resultantes = []
    bajo = None

    for i, traste in enumerate(acorde):
        cuerda = 6 - i
        valor = nota_en_traste(cuerda, traste)
        if valor is not None:
            valores_resultantes.append(valor)
            if bajo is None:
                bajo = valor

    valores_unicos = set(valores_resultantes)

    print(f"Notas resultantes: {[NOTAS[v] for v in valores_resultantes]}")
    print(identificar_acorde(valores_unicos, bajo))