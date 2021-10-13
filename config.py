# Default PPA settings
pop_size = 30
max_offspring = 5  # n_max

# run settings
max_evaluations = 50_000

# the size of tournaments used in the tournament selection methods
tournament_size = 7

# ==================
# Used for a single run
# ==================
# benchmarks
benchmark_name = 'Rosenbrock'  # Six Hump Camel, Martin-Gaddy

# survivor selection
survivor_selection = 'single_elitist_tournament'  # mupluslambda, mulambda, tournament, roulette_wheel, linear_ranking,

# ==================
# used for multi processing numerous runs
all_benchmarks = ['Six-Hump-Camel', 'Martin-Gaddy', 'Goldstein-Price', 'Branin', 'Easom', 'Rosenbrock', 'Ackley',
                  'Griewank', 'Rastrigrin', 'Schwefel', 'Ellipse', 'Cigar', 'Tablet', 'Sphere']

all_selection_methods = ['mupluslambda', 'mulambda', 'tournament', 'roulette_wheel', 'linear_ranking',
                         'single_elitist_rws', 'single_elitist_tournament', 'no_replacement_tournament']

n_dim_benchmarks = ['Ackley', 'Rosenbrock', 'Griewank', 'Rastrigrin', 'Schwefel', 'Ellipse', 'Cigar', 'Tablet',
                    'Sphere']
n_dimensions = [2, 5, 10, 20, 50, 100]

