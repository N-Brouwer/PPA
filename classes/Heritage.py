class Heritage:

    def __init__(self):
        self.ancestors = {}
        self.relations = []
        self.unique_individual_count = []
        self.ages_per_generation = {}

    def add_ancestors(self, population: [], generation: int):
        for i in population:
            if i.id not in self.ancestors:
                self.ancestors.update(
                    {i.id: {'id': i.id, 'obj_values': i.objective_value, 'inputs': i.inputs, 'parents': i.parents,
                            'generation': generation}})

    def save_relation(self, child_id: int, parent_id: int):
        self.relations.append([child_id, parent_id])

    def save_unique_individual_count(self, generation: int, parent_population: []):
        unique_ids = set([individual.id for individual in parent_population])
        self.unique_individual_count.append([generation, len(unique_ids)])

    def save_ages(self, generation: int, parent_population: []):
        ages = [individual.age for individual in parent_population]
        self.ages_per_generation[generation] = ages

