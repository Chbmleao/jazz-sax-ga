import random

from core.config import Config
from core.music import REST, LOWEST_NOTE, HIGHEST_NOTE, EIGHTHS_PER_BAR

# Reseeded at the start of every run() so the same seed always gives the same run.
rng = random.Random()


class Individual:
  def __init__(self, notes):
    # A tuple so that mutating a child can never alter a genome already saved in the history.
    self.notes = tuple(notes)
    self.fitness = 0

  def evaluate_fitness(self):
    self.fitness = 0
    return self.fitness

def generate_random_notes(bars, rest_rate):
  length = bars * EIGHTHS_PER_BAR
  notes = [
    REST if rng.random() < rest_rate else rng.randint(LOWEST_NOTE, HIGHEST_NOTE)
    for _ in range(length)
  ]
  return notes

def select_elite(individuals, elite_size):
  individuals_sorted = sorted(individuals, key=lambda ind: ind.fitness, reverse=True)
  return individuals_sorted[:elite_size]

def select_parents(individuals):
  weights = [ind.fitness for ind in individuals]
  if sum(weights) == 0:
    return rng.sample(individuals, 2)

  return rng.choices(individuals, weights=weights, k=2)

def crossover(parent1, parent2):
  bars = len(parent1.notes) // EIGHTHS_PER_BAR
  crossover_point = rng.randint(1, bars - 1) * EIGHTHS_PER_BAR
  child_notes_1 = parent1.notes[:crossover_point] + parent2.notes[crossover_point:]
  child_notes_2 = parent2.notes[:crossover_point] + parent1.notes[crossover_point:]
  return Individual(child_notes_1), Individual(child_notes_2)

def mutate(individual, mutation_rate, mutation_step, rest_rate):
  mutated_notes = []
  for note in individual.notes:
    if rng.random() < mutation_rate:
      if rng.random() < rest_rate:
        mutated_notes.append(REST)
      elif note == REST:
        mutated_notes.append(rng.randint(LOWEST_NOTE, HIGHEST_NOTE))
      else:
        new_note = note + rng.randint(-mutation_step, mutation_step)
        mutated_notes.append(max(LOWEST_NOTE, min(HIGHEST_NOTE, new_note)))
    else:
      mutated_notes.append(note)

  return Individual(mutated_notes)

def run(config: Config):
  rng.seed(config.seed)
  populations = []

  individuals = [
    Individual(generate_random_notes(config.bars, config.rest_rate))
    for _ in range(config.population_size)
  ]

  for _ in range(config.generations):
    for individual in individuals:
      individual.evaluate_fitness()

    individuals = sorted(individuals, key=lambda ind: ind.fitness, reverse=True)
    populations.append(individuals)

    elite_individuals = select_elite(individuals, config.elite_size)

    new_population = elite_individuals.copy()
    while len(new_population) < config.population_size:
      parent1, parent2 = select_parents(individuals)
      child1, child2 = crossover(parent1, parent2)

      child1 = mutate(child1, config.mutation_rate, config.mutation_step, config.rest_rate)
      child2 = mutate(child2, config.mutation_rate, config.mutation_step, config.rest_rate)

      new_population.append(child1)
      new_population.append(child2)

    individuals = new_population[:config.population_size]

  return populations
