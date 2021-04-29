import random

from classes.SurvivorSelection import SurvivorSelection
from classes.Benchmark import Benchmark
from classes.Individual import Individual
import config


class run:
    def __init__(self):
        self.parent_population = []

        self.survivor_selection = SurvivorSelection(config.survivor_selection)
        self.benchmark = Benchmark(config.benchmark_name)
        self.parent_population = self.initial_generate_parents(config.pop_size, self.benchmark)
        self.run()

    def run(self):
        print('run')

    def initial_generate_parents(self, pop_size: int, benchmark: Benchmark):
        parents = []
        self.parent_population = []
        for i in range(0, pop_size):
            x = Individual()
            inputs = []
            for d in range(0, benchmark.input_dimension):
                bound = benchmark.bounds[d]
                inputs.append(random.uniform(bound[0], bound[1]))
            x.set_inputs(inputs)
            x.calculate_fitness(benchmark)
            parents.append(x)

        return parents


start = run()
print('end')
