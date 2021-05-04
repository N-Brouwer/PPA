from PPA.classes.Benchmark import Benchmark


class Individual:

    def __init__(self, individual_id: int):
        self.inputs = []
        self.objective_value = None  # None is checked, if None: then caluclate; else: assume it is calculated
        self.norm_objective_value = None
        self.fitness = None

        self.parents = []

        self.id = individual_id
        self.n_offspring = None

    def set_inputs(self, inputs: []):
        self.inputs = inputs
        return self

    def set_parents(self, ancestor_parents: []):
        ancestor_parents.append(self)
        self.parents = ancestor_parents

    def calculate_fitness(self, benchmark: Benchmark):
        self.fitness = benchmark.eval(self.inputs)
