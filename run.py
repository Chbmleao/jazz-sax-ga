import json
import sys
from dataclasses import asdict
from pathlib import Path

from core import ga
from core.config import Config

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
  print(f"saved {len(populations)} generations to {run_dir}")

if __name__ == "__main__":
  main()
