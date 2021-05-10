import concurrent.futures
from datetime import datetime
import pickle
import time
from operator import attrgetter

from pathlib import Path

from PPA.classes.Heritage import Heritage
from PPA.classes.SurvivorSelection import SurvivorSelection
from PPA.classes.Benchmark import Benchmark
from PPA.classes.PPAProcess import PPAProcess
import PPA.config as config


class run:
    def __init__(self, benchmark_name: str, survivor_selection: str, run_n: int, file_name=""):
        self.survivor_selection = SurvivorSelection(survivor_selection, config.pop_size)
        self.benchmark = Benchmark(benchmark_name)
        self.heritage = Heritage()
        self.file_name = file_name
        self.benchmark_name = benchmark_name
        self.survivor_selection_name = survivor_selection
        self.run_n = run_n

    def run(self):

        ppa = PPAProcess(config.pop_size, config.max_offspring, self.benchmark, self.survivor_selection, self.heritage)
        ppa.calculate_objective_values_parents()
        ppa.save_heritage()

        while ppa.benchmark.eval_counter < config.max_evaluations:
            ppa.generation += 1
            ppa.normalize_objective_values_parents()
            ppa.calculate_fitness_values_parents()
            ppa.generate_offspring()

            ppa.normalize_objective_values_offspring()
            ppa.select_survivors()
            ppa.save_heritage()

        if self.file_name != "":
            # storing data so it can be retrieved easier in the data analytics part
            ppa.run_n = self.run_n
            ppa.benchmark_name = self.benchmark_name
            ppa.survivor_selection_name = self.survivor_selection_name

            pickle.dump(ppa, open(self.file_name, "wb"))
        return ppa


# start = run(config.benchmark_name, config.survivor_selection, 0, "results/test/mc-test.p")
# results = start.run()
# best = min(results.parent_population, key=attrgetter('objective_value'))
# print(str(best.objective_value).replace('.', ','))
# print('done')
i = 1
for b in config.all_benchmarks:
    if b in config.n_dim_benchmarks:
        print(b)
        print(i)
        i+=1



# if __name__ == '__main__':
#     print('starting')
#     start_time = time.time()
#     folder_path = f"results/results-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
#     Path(folder_path).mkdir(parents=False, exist_ok=False)
#     processes = []
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         for run_n in range(10):
#             for benchmark in config.all_benchmarks:
#                 for selection_method in config.all_selection_methods:
#                     save_path = folder_path + "/" + str(selection_method + "-" + benchmark) + f"run-{run_n}.p"
#                     ppa_class = run(benchmark, selection_method, run_n, save_path)
#                     executor.submit(ppa_class.run)
#
#     end_time = time.time()
#
#     print(f'done: {end_time - start_time}')