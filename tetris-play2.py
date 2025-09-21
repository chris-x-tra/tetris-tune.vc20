#!/usr/bin/python

# mit schlagzeug
# mit trackerstyle-ansicht

#
#pip install sounddevice numpy 
#

import numpy as np
import sounddevice as sd
import time
import argparse
import os
import curses

#DUR_1_4 = 12
#DUR_2_4 = 24
#DUR_3_4 = 36
#DUR_4_4 = 48

DUR_1_4 = 10
DUR_2_4 = 20
DUR_3_4 = 30
DUR_4_4 = 40

DRUM_P = 48
#DRUM_P_2 = 24
DRUM_P_2 = 20

BD_P = 1
SD_P = 1

BDV2_P = 1

# ---------------------------------------
# Frequenztabelle (alles klein geschrieben)
# ---------------------------------------
NOTE_FREQUENCIES = {
    "g1": 49.00, "a1": 55.00, "h1": 61.74,
    "c2": 65.41, "d2": 73.42, "e2": 82.41, "f2": 87.31,
    "g2": 98.00, "a2": 110.00, "h2": 123.47,
    "c3": 130.81, "d3": 146.83, "e3": 164.81, "f3": 174.61,

    "g4": 392.00, "a4": 440.00, "h4": 493.88,
    "c5": 523.25, "d5": 587.33, "e5": 659.25,
    "f5": 698.46, "g5": 783.99, "a5": 880.00,
}
note_to_vic = {
    # Voice 1 (low)
    "g1": 0xA7, "a1": 0xB0, "h1": 0xB9,
    "c2": 0xBD, "d2": 0xC4, "e2": 0xCA, "f2": 0xCD,
    "g2": 0xD3, "a2": 0xD8, "h2": 0xDC,
    "c3": 0xDE, "d3": 0xE2, "e3": 0xE5, "f3": 0xE6,

    # Voice 2 (high)
    "c4": 0xDE, "d4": 0xE2, "e4": 0xE5, "f4": 0xE6,
    "g4": 0xEA, "a4": 0xEB, "h4": 0xED,
    "c5": 0xEE, "d5": 0xF0, "e5": 0xF2, "f5": 0xF3,
    "g5": 0xF4, "a5": 0xF5, "h5": 0xF6,

    "p": "0x00",   # Pause
    "bd": "0xF0",  # Bassdrum
    "sd": "0xF1"   # Snare
}

    ###
    ###
    # Voice 1: Bass
