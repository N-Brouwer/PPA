from operator import attrgetter


# keep track of the number of unique individuals, best individual, and ranks and fitness of each individual per generation
class Heritage:

    def __init__(self):
        self.unique_individual_count = []
        self.best_individual_in_generation = []
        self.ranks_per_generation = []

    # we save the number of distinct individuals by selecting the number of distinct ID's using properties of the
    # "set" collection
    def save_unique_individual_count(self, generation: int, parent_population: []):
        unique_ids = set([individual.id for individual in parent_population])
        self.unique_individual_count.append([generation, len(unique_ids)])

    # we store the whole best individual of a generation, only considering those selected
    def save_best_individual_in_generation(self, parent_population: [], generation: int, evaluations: int):
        best_individual = min(parent_population, key=attrgetter('objective_value'))
        self.best_individual_in_generation.append([best_individual.objective_value, generation, evaluations])

    # save from every individual the rank and fitness value
    # Note: these fitnesses are from the beginning of the generation, before offspring is generated
    def save_fitness_and_rank(self, id_fitness_list: [], generation: int):
        id_fitness_list.sort(key=lambda id_fitness: id_fitness['fitness'], reverse=True)
        rank_counter = 1
        ranks = []
        for id_fitness in id_fitness_list:
            ranks.append({'id': id_fitness['id'], 'rank': rank_counter, 'fitness': id_fitness['fitness'],
                          'generation': generation})
            rank_counter += 1
        self.ranks_per_generation.append(ranks)
