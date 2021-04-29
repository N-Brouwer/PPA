from classes.SurvivorSelection import SurvivorSelection
from classes.Benchmark import Benchmark
from classes.PPAProcess import PPAProcess
import config


class run:
    def __init__(self):
        self.survivor_selection = SurvivorSelection(config.survivor_selection, config.pop_size)
        self.benchmark = Benchmark(config.benchmark_name)
        self.run()

    def run(self):
        print('run')
        ppa = PPAProcess(config.pop_size, config.max_offspring, self.benchmark, self.survivor_selection)
        ppa.calculate_objective_values_parents()
        ppa.calculate_fitness_values_parents()
        ppa.generate_offspring()
        ppa.calculate_objective_values_offspring()

        ppa.select_survivors()


start = run()
print('end')
