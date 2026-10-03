import os
import subprocess
from pathlib import Path

DEFAULT_SOUNDFONT = Path.home() / "soundfonts" / "GeneralUser-GS.sf2"
SAMPLE_RATE = 44100

def midi_to_wav(midi_path, wav_path, soundfont=None):
  soundfont = soundfont or os.environ.get("SOUNDFONT", DEFAULT_SOUNDFONT)
  if not Path(soundfont).exists():
    raise FileNotFoundError(f"SoundFont not found: {soundfont} (set the SOUNDFONT variable)")

  subprocess.run(
    ["fluidsynth", "-ni", "-q", "-F", str(wav_path), "-r", str(SAMPLE_RATE), str(soundfont), str(midi_path)],
    check=True,
  )
