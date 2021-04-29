import numpy as np


class SurvivorSelection:

    def __init__(self, method_name):
        self.method = self.set_method(method_name)

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

    def mulambda(self, parents: np.array, offspring: np.array):
        return 'not implemented yet'

    def mupluslambda(self, parents: np.array, offspring: np.array):
        return 'not implemented yet'

    def tournament(self, parents: np.array, offspring: np.array):
        return 'not implemented yet'

    def rws(self, parents: np.array, offspring: np.array):
        return 'not implemented yet'

    def linear_ranking(self, parents: np.array, offspring: np.array):
        return 'not implemented yet'
