import pickle
import sys
if __name__ == '__main__':
    test = pickle.load(open(r"../results/results-2021-05-11_12-43-12/mulambda-Ackley100Drun-0.p", "rb"))
    size = sys.getsizeof(test.best_objval_during_run, float)
    print(f'size: {size}')
    print("test")