# Default PPA settings
pop_size = 30
max_offspring = 5  # n_max

# run settings
max_evaluations = 10_000

# benchmarks
benchmark_name = 'Tablet'  # Six Hump Camel, Martin-Gaddy

# survivor selection
survivor_selection = 'tournament'  # mupluslambda, mulambda, tournament, roulette_wheel, linear_ranking,
# single_elitist_rws
tournament_size = 7

# used for multi processing
all_benchmarks = ['Six-Hump-Camel', 'Martin-Gaddy', 'Goldstein-Price', 'Branin', 'Easom', 'Rosenbrock', 'Ackley',
                  'Griewank', 'Rastrigrin', 'Schwefel', 'Ellipse', 'Cigar', 'Tablet', 'Sphere']

all_selection_methods = ['mupluslambda', 'mulambda', 'tournament', 'roulette_wheel', 'linear_ranking',
                         'single_elitist_rws', 'single_elitist_tournament', 'no_replacement_tournament']

record_heritage_selection_methods = ['mupluslambda', 'tournament', 'single_elitist_tournament','no_replacement_tournament']

n_dim_benchmarks = ['Ackley', 'Rosenbrock', 'Griewank', 'Rastrigrin', 'Schwefel', 'Ellipse', 'Cigar', 'Tablet',
                    'Sphere']
n_dimensions = [2, 5, 10, 20, 50, 100]
