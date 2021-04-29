import math
import random

import numpy as np
from PPA.classes.Benchmark import Benchmark
from PPA.classes.Individual import Individual
from PPA.classes.SurvivorSelection import SurvivorSelection


class PPAProcess:

    def __init__(self, pop_size: int, max_offspring: int, benchmark: Benchmark, survivor_selection: SurvivorSelection):
        self.pop_size = pop_size
        self.max_offspring = max_offspring
        self.id_counter = 0

        self.benchmark = benchmark
        self.survivor_selection = survivor_selection

        self.parent_population = self.initial_generate_parents(pop_size, benchmark)
        self.offspring_population = []

        self.parents_norm_objective_values = []
        self.offspring_norm_objective_values = []

        self.parents_fitness = []
        self.offspring_fitness = []

    def calculate_objective_values_parents(self):
        raw_objective_values = self.calculate_objective_values(self.parent_population)
        norm_objective_values = self.normalize_objective_values(raw_objective_values, self.parent_population)
        self.parents_norm_objective_values = norm_objective_values

    def calculate_objective_values_offspring(self):
        raw_objective_values = self.calculate_objective_values(self.offspring_population)
        norm_objective_values = self.normalize_objective_values(raw_objective_values, self.offspring_population)
        self.offspring_norm_objective_values = norm_objective_values

    def calculate_fitness_values_parents(self):
        self.parents_fitness = self.calculate_fitness(self.parent_population)

    def calculate_fitness_values_offspring(self):
        self.offspring_fitness = self.calculate_fitness(self.offspring_population)

    def generate_offspring(self):
        population = self.parent_population
        new_offspring = []

        for i in population:
            number_offspring = (
                math.ceil(self.max_offspring * i.fitness * random.uniform(0, 1)))  # note we use [0,1] instead of [0,1)
            for r in range(0, number_offspring):
                new_inputs = []
                for j in range(self.benchmark.input_dimension):
                    distance = 2 * (1 - i.fitness) * (random.uniform(0, 1) - 0.5)

                    new_inputs.append(
                        i.inputs[j] + ((self.benchmark.bounds[j][1] - self.benchmark.bounds[j][0]) * distance))
                self.id_counter += 1
                new_individual = Individual(self.id_counter)
                new_individual.set_inputs(new_inputs).objective_value = self.benchmark.eval(new_inputs)

                new_offspring.append(new_individual)

        self.offspring_population = new_offspring

    def select_survivors(self):
        self.parent_population = self.survivor_selection.select_survivors(self.parent_population,
                                                                          self.offspring_population)

    #  sort of private functions
    def calculate_fitness(self, population: []):
        fitness_list = []
        for i in population:
            fitness = 0.5 * (np.tanh(4 * i.norm_objective_value - 2) + 1)
            i.fitness = fitness
            fitness_list.append(fitness)
        return fitness_list

    def calculate_objective_values(self, population: []):
        if len(population) < 1:
            raise Exception('Calculating objective values of empty population')
        objective_values = []
        for i in population:
            if i.objective_value is None:
                i.objective_value = self.benchmark.eval(i.inputs)
            objective_values.append(i.objective_value)
        return objective_values

    def normalize_objective_values(self, objective_values: [], population: []):
        norm_objective_values = []
        min_objective_val = min(objective_values)
        max_objective_val = max(objective_values)
        for i in population:
            i.norm_objective_value = (max_objective_val - i.objective_value) / (max_objective_val - min_objective_val)

        return norm_objective_values

    def initial_generate_parents(self, pop_size: int, benchmark: Benchmark):
        parents = []
        self.parent_population = []
        for i in range(0, pop_size):
            self.id_counter += 1
            x = Individual(self.id_counter)
            inputs = []
            for d in range(0, benchmark.input_dimension):
                bound = benchmark.bounds[d]
                inputs.append(np.random.uniform(bound[0], bound[1]))
            x.set_inputs(inputs)
            x.calculate_fitness(benchmark)
            parents.append(x)

        return parents
