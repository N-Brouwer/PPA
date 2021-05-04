import concurrent.futures
import pickle
from operator import attrgetter
import multiprocessing

from classes.Heritage import Heritage
from classes.SurvivorSelection import SurvivorSelection
from classes.Benchmark import Benchmark
from classes.PPAProcess import PPAProcess
import config


class run:
    def __init__(self, benchmark_name: str, survivor_selection: str):
        self.survivor_selection = SurvivorSelection(survivor_selection, config.pop_size)
        self.benchmark = Benchmark(benchmark_name)
        self.heritage = Heritage()
        self.btest = benchmark_name
        self.stest = survivor_selection
        print('ja')

    def run(self):
        # print('run')
        ppa = PPAProcess(config.pop_size, config.max_offspring, self.benchmark, self.survivor_selection, self.heritage)
        ppa.calculate_objective_values_parents()
        ppa.save_heritage()
        # loop start
        print('ja 2')
        while ppa.benchmark.eval_counter < config.max_evaluations:
            ppa.generation += 1
            ppa.normalize_objective_values_parents()
            ppa.calculate_fitness_values_parents()
            ppa.generate_offspring()

            # ppa.calculate_objective_values_offspring()
            ppa.normalize_objective_values_offspring()
            ppa.select_survivors()
            ppa.save_heritage()
            # if not ppa.generation % 1000:
            # print('another 1000 generations')

        print(f'finished {self.btest} with {self.stest}')

        return ppa


# for i in range(10):
#     start = run(config.benchmark_name, config.survivor_selection)
#     results = start.run()
#     best = min(results.parent_population, key=attrgetter('objective_value'))
#     print(str(best.objective_value).replace('.', ','))
#     print('next')
# print('end')


if __name__ == '__main__':
    processes = []
    for benchmark in config.all_benchmarks:
        for selection_method in config.all_selection_methods:
            ppa = run(benchmark, selection_method)
            p = multiprocessing.Process(target=ppa.run)
            p.start()
            processes.append(p)

    for process in processes:
        process.join()

    print('done')
