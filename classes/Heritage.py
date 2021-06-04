from operator import attrgetter


class Heritage:

    def __init__(self):
        # self.ancestors = {}
        self.relations = []
        self.unique_individual_count = []
        self.ages_per_generation = {}
        self.best_individual_in_generation = []
        self.ranks_per_generation = []
        self.offspring_per_generation = []

    # def add_ancestors(self, population: [], generation: int):
    #     for i in population:
    #         if i.id not in self.ancestors:
    #             self.ancestors.update(
    #                 {i.id: {'id': i.id, 'obj_values': i.objective_value, 'inputs': i.inputs, 'parents': i.parents,
    #                         'generation': generation}})
    def save_offspring_count(self, offspring: [], generation: int):
        self.offspring_per_generation.append({'generation': generation, 'offspring_len': len(offspring)})

    def save_relation(self, child_id: int, parent_id: int, generation: int):
        self.relations.append([child_id, parent_id, generation])

    def save_unique_individual_count(self, generation: int, parent_population: []):
        unique_ids = set([individual.id for individual in parent_population])
        self.unique_individual_count.append([generation, len(unique_ids)])

    def save_ages(self, generation: int, parent_population: []):
        ages = [individual.age for individual in parent_population]
        self.ages_per_generation[generation] = ages

    def save_best_individual_in_generation(self, parent_population: [], generation: int):
        best_individual = min(parent_population, key=attrgetter('objective_value'))
        self.best_individual_in_generation.append([best_individual, generation])

    # Note: these fitnesses are from the beginning of the generation, before offspring is generated
    def save_fitness_and_rank(self, id_fitness_list: [], generation: int):
        id_fitness_list.sort(key=lambda id_fitness: id_fitness['fitness'], reverse=True)
        rank_counter = 1
        ranks = []
        for id_fitness in id_fitness_list:
            ranks.append({'id': id_fitness['id'], 'rank': rank_counter, 'fitness': id_fitness['fitness']})
            rank_counter += 1
        self.ranks_per_generation.append({generation: ranks})
