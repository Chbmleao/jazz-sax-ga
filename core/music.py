REST = 43
LOWEST_NOTE = 44
HIGHEST_NOTE = 76
EIGHTHS_PER_BAR = 8
JAZZ_AVG_STEPS = 2.7

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