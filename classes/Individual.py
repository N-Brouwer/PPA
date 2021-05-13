from PPA.classes.Benchmark import Benchmark


class Individual:

    def __init__(self, individual_id: int):
        self.inputs = []
        self.objective_value = None  # None is checked, if None: then caluclate; else: assume it is calculated
        self.norm_objective_value = None
        self.fitness = None
        self.n_offspring = None

        self.parents = []
        self.parent_id = None
        self.parent_child_relation_recorded = False
        self.id = individual_id


    def set_inputs(self, inputs: []):
        self.inputs = inputs
        return self

    def set_parents(self, ancestor_parents: []):
        heritage_data = {"id": self.id, "objective_value":self.objective_value, "inputs":self.inputs}
        ancestor_parents.append(heritage_data)
        self.parents = ancestor_parents

    def calculate_fitness(self, benchmark: Benchmark):
        self.fitness = benchmark.eval(self.inputs)
