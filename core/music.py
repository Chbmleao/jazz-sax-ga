REST = 43
LOWEST_NOTE = 44
HIGHEST_NOTE = 76
HOLD = HIGHEST_NOTE + 1
EIGHTHS_PER_BAR = 8
JAZZ_AVG_STEPS = 2.7
LEAP_SIZE = 7
JAZZ_LEAP_SHARE = 0.02

SCALE = {0, 2, 4, 5, 7, 9, 11}

CHORDS = [
  {2, 5, 9, 0},   # Dm7:   D F A C
  {7, 11, 2, 5},  # G7:    G B D F
  {0, 4, 7, 11},  # Cmaj7: C E G B
  {0, 4, 7, 11},  # Cmaj7
]

GUIDE_TONES = [
  {5, 0},   # Dm7:   F C
  {11, 5},  # G7:    B F
  {4, 11},  # Cmaj7: E B
  {4, 11},  # Cmaj7
]

class Note():
  def __init__(self, pitch, start, length):
    self.pitch = pitch
    self.start = start
    self.length = length

def decode(raw_notes, merge_repeats=True):
  notes = []

  for position, raw in enumerate(raw_notes):
    pitch = raw
    if raw == HOLD:
      pitch = notes[-1].pitch if notes else REST

    extends_previous = (
      notes
      and position % EIGHTHS_PER_BAR != 0
      and (raw == HOLD or (pitch == notes[-1].pitch and (merge_repeats or pitch == REST)))
    )
    if extends_previous:
      notes[-1].length += 1
    else:
      notes.append(Note(pitch, position, 1))

  return notes