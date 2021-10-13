import concurrent.futures
from datetime import datetime
import pickle
import time
from operator import attrgetter
from pathlib import Path

from PPA.classes.DataExporter import DataExporter
from PPA.classes.Heritage import Heritage
from PPA.classes.SurvivorSelection import SurvivorSelection
from PPA.classes.Benchmark import Benchmark
from PPA.classes.PPAProcess import PPAProcess
import PPA.config as config


class run:
    # we start a new run and set some properties for this run specific
    def __init__(self, benchmark_name: str, benchmark_dim: int, survivor_selection: str, run_n: int, file_name=""):
        self.survivor_selection = SurvivorSelection(survivor_selection, config.pop_size)
        self.benchmark = Benchmark(benchmark_name, benchmark_dim)
        self.heritage = Heritage()
        self.file_name = file_name
        self.benchmark_name = benchmark_name
        self.survivor_selection_name = survivor_selection
        self.run_n = run_n

    # Here the run actually starts, we first initialize the first population, next we start looping until we have
    # surpassed our maximum number of evaluations
    def run(self):

        ppa = PPAProcess(config.pop_size, config.max_offspring, self.benchmark, self.survivor_selection, self.heritage)
        # when the PPA process is initialized, in the init, we initialize the first population, next, the rest of the ppa process follows
        ppa.calculate_objective_values_parents()
        ppa.normalize_objective_values_parents()
        ppa.calculate_fitness_values_parents()
        ppa.save_heritage()

        # The while loop follows the PPA process while keeping track of the generations and some heritage data
        while ppa.benchmark.eval_counter < config.max_evaluations:
            ppa.generation += 1
            ppa.normalize_objective_values_parents()
            ppa.calculate_fitness_values_parents()
            ppa.generate_offspring()
            ppa.select_survivors()

            ppa.save_heritage()

        # If no filename is specified we assume a test run, therefore we do not export all data as it takes much time
        if self.file_name != "":
            # storing data so it can be retrieved easier in the data analytics part
            DataExporter.export_data(self.run_n, self.benchmark_name,self.survivor_selection_name, self.benchmark.input_dimension, self.benchmark.optimum, ppa, self.file_name)

        return ppa


#  Deselect the part until print('done') in order to perform one run specified
# ============================================================
# benchmark_dimensions = 100
# start = run(config.benchmark_name, benchmark_dimensions, config.survivor_selection, 0, "results/test/test.csv")
# results = start.run()
# best_final_pop = min(results.parent_population, key=attrgetter('objective_value'))
# print(str(best_final_pop.objective_value).replace('.', ','))
#
# print('done')


# Run this in order to reproduce the full experiments, note: will run for long time
# ============================================================
if __name__ == '__main__':

    print('starting')
    start_time = time.time()
    # create a new "unique" folder for this run
    folder_path = f"results/results-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    Path(folder_path).mkdir(parents=False, exist_ok=False)

    # we now start with multiprocessing, this speeds up the whole experiment significantly, each run get assigned
    # a new process, next we loop through each benchmark, dimension, and selection method and perform the experiment
    processes = []
    with concurrent.futures.ProcessPoolExecutor() as executor:  # max_workers=6
        for run_n in range(15):
            print(f'run {run_n}')
            for benchmark in config.all_benchmarks:
                for selection_method in config.all_selection_methods:

                    # we make a distinction between n-dim and 2-dim benchmarks so we don't run the 2-dim with all dimensions
                    if benchmark in config.n_dim_benchmarks:
                        for dim in config.n_dimensions:
                            save_path = folder_path + "/" + str(
                                selection_method + "-" + benchmark + f"{dim}D") + f"run-{run_n}.csv"
                            ppa_class = run(benchmark, dim, selection_method, run_n, save_path)
                            executor.submit(ppa_class.run)
                    else:
                        dim = 2
                        save_path = folder_path + "/" + str(selection_method + "-" + benchmark) + f"run-{run_n}.csv"
                        ppa_class = run(benchmark, dim, selection_method, run_n, save_path)
                        executor.submit(ppa_class.run)

    end_time = time.time()

    print(f'done: {end_time - start_time}')
