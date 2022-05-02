import random
from copy import deepcopy

import numpy as np
from PPA import config
from operator import attrgetter


# the survivor selection class, selection survivors to participate in the next generation
class SurvivorSelection:

    def __init__(self, method_name: str, pop_size: int):
        self.method = self.set_method(method_name)
        self.pop_size = pop_size

    # we dynamically assign a selection method to the class object "method" this way every run can call the same
    # fucntion, but containing different selection methods
    def set_method(self, method_name):
        if method_name == 'mulambda':
            return self.mulambda
        elif method_name == 'mupluslambda':
            return self.mupluslambda
        elif method_name == 'tournament':
            self.tournament_size = config.tournament_size
            return self.tournament
        elif method_name == 'single_elitist_tournament':
            self.tournament_size = config.tournament_size
            return self.single_elitist_tournament
        elif method_name == 'no_replacement_tournament':
            self.tournament_size = config.tournament_size
            return self.no_replacement_tournament
        elif method_name == 'roulette_wheel':
            return self.rws
        elif method_name == 'linear_ranking':
            return self.linear_ranking
        elif method_name == 'single_elitist_rws':
            return self.single_elitist_rws
        else:
            raise Exception('the specified survivor selection method does not exist')

    # we call the dynamically assigned selection method
    def select_survivors(self, parents: [], offspring: []):
        return self.method(parents, offspring)

    # =============
    # Below are the selection methods as specified in the research
    # =============

    # add best individuals from offspring
    def mulambda(self, parents: [], offspring: []):
        new_population = offspring[:]
        new_population.sort(key=lambda i: i.objective_value)

        return new_population[:self.pop_size]

    # add popsize best individuals from parents + offspring
    def mupluslambda(self, parents: [], offspring: []):
        new_population = parents + offspring
        new_population.sort(key=lambda i: i.objective_value)

        return new_population[:self.pop_size]

    # tournament selection selecting one less individual, but add the best individual of parents + offspring
    def single_elitist_tournament(self, parents: [], offspring: []):
        new_population = self.tournament(parents, offspring, self.pop_size - 1)
        combined_population = parents[:] + offspring[:]
        new_population.append(min(combined_population, key=attrgetter('objective_value')))

        return new_population

    # this function performs exactly the same as tournament selection, except the individuals are selected without
    # replacement, made possible by using random.sample, instead of random.choices
    def no_replacement_tournament(self, parents: [], offspring: []):
        new_population = self.tournament(parents, offspring, self.pop_size, False)
        return new_population

    # the tournament selection method used by both with and without replacement tournament selection methods
    def tournament(self, parents: [], offspring: [], custom_pop_size=-1, replacement=True):
        combined_population = parents + offspring
        new_population = []
        new_pop_size = custom_pop_size if custom_pop_size > 0 else self.pop_size
        for i in range(new_pop_size):
            # the random.choices samples with replacement, the random.sample without replacement
            if replacement:
                tournament = random.choices(combined_population, k=self.tournament_size)
            else:
                tournament = random.sample(combined_population, k=self.tournament_size)
            winner = min(tournament, key=attrgetter('objective_value'))

            new_population.append(winner)
        return new_population

    # roulette wheel selection, except there is one less indivual selected, instead the best individual is
    # automatically transferred
    def single_elitist_rws(self, parents: [], offspring: []):
        new_population = self.rws(parents, offspring, self.pop_size - 1)
        combined_population = parents[:] + offspring[:]
        new_population.append(min(combined_population, key=attrgetter('objective_value')))
        return new_population

    # selection method where the relative objective value size is proportional to the selection probability
    def rws(self, parents: [], offspring: [], custom_pop_size=-1):
        combined_population = parents[:] + offspring[
                                           :]
        # (re-)normalize objective values because otherwise the the higher the objective value, the higher the
        # selection probability, which we do not want, we want the reverse to be true
        min_objective_val = min(individual.objective_value for individual in combined_population)
        max_objective_val = max(individual.objective_value for individual in combined_population)
        epsilon = 1e-100
        summed_renorm_objective_value = 0

        for i in combined_population:
            i.renorm_objective_value = (max_objective_val - i.objective_value) / (
                    (max_objective_val - min_objective_val) + epsilon)
            summed_renorm_objective_value += i.renorm_objective_value

        new_population = []

        population_size = custom_pop_size if custom_pop_size > 0 else self.pop_size

        # select popsize or custom popsize individuals form the parents+offspring
        for t in range(population_size):
            roulette_wheel = 0
            r = random.uniform(0, summed_renorm_objective_value)
            for i in combined_population:

                roulette_wheel += i.renorm_objective_value
                if roulette_wheel >= r:
                    new_population.append(i)
                    break

        return new_population
    # Select individuals based on rank, summing all ranks available and drawing a random number; next we add rank by
    # rank until the random number is met or passed
    def linear_ranking(self, parents: [], offspring: []):
        new_population = []
        combined_population = parents[:] + offspring[:]
        combined_population.sort(key=lambda i: i.objective_value)
        sum_of_ranks = sum(np.arange(1, len(combined_population) + 1,
                                     1))  # added 1 because the minimal position is 0, but should be rank 1

        for t in range(self.pop_size):
            y = 0
            r = random.uniform(0, sum_of_ranks)
            rank = len(combined_population) + 1
            for i in combined_population:
                rank -= 1
                y += rank
                if y >= r:
                    new_population.append(i)
                    break

        return new_population
