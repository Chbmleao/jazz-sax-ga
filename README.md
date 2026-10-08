# Genetic Algorith for Jazz Music

A genetic algorithm that composes a 12-bar jazz tenor sax melody over a ii-V-I loop in C major (Dm7 | G7 | Cmaj7 | Cmaj7). 

The fitness is a weighted mean of five rules: breathing, step size, chord tones on strong beats, chromatic approach notes and guide tones. The output is MIDI and WAV (tenor sax plus piano chords, swing applied at playback).

## Install

Tested on macOS with Python 3 from Homebrew.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install fluid-synth
```

## Run

```bash
python run.py my_run
python run.py my_run --seed 7 --mutation-rate 0.1
python run.py --help
```

Every option in `core/config.py` can be overridden from the command line. Each run writes to
`runs/<name>/`:

| File | Content |
|------|---------|
| `config.json` | Config used |
| `history.json` | Best individual and mean fitness of each generation |
| `fitness.png` | Best and mean fitness per generation |
| `midi/`, `audio/` | Best melody at generations 0, 999, 1999, 2999 and 3999 |

## Reproduce the experiments

```bash
./experiments.sh
python compare.py
```

`experiments.sh` runs 9 full runs in parallel: mutation rate 0.01, 0.05 and 0.2, each with seeds 1, 2 and 3. `compare.py` then plots the best fitness per generation, averaged over the seeds, for each mutation rate (`runs/experiments/comparison.png`).

The repository keeps the config, fitness graph, MIDI files and final WAV of every experiment in `runs/experiments/`. The `history.json` files (about 2 MB each) are not committed, so run `./experiments.sh` again before `compare.py`. Runs are deterministic for a given config.
