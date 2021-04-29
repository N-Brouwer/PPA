import numpy as np
from PPA.classes.Benchmark import Benchmark


class Individual:

    def __init__(self):
        print('init')
        self.inputs = []
        self.fitness = None
        self.id = None

    def set_inputs(self, inputs: np.array):
        self.inputs = inputs

    def calculate_fitness(self, benchmark: Benchmark):
        self.fitness = benchmark.eval(self.inputs)
