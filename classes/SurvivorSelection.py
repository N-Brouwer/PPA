import numpy as np


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
            return self.tournament
        elif method_name == 'rouletteWheel':
            return self.rws
        elif method_name == 'linearRanking':
            return self.linear_ranking
        else:
            raise Exception('the specified survivor selection method does not exist')

    def select_survivors(self, parents: [], offspring: []):
        return self.method(parents, offspring)

    def mulambda(self, parents: [], offspring: []):

        return 'not implemented yet'

    def mupluslambda(self, parents: [], offspring: []):
        print('im mupluslambda')
        new_population = parents + offspring
        new_population.sort(key=lambda i: i.fitness)

        print('============parents====================')
        print(parents)

        print('============offspring====================')
        print(offspring)

        print('============new population====================')
        print(new_population)

        return new_population[:self.pop_size]
        # return 'not implemented yet'

    def tournament(self, parents: [], offspring: []):
        return 'not implemented yet'

    def rws(self, parents: [], offspring: []):
        return 'not implemented yet'

    def linear_ranking(self, parents: [], offspring: []):
        return 'not implemented yet'
