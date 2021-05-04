import numpy as np


class Benchmark:

    def __init__(self, benchmark_name):
        self.input_dimension = None
        self.bounds = None  # [[lower:float, upper:float]] per dimension
        self.benchmark = None
        self.set_benchmark(benchmark_name)
        self.eval_counter = 0

    def set_benchmark(self, benchmark_name: str):
        if benchmark_name == 'Griewank':
            self.input_dimension = 1
            self.bounds = [[0.0, 3.0]]
            self.benchmark = self.griewank
        elif benchmark_name == 'Six Hump Camel':
            self.input_dimension = 2
            self.bounds = [[-3.0, 3.0], [-2.0, 2]]
            self.benchmark = self.six_hump_camel
        elif benchmark_name == 'Martin-Gaddy':
            self.input_dimension = 2
            self.bounds = [[-20.0, 20.0], [-20.0, 20.0]]
            self.benchmark = self.martin_gaddy

    def eval(self, inputs: np.array):
        self.eval_counter += 1
        return self.benchmark(inputs)

    def griewank(self, inputs: []):
        if len(inputs) != self.input_dimension:
            raise Exception('Input and benchmark dimension mismatch in Griewank')
        result = np.exp(inputs[0])
        return result

    def six_hump_camel(self, inputs: []):
        first_term = (4 - 2.1 * (inputs[0] ** 2) + (inputs[0] ** 4) / 3) * inputs[0] ** 2
        second_term = inputs[0] * inputs[1]
        third_term = (-4 + 4 * (inputs[1] ** 2)) * inputs[1] ** 2

        return first_term + second_term + third_term

    def martin_gaddy(self, inputs: []):
        first_term = (inputs[0] - inputs[1]) ** 2
        second_term = ((inputs[0] + inputs[1] - 10) / 3) ** 2

        return first_term + second_term
