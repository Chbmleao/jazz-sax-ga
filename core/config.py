class Config:
  def __init__(
    self, 
    seed: int = 42, 
    bars: int = 4, 
    population_size: int = 100,
    generations: int = 200,
    elite_size: int = 2,
    mutation_rate: float = 0.05,
    mutation_step: int = 2,
    rest_rate: float = 0.1,
    max_phrase_eights: int = 16,
    weights: tuple = (1, 1, 1, 1, 1),
  ):
    self.seed = seed
    self.bars = bars
    self.population_size = population_size
    self.generations = generations
    self.elite_size = elite_size
    self.mutation_rate = mutation_rate
    self.mutation_step = mutation_step
    self.rest_rate = rest_rate
    self.max_phrase_eights = max_phrase_eights
    self.weights = weights
    self.notes_range = (44, 76)