import random

from core.config import Config
from core.music import REST, HOLD, LOWEST_NOTE, HIGHEST_NOTE, EIGHTHS_PER_BAR
from core.music import decode, Note
from core.rules import get_breathing_score, get_step_score, get_chord_tone_score, get_chromatic_score, get_guide_tone_score

rng = random.Random()
config = Config()

class Individual:
  def __init__(self, notes):
    self.notes = tuple(notes)
    self.fitness = 0
    self.scores = [0, 0, 0, 0, 0]

  def evaluate_fitness(self):
    notes = decode(self.notes, config.merge_repeats)

    self.scores = [
      get_breathing_score(notes, config.max_phrase_eighths),
      get_step_score(notes),
      get_chord_tone_score(notes),
      get_chromatic_score(notes),
      get_guide_tone_score(notes)
    ]

    total_score = sum(score * weight for score, weight in zip(self.scores, config.weights))
    self.fitness = total_score / sum(config.weights)
    return self.fitness

def generate_random_notes(bars, rest_rate, hold_rate, walk_step):
  length = bars * EIGHTHS_PER_BAR
  pitch = rng.randint(LOWEST_NOTE, HIGHEST_NOTE)
  notes = []
  for _ in range(length):
    roll = rng.random()
    if roll < rest_rate:
      notes.append(REST)
      continue
    if roll < rest_rate + hold_rate:
      notes.append(HOLD)
      continue
    pitch = max(LOWEST_NOTE, min(HIGHEST_NOTE, pitch + rng.randint(-walk_step, walk_step)))
    notes.append(pitch)
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

def mutate(individual, mutation_rate, mutation_step, rest_rate, hold_rate):
  mutated_notes = []
  for note in individual.notes:
    if rng.random() < mutation_rate:
      roll = rng.random()
      if roll < rest_rate:
        mutated_notes.append(REST)
      elif roll < rest_rate + hold_rate:
        mutated_notes.append(HOLD)
      elif note in (REST, HOLD):
        mutated_notes.append(rng.randint(LOWEST_NOTE, HIGHEST_NOTE))
      else:
        new_note = note + rng.randint(-mutation_step, mutation_step)
        mutated_notes.append(max(LOWEST_NOTE, min(HIGHEST_NOTE, new_note)))
    else:
      mutated_notes.append(note)

  return Individual(mutated_notes)

def run(new_config: Config):
  global config
  config = new_config
  rng.seed(config.seed)
  populations = []

  individuals = [
    Individual(generate_random_notes(config.bars, config.rest_rate, config.hold_rate, config.walk_step))
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

      child1 = mutate(child1, config.mutation_rate, config.mutation_step, config.rest_rate, config.hold_rate)
      child2 = mutate(child2, config.mutation_rate, config.mutation_step, config.rest_rate, config.hold_rate)

      new_population.append(child1)
      new_population.append(child2)

    individuals = new_population[:config.population_size]

  return populations