notes1 = [
    ("e2",DUR_1_4),("e3",DUR_1_4),("e2",DUR_1_4),("e3",DUR_1_4),("e2",DUR_1_4),("e3",DUR_1_4),("e2",DUR_1_4),("e3",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("d2",DUR_1_4),("d3",DUR_1_4),("d2",DUR_1_4),("d3",DUR_1_4),("d2",DUR_1_4),("d3",DUR_1_4),("d2",DUR_1_4),("d3",DUR_1_4),
    ("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),
    ("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("g1",DUR_1_4),("g2",DUR_1_4),("g1",DUR_1_4),("g2",DUR_1_4),("g1",DUR_1_4),("g2",DUR_1_4),("g1",DUR_1_4),("g2",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),
    ("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),("a1",DUR_1_4),("a2",DUR_1_4),
    ("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),
    ("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),("c2",DUR_1_4),("c3",DUR_1_4),
    ("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),("h1",DUR_1_4),("h2",DUR_1_4),
    ]

    ###
    ###
    # Voice 2: Melodie
notes2 = [
    ("e5",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),("c5",DUR_1_4),("h4",DUR_1_4),
    ("a4",DUR_1_4),("a4",DUR_1_4),("c5",DUR_1_4),("e5",DUR_1_4),("d5",DUR_1_4),("c5",DUR_1_4),
    ("h4",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),("a4",DUR_1_4),
    ("a4",DUR_1_4),("p",2), ("p",DUR_1_4), ("d5",DUR_1_4),("f5",DUR_1_4),("a5",DUR_1_4),
    ("g5",DUR_1_4),("f5",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),("e5",DUR_1_4),("d5",DUR_1_4),
    ("c5",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),
    ("a4",DUR_1_4),("a4",DUR_1_4),("p",2),("e5",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),
    ("h4",DUR_1_4),("c5",DUR_1_4),("a4",DUR_1_4),("g4",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),
    ("d5",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),("e5",DUR_1_4),("a5",DUR_1_4),("a5",DUR_1_4),
    ("g5",DUR_1_4),("e5",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),("c5",DUR_1_4),
    ("h4",DUR_1_4),("a4",DUR_1_4),("a4",DUR_1_4),("c5",DUR_1_4),("e5",DUR_1_4),("d5",DUR_1_4),
    ("c5",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),("d5",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),
    ("a4",DUR_1_4),("a4",DUR_1_4),("p",2),("p",DUR_1_4),("d5",DUR_1_4),("f5",DUR_1_4),
    ("a5",DUR_1_4),("g5",DUR_1_4),("f5",DUR_1_4),("p",DUR_1_4),("e5",DUR_1_4),("c5",DUR_1_4),
    ("e5",DUR_1_4),("d5",DUR_1_4),("c5",DUR_1_4),("p",DUR_1_4),("h4",DUR_1_4),("c5",DUR_1_4),
    ("d5",DUR_1_4),("e5",DUR_1_4),("p",DUR_1_4),("c5",DUR_1_4),("a4",DUR_1_4),("a4",DUR_1_4),
    ]

    ###
    ###
    # Voice 3: 
notes3 =  [
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1)
    ]


    ###
    ###
    # Voice 4: (Teil-)Schlagzeug
    # 1. Abschnitt: nur Pausen
pattern1 = [
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1),
        ("p", 1), ("p", 1), ("p", 1), ("p", 1)
        ]

    # 2. Abschnitt: Bassdrum auf 1 und 3, hoert sich am vc 20 aber eher an wie snare
pattern2 = [
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2)
        ]

    # 3. Abschnitt: Bassdrum & Snare im Wechsel
pattern3 = [
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2),
        ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2), ("bd", 1), ("p", DRUM_P_2), ("sd", 1), ("p", DRUM_P_2)
        ]
# zusammenfgen:
#notes4 = pattern1 + pattern2 + pattern3

notes4 = pattern2 * 3

bd_pattern = [
    (0xF0, BD_P), (0xD0, BD_P), (0xC0, BD_P), (0x80, BD_P),
    (0x00, BD_P), (0x00, BD_P), (0x00, BD_P), (0x00, BD_P),
    (0x00, BD_P), (0x00, BD_P), (0x00, BD_P), (0x00, BD_P)
]

sd_pattern = [
    (0xB0, SD_P), (0xB4, SD_P), (0xB8, SD_P), (0xB4, SD_P),
    (0xB0, SD_P), (0xA8, SD_P), (0xA0, SD_P), (0x98, SD_P),
    (0x00, SD_P), (0x00, SD_P), (0x00, SD_P), (0x00, SD_P),
    (0x00, SD_P), (0x00, SD_P), (0x00, SD_P), (0x00, SD_P),
    (0x00, SD_P), (0x00, SD_P), (0x00, SD_P), (0x00, SD_P)
]

bdv2_pattern = [
    (0xF0, BDV2_P),  # sehr hoch
    (0xD0, BDV2_P),  # hoch
    (0xB0, BDV2_P),  # mittelhoch
    (0x90, BDV2_P),  # mitteltief
    (0x70, BDV2_P),  # tief
    (0x50, BDV2_P),  # sehr tief
    (0x30, BDV2_P),  # Sub
    (0x00, BDV2_P),  # aus
    (0x00, BDV2_P),  # Stille
    (0x00, BDV2_P)
]

# ---------------------------------------
# Bassdrum Synthese (Sweep)
# ---------------------------------------
def bass_drum(unit_length=0.02, samplerate=44100):
    steps = 8
    start_freq = 200.0
    end_freq = 60.0
    freqs = np.geomspace(start_freq, end_freq, steps)
    parts = []
    for i, f in enumerate(freqs):
        dur = unit_length
        amp = 1.0 - (i / steps)
        t = np.linspace(0, dur, int(samplerate * dur), endpoint=False)
        part = amp * np.sign(np.sin(2 * np.pi * f * t))
        parts.append(part)
    return np.concatenate(parts)

# ---------------------------------------
# Snaredrum Synthese
# ---------------------------------------
def snare_drum(unit_length=0.02, samplerate=44100):
    steps = 6  # Gesamtdauer ~ 6 * unit_length
    parts = []
    for i in range(steps):
        dur = unit_length
        amp = 1.0 - (i / steps)  # abklingende Amplitude
        t = np.linspace(0, dur, int(samplerate * dur), endpoint=False)
        noise = np.random.uniform(-1, 1, size=t.shape)
        parts.append(noise * amp)
    return np.concatenate(parts)

# ---------------------------------------
# Note-zu-Wave Umwandlung
# ---------------------------------------
def note_to_wave(note, duration_units, unit_length=0.02, samplerate=44100):
    note_key = str(note).lower()

    # Pause
    if note_key.startswith("p"):
        length = int(samplerate * duration_units * unit_length)
        return np.zeros(length, dtype=np.float32)

    # Bassdrum
    if note_key == "bd":
        raw_bd = bass_drum(unit_length, samplerate)
        target_len = int(samplerate * duration_units * unit_length)

        if len(raw_bd) > target_len:
            return raw_bd[:target_len] * 0.6
        elif len(raw_bd) < target_len:
            pad = np.zeros(target_len - len(raw_bd), dtype=np.float32)
            return np.concatenate([raw_bd * 0.6, pad])
        else:
            return raw_bd * 0.6

    # Snaredrum
    if note_key == "sd":
        raw_sd = snare_drum(unit_length, samplerate)
        target_len = int(samplerate * duration_units * unit_length)

        if len(raw_sd) > target_len:
            return raw_sd[:target_len] * 0.6
        elif len(raw_sd) < target_len:
            pad = np.zeros(target_len - len(raw_sd), dtype=np.float32)
            return np.concatenate([raw_sd * 0.6, pad])
        else:
            return raw_sd * 0.6

    # Normale Note
    freq = NOTE_FREQUENCIES.get(note_key, None)
    if freq is None:
        length = int(samplerate * duration_units * unit_length)
        return np.zeros(length, dtype=np.float32)

    dur = duration_units * unit_length
    length = int(samplerate * dur)
    t = np.linspace(0, dur, length, endpoint=False)
    wave = np.sign(np.sin(2 * np.pi * freq * t))
    return wave * 0.3

# ---------------------------------------
# Drei-Stimmen-Player
# ---------------------------------------
def play_three_voices(notes1, notes2, notes3,
                      unit_length=0.02, samplerate=44100):
    maxlen = max(len(notes1), len(notes2), len(notes3))

    n1 = notes1 + [("p",1)]*(maxlen - len(notes1))
    n2 = notes2 + [("p",1)]*(maxlen - len(notes2))
    n3 = notes3 + [("p",1)]*(maxlen - len(notes3))

    song = []
    for (note1, dur1), (note2, dur2), (note3, dur3) in zip(n1, n2, n3):
        dur = max(dur1, dur2, dur3)
        w1 = note_to_wave(note1, dur, unit_length, samplerate)
        w2 = note_to_wave(note2, dur, unit_length, samplerate)
        w3 = note_to_wave(note3, dur, unit_length, samplerate)
        mix = (w1 + w2 + w3) * 0.3
        song.append(mix)

    audio = np.concatenate(song)
    sd.play(audio, samplerate=samplerate)
    sd.wait()

def play_three_voices_with_display(notes1, notes2, notes3,
                                   unit_length=0.02, samplerate=44100):
    maxlen = max(len(notes1), len(notes2), len(notes3))
    n1 = notes1 + [("p",1)]*(maxlen - len(notes1))
    n2 = notes2 + [("p",1)]*(maxlen - len(notes2))
    n3 = notes3 + [("p",1)]*(maxlen - len(notes3))

    for i, ((note1, dur1), (note2, dur2), (note3, dur3)) in enumerate(zip(n1, n2, n3)):
        dur = max(dur1, dur2, dur3)

        w1 = note_to_wave(note1, dur, unit_length, samplerate)
        w2 = note_to_wave(note2, dur, unit_length, samplerate)
        w3 = note_to_wave(note3, dur, unit_length, samplerate)

        mix = (w1 + w2 + w3) * 0.3

        # Abspielen dieser Note
        sd.play(mix, samplerate=samplerate)
        sd.wait()

        # Anzeige
        print(f"{i:03d}: V1={note1:<3} V2={note2:<3} V3={note3:<3} dur={dur}")

        # kurze Pause, um ticken zu vermeiden
        time.sleep(0.001)

def tracker_player(stdscr, notes1, notes2, notes3,
                   unit_length=0.02, samplerate=44100):

    curses.curs_set(0)   # kein Cursor
    stdscr.nodelay(True) # Eingaben nicht blockieren

    maxlen = max(len(notes1), len(notes2), len(notes3))
    n1 = notes1 + [("p",1)]*(maxlen - len(notes1))
    n2 = notes2 + [("p",1)]*(maxlen - len(notes2))
    n3 = notes3 + [("p",1)]*(maxlen - len(notes3))

    for i, ((note1, dur1), (note2, dur2), (note3, dur3)) in enumerate(zip(n1, n2, n3)):
        dur = max(dur1, dur2, dur3)

        # Wellen erzeugen
        w1 = note_to_wave(note1, dur, unit_length, samplerate)
        w2 = note_to_wave(note2, dur, unit_length, samplerate)
        w3 = note_to_wave(note3, dur, unit_length, samplerate)
        mix = (w1 + w2 + w3) * 0.3

        # Tracker-Ausgabe
        stdscr.clear()
        stdscr.addstr(0, 0, "Step | Voice1 | Voice2 | Voice3")
        stdscr.addstr(1, 0, "-"*35)

        start = max(0, i-10)        # nur 10 Zeilen vorher zeigen
        end = min(maxlen, i+15)     # ein Stuck nach vorne
        for row, j in enumerate(range(start, end), start=2):
            marker = ">" if j == i else " "
            stdscr.addstr(row, 0,
                f"{marker}{j:03d} | {n1[j][0]:<6} | {n2[j][0]:<6} | {n3[j][0]:<6}")
        stdscr.refresh()

        # Abspielen dieser Note
        sd.play(mix, samplerate=samplerate)
        sd.wait()
        time.sleep(0.001)

def play_with_tracker(notes1, notes2, notes3):
    curses.wrapper(tracker_player, notes1, notes2, notes3)

def _normalize_to_byte(val):
    """
    Nimmt int oder String wie "$F0", "F0" oder "0xF0" oder "240" und
    gibt einen Integer 0..255 zurÃ¼ck. Wir werfen bei unparsbaren Werten.
    """
    if isinstance(val, int):
        return val & 0xFF
    if isinstance(val, str):
        s = val.strip()
        if s.startswith('$'):
            s = s[1:]
        if s.startswith('0x') or s.startswith('0X'):
            s = s[2:]
        # jetzt versuchen als hex, sonst als dezimal
        try:
            return int(s, 16) & 0xFF
        except ValueError:
            try:
                return int(s, 10) & 0xFF
            except ValueError:
                raise ValueError(f"Cannot parse mapping value: {val!r}")
    raise TypeError(f"Unsupported mapping value type: {type(val)}")

def export_acme(voice_name, notes, mapping):
    """
    voice_name: String (z.B. "voice3")
    notes: Liste von (note, dur) Tupeln, note kann z.B. "bd","sd","p" oder "a1","c5" sein
    mapping: dict note->byte (int or hex-string). Muss EintrÃ¤ge fÃ¼r drums/pause enthalten oder es wird 0x00 verwendet.
    """
    print(voice_name)
    line = "    !byte"
    count = 0

    for note, dur in notes:
        note_key = str(note).lower()

        # Drum-Pattern-Expansion
        if note_key == "bd":
            pattern = bd_pattern
        elif note_key == "sd":
            pattern = sd_pattern
        elif note_key == "bdv2":
            pattern = bdv2_pattern
        else:
            raw = mapping.get(note_key, mapping.get(note, 0x00))
            try:
                freq = _normalize_to_byte(raw)
            except Exception as e:
                print(f"Warning: mapping value for {note_key!r} couldn't be parsed: {e}. Using $00.")
                freq = 0x00
            pattern = [(freq, dur)]

        # Ausgabe der Pattern-Elemente
        for freq, d in pattern:
            line += f" ${freq:02X}, ${d:02X}, "
            count += 1
            if count % 8 == 0:
                print(line[:-2])  # letzte ", " entfernen
                line = "    !byte "

    if line.strip() != "!byte":
        print(line[:-2])
    # Endmarker
    print("    !byte $00, $ff\n")

# ---------------------------------------
# Los gehts
# ---------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VC-20 Tetris Player/Exporter")
    parser.add_argument("--play", action="store_true", help="Play the song")
    parser.add_argument("--export", action="store_true", help="Export to ACME format")
    args = parser.parse_args()

    # Default: play, wenn kein Argument angegeben
    if not args.play and not args.export:
        args.play = True

    if args.play:
        #play_three_voices(notes1, notes2, notes3)
        play_with_tracker(notes1, notes2, notes3)
    if args.export:
        export_acme("voice1", notes1, note_to_vic)
        export_acme("voice2", notes2, note_to_vic)
        export_acme("voice3", notes3, note_to_vic)
        export_acme("voice4", notes4, note_to_vic)
