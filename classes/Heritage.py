class Heritage:

    def __init__(self):
        self.ancestors = {}
        self.relations = []

    def add_ancestors(self, population: [], generation: int):
        for i in population:
            if i.id not in self.ancestors:
                self.ancestors.update({i.id: {'id': i.id, 'obj_values': i.objective_value, 'inputs': i.inputs, 'parents': i.parents,
                                              'generation': generation}})

    def save_relation(self, child_id, parent_id):
        self.relations.append([child_id, parent_id])
