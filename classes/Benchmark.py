import numpy as np


class Benchmark:

    def __init__(self, benchmark_name):
        self.input_dimension = None
        self.bounds = None  # [float, float]
        self.benchmark = None
        self.set_benchmark(benchmark_name)

    def set_benchmark(self, benchmark_name: str):
        if benchmark_name == 'Griewank':
            self.input_dimension = 1
            self.bounds = [[0.0, 3.0]]
            self.benchmark = self.griewank

    def eval(self, inputs: np.array):
        return self.benchmark(inputs)

    def griewank(self, inputs: np.array):
        if len(inputs) != self.input_dimension:
            raise Exception('Input and benchmark dimension mismatch in Griewank')
        result = np.exp(inputs[0])
        return result


