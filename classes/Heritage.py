class Heritage:

    def __init__(self):
        self.ancestors = {}

    def add_ancestors(self, population: [], generation: int):
        for i in population:
            if i.id not in self.ancestors:
                self.ancestors.update({i.id: {'id': i.id, 'obj_values': i.objective_value, 'inputs': i.inputs, 'parents': i.parents,
                                              'generation': generation}})
