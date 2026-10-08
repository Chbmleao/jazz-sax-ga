import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

def plot_fitness(history, path):
  generations = range(len(history))
  best = [entry["fitness"] for entry in history]
  mean = [entry["mean_fitness"] for entry in history]

  fig, ax = plt.subplots(figsize=(6, 3.5))
  ax.plot(generations, best, label="Best")
  ax.plot(generations, mean, label="Mean")
  ax.set_xlabel("Generation")
  ax.set_ylabel("Fitness")
  ax.set_ylim(0, 1)
  ax.grid(alpha=0.3)
  ax.legend()
  fig.tight_layout()
  fig.savefig(path, dpi=200)
  plt.close(fig)
