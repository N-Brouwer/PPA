import math
import random
from operator import attrgetter

import numpy as np
from PPA.classes.Benchmark import Benchmark
from PPA.classes.Individual import Individual
from PPA.classes.SurvivorSelection import SurvivorSelection
from PPA.classes.Heritage import Heritage


# Containing all elements of the PPA process, together with some heritage objects.
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

        self.parents_fitness = []

        self.best_objval_during_run = self.parent_population[
            0]  # placeholder, updated in first evaluation of inputs recorded in the select survivors method

     # We initialize popSize new individuals, and set their parent to be -1,
    def initial_generate_parents(self, pop_size: int, benchmark: Benchmark):
        parents = []
        self.parent_population = []
        for i in range(0, pop_size):
            # to ensure every individual gets a unique id, we increase the id_counter here, and in the generate
            # offspring function everytime a new individual is created
            self.id_counter += 1
            x = Individual(self.id_counter)
            x.parent_id = -1
            inputs = []
            # we initialize an individual within the bounds of the benchmark function
            for d in range(0, benchmark.input_dimension):
                bound = benchmark.bounds[d]
                inputs.append(random.uniform(bound[0], bound[1]))
            x.set_inputs(inputs)
            x.set_parents([])
            # finally we append each individual to the parent collection
            parents.append(x)

        return parents    
        
        
    def calculate_objective_values_parents(self):
        self.calculate_objective_values(self.parent_population)
        self.best_objval_during_run = min(self.parent_population,
                                          key=attrgetter('objective_value'))

    def normalize_objective_values_parents(self):
        self.parents_norm_objective_values = self.normalize_objective_values(self.parent_population)

    def calculate_fitness_values_parents(self):
        self.parents_fitness = self.calculate_fitness(self.parent_population)

    # here we generate the offspring for every individual according to the PPA
    def generate_offspring(self):
        population = self.parent_population
        new_offspring = []

        # we loop over EVERY individual
        for i in population:
            try:
                # determine the number of offspring
                number_offspring = (
                    math.ceil(
                        self.max_offspring * i.fitness * random.uniform(0, 1)))  # note we use [0,1] instead of [0,1)
            except:
                raise Exception('There probably is a nan value in the fitness values')
            # For every offspring we determine the mutation
            for r in range(0, number_offspring):
                new_inputs = []
                for j in range(self.benchmark.input_dimension):
                    distance = 2 * (1 - i.fitness) * (random.uniform(0, 1) - 0.5)
                    new_input = i.inputs[j] + ((self.benchmark.bounds[j][1] - self.benchmark.bounds[j][0]) * distance)

                    corrected_input = self.benchmark.bounds[j][0] if new_input < self.benchmark.bounds[j][0] else \
                        self.benchmark.bounds[j][1] if new_input > self.benchmark.bounds[j][1] else new_input
                    new_inputs.append(corrected_input)

                # from here the offspring is actually created and assigned the mutated input values
                self.id_counter += 1
                new_individual = Individual(self.id_counter)
                new_individual.parent_id = i.id
                new_individual.set_inputs(new_inputs).objective_value = self.benchmark.eval(new_inputs)

                # the parent's heritage is added to the new individual
                new_individual.set_parents(i.parents[:])

                new_offspring.append(new_individual)
        # the previous offspring population is replaced with the current offspring population
        self.offspring_population = new_offspring

    # we select the survivors according to the selection method per run, defined by the run.py class initialization
    def select_survivors(self):
        self.parent_population = self.survivor_selection.select_survivors(self.parent_population,
                                                                          self.offspring_population)

        # we save the lowest objective value, since we do minimization, of the entire parent population
        min_objval_individual = min(self.parent_population, key=attrgetter('objective_value'))
        if min_objval_individual.objective_value < self.best_objval_during_run.objective_value:
            self.best_objval_during_run = min_objval_individual

    # here we save some heritage data, like the rank and fitness of every individual in a generation, number of distinct
    # individuals and the best individual and its inputs per generation
    def save_heritage(self):

        # the fitness and rank of the individuals at the beginning of this generation
        self.heritage.save_fitness_and_rank(self.parents_fitness, self.generation)

        # unique (or better distinct) individuals at the end of a generation
        self.heritage.save_unique_individual_count(self.generation, self.parent_population)

        # keep track of the whole individual object of the best individual of th generation
        self.heritage.save_best_individual_in_generation(self.parent_population, self.generation,
                                                         self.benchmark.eval_counter)

    # Calculate the fitness, but first check if the min and max are the same, meaning all objective values are the
    # same, then according to the PPA all fintess of the individuals becomes 0.5
    def calculate_fitness(self, population: []):
        fitness_list = []

        min_objective_val = min(individual.objective_value for individual in population)
        max_objective_val = max(individual.objective_value for individual in population)
        if min_objective_val == max_objective_val:
            for i in population:
                i.fitness = 0.5
                fitness_list.append({'id': i.id, 'fitness': 0.5})
            return fitness_list
        else:
            for i in population:
                fitness = 0.5 * (np.tanh(4 * i.norm_objective_value - 2) + 1)
                i.fitness = fitness
                fitness_list.append({'id': i.id, 'fitness': fitness})
            return fitness_list

    # evaluate inputs of individuals on the benchmark function, retrieving an objective value
    def calculate_objective_values(self, population: []):
        if len(population) < 1:
            raise Exception('Calculating objective values of empty population')
        objective_values = []
        for i in population:
            if i.objective_value is None:
                i.objective_value = self.benchmark.eval(i.inputs)
            objective_values.append(i.objective_value)
        return objective_values

    # Normalization of the objective values is done by dividing the max_objective value - objective value over the
    # difference between min and max objective value; the normalized objective values are stored in the individual
    # object per individual
    def normalize_objective_values(self, population: []):
        norm_objective_values = []
        min_objective_val = min(individual.objective_value for individual in population)
        max_objective_val = max(individual.objective_value for individual in population)

        # a really small epsilon is added in order to prevent division by zero, might it ever occur
        epsilon = 1e-100
        for i in population:
            i.norm_objective_value = (max_objective_val - i.objective_value) / (
                    (max_objective_val - min_objective_val) + epsilon)

        return norm_objective_values

   
