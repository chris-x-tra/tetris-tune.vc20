#!/usr/bin/python
#
#pip install sounddevice numpy

import numpy as np
import sounddevice as sd
import time
import argparse



# notes1 dein ursprÃ¼ngliches BASIC-Listing, das die begleitenden Arpeggios spielt.
# notes2 die Hauptmelodie (Tetris Theme / Korobeiniki).
# notes3 eine tiefe Basslinie, die die Harmonien unterstÃ¼tzt.

# Frequenzen fÃ¼r die wichtigsten Noten
NOTE_FREQUENCIES = {
    "00": 0,
    "c2": 65.41, "c3": 130.81,
    "d2": 73.42, "d3": 146.83,
    "e2": 82.41, "e3": 164.81,
    "f2": 87.31, "f3": 174.61,
    "g1": 49.00, "g2": 98.00, "g4": 392.00,
    "a1": 55.00, "a2": 110.00, "a4": 440.00, "a5": 880.00,
    "h1": 61.74, "h2": 123.47, "h4": 493.88,
    "c5": 523.25, "d5": 587.33, "e5": 659.25,
    "f5": 698.46, "g5": 783.99,
}
note_to_vic = {
    # Voice 1 (low)
    "g1": 0xA7, "a1": 0xB0, "h1": 0xB9,
    "c2": 0xBD, "d2": 0xC4, "e2": 0xCA, "f2": 0xCD,
    "g2": 0xD3, "a2": 0xD8, "h2": 0xDC,
    "c3": 0xDE, "d3": 0xE2, "e3": 0xE5, "f3": 0xE6,

    "p":  0x00,  # Pause

    # Voice 2 (high)
    "c4": 0xDE, "d4": 0xE2, "e4": 0xE5, "f4": 0xE6,
    "g4": 0xEA, "a4": 0xEB, "h4": 0xED,
    "c5": 0xEE, "d5": 0xF0, "e5": 0xF2, "f5": 0xF3,
    "g5": 0xF4, "a5": 0xF5, "h5": 0xF6,
}

