import argparse
import json
import shutil
from dataclasses import asdict, fields, replace
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

def parse_args():
  parser = argparse.ArgumentParser(description="Evolve a jazz tenor sax melody with a genetic algorithm.")
  parser.add_argument("name", nargs="?", default="default", help="output folder inside runs/")
  default_config = Config()
  for field in fields(Config):
    flag = "--" + field.name.replace("_", "-")
    default = getattr(default_config, field.name)
    if field.name == "weights":
      parser.add_argument(flag, type=float, nargs=len(default), help=f"rule weights (default: {' '.join(map(str, default))})")
    else:
      parser.add_argument(flag, type=field.type, help=f"default: {default}")
  return parser.parse_args()

def build_config(args):
  overrides = {
    field.name: getattr(args, field.name)
    for field in fields(Config)
    if getattr(args, field.name) is not None
  }
  if "weights" in overrides:
    overrides["weights"] = tuple(overrides["weights"])
  return replace(Config(), **overrides)

def main():
  args = parse_args()
  name = args.name
  config = build_config(args)

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
