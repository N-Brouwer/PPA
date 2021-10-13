from PPA.classes.Benchmark import Benchmark

# The individual class represents an individual in the PPA process, containing all information belonging to an
# individual, amongst others: objective value, fitness value, input values, and some heritage data
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
        self.age = 0

    def set_inputs(self, inputs: []):
        self.inputs = inputs
        return self

    def set_parents(self, ancestor_parents: []):
        heritage_data = {"id": self.id, "objective_value": self.objective_value, "inputs": self.inputs}
        ancestor_parents.append(heritage_data)
        self.parents = ancestor_parents

    def calculate_fitness(self, benchmark: Benchmark):
        self.fitness = benchmark.eval(self.inputs)

