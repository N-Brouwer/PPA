from PPA.classes import PPAProcess
import csv


class DataExporter:

    def export_data(run_n: int, benchmark_name: str, survivor_selection_name: str, dimensions: int,
                    optimum: float, ppa: PPAProcess, filename: str):
        # we save: best individual during run,
        fields_one = ['run_n', 'selection_method', 'benchmark_name', 'dimensions', 'optimum', 'best_during run']
        data_one = [run_n, survivor_selection_name, benchmark_name, dimensions, optimum, ppa.best_objval_during_run.objective_value]
        with open(filename.replace('.csv', '_performance.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerow(fields_one)
            write.writerow(data_one)

        best_individual_in_generation = ppa.heritage.best_individual_in_generation
        fields_two = ['objective_value', 'generation', 'evaluations']
        with open(filename.replace('.csv', '_performance_over_generations.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerow(fields_two)
            write.writerows(best_individual_in_generation)

        ranks_per_generation = ppa.heritage.ranks_per_generation
        fields_three = ['rank_data']
        with open(filename.replace('.csv', '_fitness_ranks.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerow(fields_three)
            write.writerows(ranks_per_generation)

        unique_individuals = ppa.heritage.unique_individual_count
        fields_four = ['generation','unique_ids']
        with open(filename.replace('.csv', '_unique_individuals.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerow(fields_four)
            write.writerows(unique_individuals)


