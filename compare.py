import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

EXPERIMENTS_DIR = Path("runs") / "experiments"
RUN_NAME = re.compile(r"mutation_(?P<rate>[\d.]+)_seed_\d+")

def load_best_fitness_by_rate():
  runs = defaultdict(list)
  for run_dir in sorted(EXPERIMENTS_DIR.iterdir()):
    match = RUN_NAME.fullmatch(run_dir.name)
    if not match:
      continue
    history = json.loads((run_dir / "history.json").read_text())
    runs[float(match["rate"])].append([entry["fitness"] for entry in history])
  return runs

def average(curves):
  return [sum(values) / len(values) for values in zip(*curves)]

def main():
  runs = load_best_fitness_by_rate()

  fig, ax = plt.subplots(figsize=(6, 3.5))
  for rate in sorted(runs):
    curves = runs[rate]
    ax.plot(average(curves), label=f"mutation rate {rate} ({len(curves)} seeds)")
  ax.set_xlabel("Generation")
  ax.set_ylabel("Best fitness (mean over seeds)")
  ax.set_ylim(0, 1)
  ax.grid(alpha=0.3)
  ax.legend(loc="lower right")
  fig.tight_layout()
  path = EXPERIMENTS_DIR / "comparison.png"
  fig.savefig(path, dpi=200)
  plt.close(fig)
  print(f"saved {path}")

if __name__ == "__main__":
  main()
