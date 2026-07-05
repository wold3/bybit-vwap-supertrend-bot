import random
import copy

class GeneticOptimizer:

    def __init__(self):

        self.population = [
            {"rsi": 14, "tp": 1.02, "sl": 0.99, "fitness": 0},
            {"rsi": 10, "tp": 1.03, "sl": 0.98, "fitness": 0},
            {"rsi": 20, "tp": 1.01, "sl": 0.97, "fitness": 0},
        ]

    def evaluate(self, score, idx):
        self.population[idx]["fitness"] = score

    def select(self):
        self.population.sort(key=lambda x: x["fitness"], reverse=True)
        return self.population[:2]

    def mutate(self, parent):
        child = copy.deepcopy(parent)

        child["rsi"] += random.randint(-2, 2)
        child["tp"] += random.uniform(-0.01, 0.01)
        child["sl"] += random.uniform(-0.01, 0.01)

        child["fitness"] = 0
        return child

    def next_generation(self):

        parents = self.select()

        new_pop = parents.copy()

        while len(new_pop) < len(self.population):
            p = random.choice(parents)
            new_pop.append(self.mutate(p))

        self.population = new_pop


optimizer = GeneticOptimizer()
