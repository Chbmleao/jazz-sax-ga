import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

from core import ga
from core.config import Config
from output.audio import midi_to_wav
from output.midi import save_midi

AUDIO_EVERY = 50

def history_to_dict(populations):
  return [
    [
      {"notes": list(ind.notes), "fitness": ind.fitness, "scores": ind.scores}
      for ind in individuals
    ]
    for individuals in populations
  ]

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

  last_generation = len(populations) - 1
  for generation, individuals in enumerate(populations):
    file_name = f"gen_{generation:03d}"
    save_midi(individuals[0].notes, midi_dir / f"{file_name}.mid")
    if generation % AUDIO_EVERY == 0 or generation == last_generation:
      midi_to_wav(midi_dir / f"{file_name}.mid", audio_dir / f"{file_name}.wav")

  print(f"saved {len(populations)} generations to {run_dir}")

if __name__ == "__main__":
  main()
