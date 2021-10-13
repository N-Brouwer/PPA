import math
import numpy as np

# the benchmark function, determined by the inialization of each run, fed by the config file
# every instance hold all information of a benchmark function, including, bounds and optimum
class Benchmark:

    def __init__(self, benchmark_name, input_dimensions):
        self.input_dimension = input_dimensions
        self.bounds = None  # [[lower:float, upper:float]] per dimension
        self.benchmark = None
        self.optimum = None
        self.set_benchmark(benchmark_name)
        self.eval_counter = 0

    # we dynamically assign a benchmark function to the self.benchmark object, and set the properties of each benchmark
    # as class object values; by doing so we can treat every benchmark the same with the same class calls
    def set_benchmark(self, benchmark_name: str):

        if benchmark_name == 'Six-Hump-Camel':
            self.bounds = [[-3.0, 3.0], [-2.0, 2]]
            self.benchmark = self.six_hump_camel
            self.optimum = -1.031628453489877

        elif benchmark_name == 'Martin-Gaddy':
            self.bounds = [[-20.0, 20.0], [-20.0, 20.0]]
            self.benchmark = self.martin_gaddy
            self.optimum = 0

        elif benchmark_name == 'Goldstein-Price':
            self.bounds = [[-2, 2], [-2, 2]]
            self.benchmark = self.goldstein_price
            self.optimum = 3

        elif benchmark_name == 'Branin':
            self.bounds = [[-5, 15], [-5, 15]]
            self.benchmark = self.branin
            self.optimum = 0.39788735772973816

        elif benchmark_name == 'Easom':
            self.bounds = [[-100, 100], [-100, 100]]
            self.benchmark = self.easom
            self.optimum = -1

        elif benchmark_name == 'Rosenbrock':
            self.bounds = [[-5, 10] for i in range(self.input_dimension)]
            self.benchmark = self.rosenbrock
            self.optimum = 0

        elif benchmark_name == 'Ackley':
            self.bounds = [[-100, 100] for i in range(self.input_dimension)]
            self.benchmark = self.ackley
            self.optimum = 0

        elif benchmark_name == 'Griewank':
            self.bounds = [[-600, 600] for i in range(self.input_dimension)]
            self.benchmark = self.griewank
            self.optimum = 0

        elif benchmark_name == 'Rastrigrin':
            self.bounds = [[-5.12, 5.12] for i in range(self.input_dimension)]
            self.benchmark = self.rastrigrin
            self.optimum = 0

        elif benchmark_name == 'Schwefel':
            self.bounds = [[-500, 500] for i in range(self.input_dimension)]
            self.benchmark = self.schwefel
            self.optimum = 0

        elif benchmark_name == 'Ellipse':
            self.bounds = [[-100, 100] for i in range(self.input_dimension)]
            self.benchmark = self.ellipse
            self.optimum = 0

        elif benchmark_name == 'Cigar':
            self.bounds = [[-100, 100] for i in range(self.input_dimension)]
            self.benchmark = self.cigar
            self.optimum = 0

        elif benchmark_name == 'Tablet':
            self.bounds = [[-100, 100] for i in range(self.input_dimension)]
            self.benchmark = self.tablet
            self.optimum = 0

        elif benchmark_name == 'Sphere':
            self.bounds = [[-100,100] for i in range(self.input_dimension)]
            self.benchmark = self.sphere
            self.optimum = 0
        else:
            raise Exception('The provided benchmark function does not exist')

    # called to evaluate the inputs of a individual on the specified benchmark function
    def eval(self, inputs: np.array):
        self.eval_counter += 1
        return self.benchmark(inputs)

    # =============
    # Below are all the separate benchmark functions
    # =============
    def six_hump_camel(self, inputs: []):
        first_term = (4 - 2.1 * (inputs[0] ** 2) + (inputs[0] ** 4) / 3) * inputs[0] ** 2
        second_term = inputs[0] * inputs[1]
        third_term = (-4 + 4 * (inputs[1] ** 2)) * inputs[1] ** 2

        return first_term + second_term + third_term

    def martin_gaddy(self, inputs: []):
        first_term = (inputs[0] - inputs[1]) ** 2
        second_term = ((inputs[0] + inputs[1] - 10) / 3) ** 2

        return first_term + second_term

    def goldstein_price(self, inputs: []):
        first_term = 1 + ((inputs[0] + inputs[1] + 1) ** 2) * (
                19 - 14 * inputs[0] + 3 * inputs[0] ** 2 - 14 * inputs[1] + 6 * inputs[0] * inputs[1] + 3 * inputs[
            1] ** 2)

        second_term = 30 + ((2 * inputs[0] - 3 * inputs[1]) ** 2) * (
                18 - 32 * inputs[0] + 12 * inputs[0] ** 2 + 48 * inputs[1] - 36 * inputs[0] * inputs[1] + 27 *
                inputs[1] ** 2)

        return first_term * second_term

    def branin(self, inputs: []):
        first_term = inputs[1] - (5.1 / (4 * math.pi ** 2)) * inputs[0] ** 2 + (5 / math.pi) * inputs[0] - 6
        second_term = 10 * (1 - 1 / (8 * math.pi)) * math.cos(inputs[0])

        return first_term ** 2 + second_term + 10

    def easom(self, inputs: []):
        return -math.cos(inputs[0]) * math.cos(inputs[1]) * math.exp(
            -(inputs[0] - math.pi) ** 2 - (inputs[1] - math.pi) ** 2)

    def rosenbrock(self, inputs: []):
        return sum([100 * (inputs[i + 1] - inputs[i] ** 2) ** 2 + (inputs[i] - 1) ** 2 for i in range(len(inputs) - 1)])

    def ackley(self, inputs: []):
        first_term = -20 * math.exp(-0.2 * math.sqrt((1 / len(inputs)) * sum([param ** 2 for param in inputs])))
        second_term = math.exp((1 / len(inputs)) * sum([math.cos(2 * math.pi * param) for param in inputs]))

        return first_term - second_term + 20 + math.e

    def griewank(self, inputs: []):
        first_term = sum([(param ** 2) / 4000 for param in inputs])
        second_term = np.prod([math.cos(param / math.sqrt(i + 1)) for i, param in enumerate(inputs)])
        return 1 + first_term + second_term

    def rastrigrin(self, inputs: []):
        return 10 * len(inputs) + sum([param ** 2 - 10 * math.cos(2 * math.pi * param) for param in inputs])

    def schwefel(self, inputs: []):
        return 418.9829 * len(inputs) - sum([param * math.sin(math.sqrt(abs(param))) for param in inputs])

    def ellipse(self, inputs: []):
        return sum([(10000 ** (i / (len(inputs) - 1))) * (param ** 2) for i, param in enumerate(inputs)])

    def cigar(self, inputs: []):
        term_1 = inputs[0] ** 2
        term_2 = sum([10000 * (x_i ** 2) for x_i in inputs[1:]])
        total_terms = term_1 + term_2
        return total_terms
        # return inputs[0] ** 2 + sum([10000 * param ** 2 for param in inputs[1:]])

    def tablet(self, inputs: []):
        return 10000 * inputs[0] ** 2 + sum([param ** 2 for param in inputs[1:]])

    def sphere(self, inputs: []):
        return sum([param ** 2 for param in inputs])
