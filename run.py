import json
import sys
from dataclasses import asdict
from pathlib import Path

from core import ga
from core.config import Config

def main():
  name = sys.argv[1] if len(sys.argv) > 1 else "default"
  config = Config()

  run_dir = Path("runs") / name
  run_dir.mkdir(parents=True, exist_ok=True)

  populations = ga.run(config)

  print(f"saved {len(populations)} generations to {run_dir}")

if __name__ == "__main__":
  main()
