import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

from core import ga
from core.config import Config
from output.audio import midi_to_wav
from output.midi import save_midi

QUARTILES = 4

def history_to_dict(populations):
  return [
    {"notes": list(best.notes), "fitness": best.fitness, "scores": best.scores}
    for best, *_ in populations
  ]

def quartile_generations(total):
  return [total * q // QUARTILES - 1 for q in range(1, QUARTILES + 1)]

def save_json(data, path):
  with open(path, "w") as f:
    json.dump(data, f)

def main():
  name = sys.argv[1] if len(sys.argv) > 1 else "default"
  config = Config()

  run_dir = Path("runs") / name
  run_dir.mkdir(parents=True, exist_ok=True)

  populations = ga.run(config)

  save_json(asdict(config), run_dir / "config.json")
  save_json(history_to_dict(populations), run_dir / "history.json")

  midi_dir = run_dir / "midi"
  audio_dir = run_dir / "audio"
  for directory in (midi_dir, audio_dir):
    shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir()

  for generation in [0, *quartile_generations(len(populations))]:
    file_name = f"gen_{generation:04d}"
    save_midi(populations[generation][0].notes, midi_dir / f"{file_name}.mid")
    midi_to_wav(midi_dir / f"{file_name}.mid", audio_dir / f"{file_name}.wav")

  print(f"saved {len(populations)} generations to {run_dir}")

if __name__ == "__main__":
  main()
