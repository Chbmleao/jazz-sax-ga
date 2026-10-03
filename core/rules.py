from core.music import EIGHTHS_PER_BAR, REST, LOWEST_NOTE, HIGHEST_NOTE, JAZZ_AVG_STEPS, LEAP_SIZE, JAZZ_LEAP_SHARE, CHORDS, SCALE, GUIDE_TONES
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
  step_count = 0
  total_distance = 0
  total_leaps = 0
  for i in range(1, len(notes)):
    previous_pitch = notes[i - 1].pitch
    current_pitch = notes[i].pitch

    if previous_pitch == REST or current_pitch == REST or current_pitch == previous_pitch:
      continue

    distance = abs(current_pitch - previous_pitch)
    step_count += 1
    total_distance += distance
    if distance > LEAP_SIZE:
      total_leaps += 1

  if step_count == 0:
    return 1.0

  avg_step = total_distance / step_count
  step_score = max(0, 1 - abs(avg_step - JAZZ_AVG_STEPS) / JAZZ_AVG_STEPS)

  leap_share = total_leaps / step_count
  leap_score = 1 - max(0, leap_share - JAZZ_LEAP_SHARE) / (1 - JAZZ_LEAP_SHARE)

  return (step_score + leap_score) / 2

def get_chord_tone_score(notes: list[Note]) -> float:
  beats = 0
  hits = 0
  for note in notes:
    if note.pitch == REST:
      continue

    for position in range(note.start, note.start + note.length):
      if position % 2 != 0:
        continue

      chord = CHORDS[(position // EIGHTHS_PER_BAR) % len(CHORDS)]
      beats += 1
      if note.pitch % 12 in chord:
        hits += 1

  if beats == 0:
    return 0.0

  return hits / beats

def get_chromatic_score(notes: list[Note]) -> float:
  outside = 0
  correct = 0
  for i in range(len(notes)):
    note = notes[i]
    if note.pitch == REST or note.pitch % 12 in SCALE:
      continue

    outside += 1
    if i + 1 >= len(notes):
      continue

    next_pitch = notes[i + 1].pitch
    if next_pitch != REST and note.start % 2 == 1 and abs(next_pitch - note.pitch) == 1:
      correct += 1

  if outside == 0:
    return 1.0

  return correct / outside

def get_guide_tone_score(notes: list[Note]) -> float:
  changes = 0
  hits = 0
  for note in notes:
    if note.start % EIGHTHS_PER_BAR != 0:
      continue

    bar = note.start // EIGHTHS_PER_BAR
    if bar == 0 or CHORDS[bar % len(CHORDS)] == CHORDS[(bar - 1) % len(CHORDS)]:
      continue

    changes += 1
    if note.pitch != REST and note.pitch % 12 in GUIDE_TONES[bar % len(GUIDE_TONES)]:
      hits += 1

  if changes == 0:
    return 1.0

  return hits / changes
