import math
import random
from operator import attrgetter

import numpy as np
from PPA.classes.Benchmark import Benchmark
from PPA.classes.Individual import Individual
from PPA.classes.SurvivorSelection import SurvivorSelection
from PPA.classes.Heritage import Heritage


class PPAProcess:

    def __init__(self, pop_size: int, max_offspring: int, benchmark: Benchmark, survivor_selection: SurvivorSelection,
                 heritage: Heritage):
        self.pop_size = pop_size
        self.max_offspring = max_offspring
        self.id_counter = 0
        self.generation = 0

        self.benchmark = benchmark
        self.survivor_selection = survivor_selection
        self.heritage = heritage

        self.parent_population = self.initial_generate_parents(pop_size, benchmark)
        self.offspring_population = []

        self.parents_norm_objective_values = []
        self.offspring_norm_objective_values = []

        self.parents_fitness = []  # todo do i still use this?
        self.offspring_fitness = []  # todo do i still use this?

        # used for data analytics:
        self.run_n = ''
        self.benchmark_name = ''
        self.survivor_selection_name = ''
        self.best_objval_during_run = self.parent_population[
            0]  # recorded in the select survivors method, initialised with a random individual

    def calculate_objective_values_parents(self):
        self.calculate_objective_values(self.parent_population)

    def normalize_objective_values_parents(self):
        self.parents_norm_objective_values = self.normalize_objective_values(self.parent_population)

    # def calculate_objective_values_offspring(self):
    #     self.calculate_objective_values(self.offspring_population)

    def normalize_objective_values_offspring(self):
        self.offspring_norm_objective_values = self.normalize_objective_values(self.offspring_population)

    def calculate_fitness_values_parents(self):
        self.parents_fitness = self.calculate_fitness(self.parent_population)

    def calculate_fitness_values_offspring(self):
        self.offspring_fitness = self.calculate_fitness(self.offspring_population)

    def generate_offspring(self):
        population = self.parent_population
        new_offspring = []

        for i in population:
            try:
                number_offspring = (
                    math.ceil(
                        self.max_offspring * i.fitness * random.uniform(0, 1)))  # note we use [0,1] instead of [0,1)
            except:
                raise Exception('There probably is a nan value in the fitness values')

            for r in range(0, number_offspring):
                new_inputs = []
                for j in range(self.benchmark.input_dimension):

                    distance = 2 * (1 - i.fitness) * (random.uniform(0, 1) - 0.5)
                    new_input = i.inputs[j] + ((self.benchmark.bounds[j][1] - self.benchmark.bounds[j][0]) * distance)

                    corrected_input = self.benchmark.bounds[j][0] if new_input < self.benchmark.bounds[j][0] else \
                        self.benchmark.bounds[j][1] if new_input > self.benchmark.bounds[j][1] else new_input
                    new_inputs.append(corrected_input)

                self.id_counter += 1
                new_individual = Individual(self.id_counter)
                new_individual.parent_id = i.id
                new_individual.set_inputs(new_inputs).objective_value = self.benchmark.eval(new_inputs)
                new_individual.set_parents(i.parents[:])

                new_offspring.append(new_individual)

        self.offspring_population = new_offspring

    def select_survivors(self):
        self.parent_population = self.survivor_selection.select_survivors(self.parent_population,
                                                                          self.offspring_population)
        min_objval_individual = min(self.parent_population, key=attrgetter('objective_value'))
        if min_objval_individual.objective_value < self.best_objval_during_run.objective_value:
            self.best_objval_during_run = min_objval_individual

    def save_heritage(self):
        self.heritage.add_ancestors(self.parent_population, self.generation)
        for individual in self.parent_population:
            if not individual.parent_child_relation_recorded:
                self.heritage.save_relation(individual.id, individual.parent_id)

    #  sort of private functions
    def calculate_fitness(self, population: []):
        fitness_list = []

        min_objective_val = min(individual.objective_value for individual in population)
        max_objective_val = max(individual.objective_value for individual in population)
        if min_objective_val == max_objective_val:
            for i in population:
                i.fitness = 0.5
                fitness_list.append(0.5)
            return
        else:
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

    def normalize_objective_values(self, population: []):
        norm_objective_values = []
        min_objective_val = min(individual.objective_value for individual in population)
        max_objective_val = max(individual.objective_value for individual in population)

        epsilon = 1e-100
        for i in population:
            i.norm_objective_value = (max_objective_val - i.objective_value) / (
                    (max_objective_val - min_objective_val) + epsilon)

        return norm_objective_values

    def initial_generate_parents(self, pop_size: int, benchmark: Benchmark):
        parents = []
        self.parent_population = []
        for i in range(0, pop_size):
            self.id_counter += 1
            x = Individual(self.id_counter)
            x.parent_id = -1
            inputs = []
            for d in range(0, benchmark.input_dimension):
                bound = benchmark.bounds[d]
                inputs.append(random.uniform(bound[0], bound[1]))
            x.set_inputs(inputs)
            x.set_parents([])
            parents.append(x)

        return parents