# deine Noten jetzt als (note, duration)
notes1 = [
    ("e2",1),("e3",1),("e2",1),("e3",1),("e2",1),("e3",1),("e2",1),("e3",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("d2",1),("d3",1),("d2",1),("d3",1),("d2",1),("d3",1),("d2",1),("d3",1),
    ("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),
    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("g1",1),("g2",1),("g1",1),("g2",1),("g1",1),("g2",1),("g1",1),("g2",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
    ("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),
    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),

#    ("e2",1),("e3",1),("e2",1),("e3",1),("e2",1),("e3",1),("e2",1),("e3",1),
#    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
#    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
#    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
#    ("d2",1),("d3",1),("d2",1),("d3",1),("d2",1),("d3",1),("d2",1),("d3",1),
#    ("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),("c2",1),("c3",1),
#    ("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),("h1",1),("h2",1),
#    ("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),("a1",1),("a2",1),
]
notes2 = [
    ("e5",1),("h4",1),("c5",1),("d5",1),("c5",1),("h4",1),
    ("a4",1),("a4",1),("c5",1),("e5",1),("d5",1),("c5",1),
    ("h4",1),("c5",1),("d5",1),("e5",1),
    ("c5",1),("a4",1),("a4",1),("p",2),
    ("p",1),("d5",1),("f5",1),("a5",1),("g5",1),("f5",1),
    ("e5",1),("c5",1),("e5",1),("d5",1),("c5",1),
    ("h4",1),("c5",1),("d5",1),("e5",1),
    ("c5",1),("a4",1),("a4",1),("p",2),
    ("e5",1),("c5",1),
    ("d5",1),("h4",1),
    ("c5",1),("a4",1),
    ("g4",1),
    ("e5",1),("c5",1),
    ("d5",1),("h4",1),
    ("c5",1),("e5",1),("a5",1),("a5",1),
    ("g5",1),
    ("e5",1),("h4",1),("c5",1),("d5",1),("c5",1),("h4",1),
    ("a4",1),("a4",1),("c5",1),("e5",1),("d5",1),("c5",1),
    ("h4",1),("c5",1),("d5",1),("e5",1),
    ("c5",1),("a4",1),("a4",1),("p",2),
    ("p",1),("d5",1),("f5",1),("a5",1),("g5",1),("f5",1),
    ("p",1),("e5",1),("c5",1),("e5",1),("d5",1),("c5",1),
    ("p",1),("h4",1),("c5",1),("d5",1),("e5",1),
    ("p",1),("c5",1),("a4",1),("a4",1),("p",2),
]

#Hier eine einfache, aber passende Basslinie, die sich an den Akkordwechseln der Melodie orientiert (A-Moll D-Moll G-Dur C-Dur)
#Ich halte sie ruhig im Vierteltakt, damit sie Fundament gibt, aber nicht nervt.
notes3 = [
    # Teil 1 (Am)
    ("a2",1),("a2",1),("a2",1),("a2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Teil 2 (Dm)
    ("d2",1),("d2",1),("d2",1),("d2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Teil 3 (G)
    ("g2",1),("g2",1),("g2",1),("g2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Teil 4 (C)
    ("c2",1),("c2",1),("c2",1),("c2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Wiederholung Am
    ("a2",1),("a2",1),("a2",1),("a2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Wiederholung Dm
    ("d2",1),("d2",1),("d2",1),("d2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Wiederholung G
    ("g2",1),("g2",1),("g2",1),("g2",1),
    ("00",1),("00",1),("00",1),("00",1),

    # Wiederholung C
    ("c2",1),("c2",1),("c2",1),("c2",1),
    ("00",1),("00",1),("00",1),("00",1),
]

def square_wave(frequency, duration, samplerate=44100):
    """Erzeuge Rechteckwelle fÃ¼r eine Frequenz und Dauer."""
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    wave = np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

def note_to_wave(note, duration_units, unit_length=0.25, samplerate=44100):
    """Wandelt eine Note in eine Squarewave um."""
    if note == "p":  # Pause
        return np.zeros(int(samplerate * duration_units * unit_length))
    if note not in NOTE_FREQUENCIES:
        return np.zeros(int(samplerate * duration_units * unit_length))
    freq = NOTE_FREQUENCIES[note]
    dur = duration_units * unit_length
    return square_wave(freq, dur, samplerate)


def play_two_voices(notes1, notes2, unit_length=0.25, samplerate=44100):
    """Spielt zwei Stimmen synchronisiert ab."""
    # LÃ¤nge angleichen (falls eine kÃ¼rzer ist)
    maxlen = max(len(notes1), len(notes2))
    n1 = notes1 + [("p",1)]*(maxlen-len(notes1))
    n2 = notes2 + [("p",1)]*(maxlen-len(notes2))

    full_song = []
    for (note1, dur1), (note2, dur2) in zip(n1, n2):
        dur = max(dur1, dur2)  # gemeinsame Dauer = lÃ¤ngere
        w1 = note_to_wave(note1, dur, unit_length, samplerate)
        w2 = note_to_wave(note2, dur, unit_length, samplerate)
        mix = (w1 + w2) * 0.2  # beide Stimmen summieren, LautstÃ¤rke runter
        full_song.append(mix)

    song = np.concatenate(full_song)
    sd.play(song, samplerate=samplerate)
    sd.wait()

def play_three_voices(notes1, notes2, notes3, unit_length=0.25, samplerate=44100):
    maxlen = max(len(notes1), len(notes2), len(notes3))
    n1 = notes1 + [("p",1)]*(maxlen-len(notes1))
    n2 = notes2 + [("p",1)]*(maxlen-len(notes2))
    n3 = notes3 + [("p",1)]*(maxlen-len(notes3))

    full_song = []
    for (note1, dur1), (note2, dur2), (note3, dur3) in zip(n1, n2, n3):
        dur = max(dur1, dur2, dur3)
        w1 = note_to_wave(note1, dur, unit_length, samplerate)
        w2 = note_to_wave(note2, dur, unit_length, samplerate)
        w3 = note_to_wave(note3, dur, unit_length, samplerate)
        mix = (w1 + w2 + w3) * 0.2
        full_song.append(mix)

    song = np.concatenate(full_song)
    sd.play(song, samplerate=samplerate)
    sd.wait()

def export_hex(notes, note_map):
    out = []
    for note, dur in notes:
        freq = note_map.get(note, 0x00)  # Default: Pause
        out.append((freq, dur))
    return out

voices = {
    "voice1": notes1,  # deine Arpeggio-Stimme
    "voice2": notes2,  # Melodie
    "voice3": notes3,  # Bass
}

def export_acme(voice_name, notes, mapping):
    print(voice_name)
    line = "    !byte"
    for i, (note, dur) in enumerate(notes, 1):
        freq = mapping.get(note, 0x00)
        dur *= 20
        line += f"${freq:02X}, ${dur:02X}, "
        if i % 8 == 0:
            print(line[:-2])  # letzte ", " entfernen
            line = "    !byte "
    if line.strip() != "!byte":
        print(line[:-2])
    line = "    !byte $00, $ff"
    print(line)
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VC-20 Tetris Player/Exporter")
    parser.add_argument("--play", action="store_true", help="Play the song")
    parser.add_argument("--export", action="store_true", help="Export to ACME format")
    args = parser.parse_args()

    # Default: play, wenn kein Argument angegeben
    if not args.play and not args.export:
        args.play = True

    if args.play:
        play_three_voices(notes1, notes2, notes3)
    if args.export:
        export_acme("voice1", notes1, note_to_vic)
        export_acme("voice2", notes2, note_to_vic)
        export_acme("voice3", notes3, note_to_vic)

