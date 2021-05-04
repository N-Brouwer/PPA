# Default PPA settings
pop_size = 30
max_offspring = 5  # n_max

# run settings
max_evaluations = 10_000

# benchmarks
benchmark_name = 'Six Hump Camel'  # Six Hump Camel, Martin-Gaddy

# survivor selection
survivor_selection = 'single_elitist_rws'  # mupluslambda, mulambda, tournament, roulette_wheel, linear_ranking,
                                        # single_elitist_rws
tournament_size = 7

# used for multi processing
all_benchmarks = ['Six Hump Camel','Martin-Gaddy']
all_selection_methods = ['mupluslambda', 'mulambda', 'tournament', 'roulette_wheel', 'linear_ranking', 'single_elitist_rws']