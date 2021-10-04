# Survivor selection for the plant propagation algorithm (PPA)

This repository presents the code used for the Evo* conference submittion: Evolutionary Algorithm Optimization: Survivor selection in the plant propagation algorithm.

the file structure is as follows

- config.py : all configurations set for running the experiments
- run.py    : The "init" class for the experiments to run, this class calls to specific PPA processes and checks if the experiments are done

- classes:
    - Benchmark.py          : all benchmark functions implemented
    - DataExporter.py       : at the end of a run, results are exported to csv using this class
    - Heritage.py           : during a run all data is stored in this class
    - Individual.py         : the class that represents an individual in the search space with all its properties (objective value, fitness value, inputs, etc)
    - PPAProcess.py         : the class containing all plant propagation algorithm components, called upon by the run.py
    - SurvivorSelection.py  : All implemented survivor selection methods
- notebooks:
    - brouwer_vandenberg_2022/brouwer_vdberg_2022_data_analysis.ipynb : the most recent notebook used for analysing data and exporting graphs
