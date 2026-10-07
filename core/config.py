from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
  seed: int = 42
  bars: int = 12
  population_size: int = 100
  generations: int = 4000
  elite_size: int = 2
  mutation_rate: float = 0.05
  mutation_step: int = 2
  rest_rate: float = 0.1
  walk_step: int = 3
  max_phrase_eighths: int = 16
  weights: tuple = (1, 1, 1, 1, 1)
