#!/usr/bin/env bash
set -euo pipefail

pids=()

for mutation_rate in 0.01 0.05 0.2; do
  for seed in 1 2 3; do
    python run.py "experiments/mutation_${mutation_rate}_seed_${seed}" \
      --mutation-rate "$mutation_rate" --seed "$seed" &
    pids+=($!)
  done
done

for pid in "${pids[@]}"; do
  wait "$pid"
done
