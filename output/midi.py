import pretty_midi

from core.music import REST, EIGHTHS_PER_BAR, decode

# One voicing per bar, same order as CHORDS in core/music.py
CHORD_VOICINGS = [
  [50, 53, 57, 60],  # Dm7:   D3 F3 A3 C4
  [55, 59, 62, 65],  # G7:    G3 B3 D4 F4
  [48, 52, 55, 59],  # Cmaj7: C3 E3 G3 B3
  [48, 52, 55, 59],  # Cmaj7
]

SAX_PROGRAM = pretty_midi.instrument_name_to_program("Tenor Sax")
PIANO_PROGRAM = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")

def position_to_seconds(position, tempo_bpm, swing_ratio):
  beat_seconds = 60 / tempo_bpm
  beat = position // 2
  seconds = beat * beat_seconds
  if position % 2 == 1:
    seconds += beat_seconds * swing_ratio / (1 + swing_ratio)
  return seconds

def genome_to_midi(genome, tempo_bpm=170, swing_ratio=1.3):
  midi = pretty_midi.PrettyMIDI(initial_tempo=tempo_bpm)
  sax = pretty_midi.Instrument(program=SAX_PROGRAM, name="Tenor Sax")
  piano = pretty_midi.Instrument(program=PIANO_PROGRAM, name="Piano")

  for note in decode(genome):
    if note.pitch == REST:
      continue
    start = position_to_seconds(note.start, tempo_bpm, swing_ratio)
    end = position_to_seconds(note.start + note.length, tempo_bpm, swing_ratio)
    sax.notes.append(pretty_midi.Note(velocity=100, pitch=note.pitch, start=start, end=end))

  bars = len(genome) // EIGHTHS_PER_BAR
  for bar in range(bars):
    start = position_to_seconds(bar * EIGHTHS_PER_BAR, tempo_bpm, swing_ratio)
    end = position_to_seconds((bar + 1) * EIGHTHS_PER_BAR, tempo_bpm, swing_ratio)
    for pitch in CHORD_VOICINGS[bar % len(CHORD_VOICINGS)]:
      piano.notes.append(pretty_midi.Note(velocity=60, pitch=pitch, start=start, end=end))

  midi.instruments.append(sax)
  midi.instruments.append(piano)
  return midi

def save_midi(genome, path, tempo_bpm=170, swing_ratio=1.3):
  genome_to_midi(genome, tempo_bpm, swing_ratio).write(str(path))
