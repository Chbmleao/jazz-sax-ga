import random

from core.config import Config

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
  pass

def select_elite(individuals, elite_size):
  pass

def select_parents(individuals):
  pass

def crossover(parent1, parent2):
  pass

def mutate(individual, mutation_rate, mutation_step):
  pass

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

    populations.append(individuals)

    elite_individuals = select_elite(individuals, config.elite_size)

    new_population = elite_individuals.copy()
    while len(new_population) < config.population_size:
      parent1, parent2 = select_parents(individuals)
      child = crossover(parent1, parent2)
      child = mutate(child, config.mutation_rate, config.mutation_step)
      new_population.append(child)

    individuals = new_population

  return populations
