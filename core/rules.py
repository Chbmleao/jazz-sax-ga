from core.music import EIGHTHS_PER_BAR, REST, LOWEST_NOTE, HIGHEST_NOTE, JAZZ_AVG_STEPS
from core.music import Note

def get_breathing_score(notes: list[Note], max_phrase_eighths: int) -> float:
  time_playing = 0
  bigger_time_playing = 0
  for note in notes:
    if note.pitch == REST:
      time_playing = 0
      continue

    time_playing += note.length
    bigger_time_playing = max(bigger_time_playing, time_playing)

  if bigger_time_playing <= max_phrase_eighths:
    return 1.0

  overflow = bigger_time_playing - max_phrase_eighths
  max_overflow = sum(note.length for note in notes) - max_phrase_eighths
  return 1 - (overflow / max_overflow)

def get_step_score(notes: list[Note]) -> float:
  total_steps = 0
  for i in range(1, len(notes)):
    previous_pitch = notes[i - 1].pitch
    current_pitch = notes[i].pitch

    if previous_pitch == REST or current_pitch == REST:
      continue

    total_steps += abs(current_pitch - previous_pitch)

  avg_step = total_steps / (len(notes) - 1)
  step_score = max(0, 1 - abs(avg_step - JAZZ_AVG_STEPS) / JAZZ_AVG_STEPS)

  return step_score
