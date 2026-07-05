import copy
import random


class GeneticOptimizer:
    """
    Genetic Algorithm Optimizer
    """

    def __init__(self, population_size=20):

        self.population_size = population_size

        self.generation = 1

        self.population = []

        self.initialize()

    # ------------------------------------------------

    def initialize(self):

        self.population = []

        for _ in range(self.population_size):

            self.population.append({

                "rsi": random.randint(8, 25),

                "tp": round(random.uniform(1.01, 1.05), 3),

                "sl": round(random.uniform(0.95, 0.99), 3),

                "fitness": 0.0,

            })

    # ------------------------------------------------

    def evaluate(self, score, idx):

        self.population[idx]["fitness"] = float(score)

    # ------------------------------------------------

    def select(self, elite=4):

        self.population.sort(
            key=lambda x: x["fitness"],
            reverse=True,
        )

        return self.population[:elite]

    # ------------------------------------------------

    def crossover(self, parent1, parent2):

        child = {

            "rsi": random.choice(
                [parent1["rsi"], parent2["rsi"]]
            ),

            "tp": random.choice(
                [parent1["tp"], parent2["tp"]]
            ),

            "sl": random.choice(
                [parent1["sl"], parent2["sl"]]
            ),

            "fitness": 0.0,

        }

        return child

    # ------------------------------------------------

    def mutate(self, child):

        child = copy.deepcopy(child)

        if random.random() < 0.5:

            child["rsi"] += random.randint(-2, 2)

        if random.random() < 0.5:

            child["tp"] += random.uniform(-0.005, 0.005)

        if random.random() < 0.5:

            child["sl"] += random.uniform(-0.005, 0.005)

        child["rsi"] = max(
            5,
            min(30, child["rsi"])
        )

        child["tp"] = round(
            max(1.005, min(1.10, child["tp"])),
            3,
        )

        child["sl"] = round(
            max(0.90, min(0.995, child["sl"])),
            3,
        )

        child["fitness"] = 0.0

        return child

    # ------------------------------------------------

    def next_generation(self):

        elites = self.select()

        new_population = copy.deepcopy(elites)

        while len(new_population) < self.population_size:

            p1 = random.choice(elites)

            p2 = random.choice(elites)

            child = self.crossover(
                p1,
                p2,
            )

            child = self.mutate(child)

            new_population.append(child)

        self.population = new_population

        self.generation += 1

    # ------------------------------------------------

    def best(self):

        self.population.sort(
            key=lambda x: x["fitness"],
            reverse=True,
        )

        return self.population[0]

    # ------------------------------------------------

    def summary(self):

        best = self.best()

        return {

            "generation": self.generation,

            "population": len(self.population),

            "best_fitness": best["fitness"],

            "best": best,

        }


optimizer = GeneticOptimizer()
