REST = 43
LOWEST_NOTE = 44
HIGHEST_NOTE = 76
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

class Note():
  def __init__(self, pitch, start, length):
    self.pitch = pitch
    self.start = start
    self.length = length

def decode(raw_notes):
  notes = []
  start = 0

  i = 0
  while i < len(raw_notes):
    pitch = raw_notes[i]
    length = 1

    while (
      i+1 < len(raw_notes)
      and (raw_notes[i+1] == pitch)
      and ((i + 1) % EIGHTHS_PER_BAR != 0)
    ):
      length += 1
      i += 1

    notes.append(Note(pitch, start, length))
    start += length
    i += 1

  return notes