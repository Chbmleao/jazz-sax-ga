from core.music import EIGHTHS_PER_BAR, REST, LOWEST_NOTE, HIGHEST_NOTE
from core.music import Note

def get_breathing_score(notes: list[Note], max_phrase_eighths: int):
  time_playing = 0
  bigger_time_playing = 0
  for note in notes:
    if note.pitch == REST:
      time_playing = 0
      continue

    time_playing += note.length
    bigger_time_playing = max(bigger_time_playing, time_playing)

  if bigger_time_playing <= max_phrase_eighths:
    return 1

  overflow = bigger_time_playing - max_phrase_eighths
  max_overflow = sum(note.length for note in notes) - max_phrase_eighths
  return 1 - (overflow / max_overflow)

