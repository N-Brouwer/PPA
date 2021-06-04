import pandas as pd
from graphviz import Digraph
from graphviz import *

edge_df = pd.read_csv("edge_test.csv")


u = Digraph('unix', filename='test/test-unix2.gv',
            node_attr={'color': 'lightblue2', 'style': 'filled'}, graph_attr={'newrank': "False", 'fixedsize': "False"})
u.attr(size='6,6')

# u.edge(f'{row["source"]}', f'{row["target"]}')

edge_df = edge_df.astype({"source": str, "target": str})
u.node("0")

for gen in edge_df.gen.unique():

    with u.subgraph() as s:
        s.attr(rank='same')
        counter = 0
        for i, row in edge_df[edge_df['gen'] == gen].iterrows():
            s.node(row['target'])
            counter += 1

for i, row in edge_df.iterrows():
    u.edge(row['source'], row['target'])
#     edge_df[edge_df['gen'] == gen].target.values
#     u.add_subgraph([edge_df[edge_df['gen'] == gen].target.values],name=f's-gen-{gen}').graph_attr['rank']='same'

#  for i, row in edge_df[edge_df['gen'] == gen].iterrows():
#             s.edge(f'{row["source"]}', f'{row["target"]}')

u.view()