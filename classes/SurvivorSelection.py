import random
import numpy as np
from PPA import config
from operator import attrgetter


class SurvivorSelection:

    def __init__(self, method_name: str, pop_size: int):
        self.method = self.set_method(method_name)
        self.pop_size = pop_size

    def set_method(self, method_name):
        if method_name == 'mulambda':
            return self.mulambda
        elif method_name == 'mupluslambda':
            return self.mupluslambda
        elif method_name == 'tournament':
            self.tournament_size = config.tournament_size
            return self.tournament
        elif method_name == 'roulette_wheel':
            return self.rws
        elif method_name == 'linear_ranking':
            return self.linear_ranking
        elif method_name == 'single_elitist_rws':
            return self.single_elitist_rws
        else:
            raise Exception('the specified survivor selection method does not exist')

    def select_survivors(self, parents: [], offspring: []):
        return self.method(parents, offspring)

    def mulambda(self, parents: [], offspring: []):
        new_population = offspring[:]
        new_population.sort(key=lambda i: i.objective_value)

        return new_population[:self.pop_size]

    def mupluslambda(self, parents: [], offspring: []):
        new_population = parents + offspring
        new_population.sort(key=lambda i: i.objective_value)

        return new_population[:self.pop_size]

    def tournament(self, parents: [], offspring: []):
        combined_population = parents + offspring
        new_population = []
        for i in range(self.pop_size):
            tournament = random.choices(combined_population, k=self.tournament_size)
            new_population.append(min(tournament, key=attrgetter('objective_value')))

        return new_population

    def single_elitist_rws(self, parents: [], offspring: []):
        new_population = self.rws(parents, offspring, self.pop_size-1)
        combined_population = parents[:] + offspring[:] # todo check if calculations do not influence the original parents and offspring variables
        new_population.append(min(combined_population, key=attrgetter('objective_value')))
        return new_population

    def rws(self, parents: [], offspring: [], custom_pop_size=-1):
        combined_population = parents[:] + offspring[
                                           :]  # todo check if calculations do not influence the original parents and offspring variables
        # normalize objective values
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

        for t in range(population_size):
            roulette_wheel = 0
            r = random.uniform(0, summed_renorm_objective_value)
            for i in combined_population:

                roulette_wheel += i.renorm_objective_value
                if roulette_wheel >= r:
                    new_population.append(i)
                    break

        # # remove one from pop size in the loop before and comment-in these two lines to add elitist approach:
        # combined_population.sort(key=lambda i: i.objective_value)
        # new_population.append(combined_population[0])

        return new_population

    def linear_ranking(self, parents: [], offspring: []):
        new_population = []
        combined_population = parents[:] + offspring[:]
        combined_population.sort(key=lambda i: i.objective_value)
        sum_of_ranks = sum(np.arange(1, len(combined_population) + 1,
                                     1))  # added 1 because the minimal position is 0, but should be rank 1


        for t in range(self.pop_size):
            y = 0
            r = random.uniform(0, sum_of_ranks)
            rank = len(combined_population)+1
            for i in combined_population:
                rank -= 1
                y += rank
                if y >= r:
                    new_population.append(i)
                    break

        return new_population

    # def select_rws_winner(self, population:[]):
