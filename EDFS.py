'''
EDFS.py
Implements the Exploration by Depth-First Search graph reduction algorithm
author: Erik Rye
date: 14 June 15
'''

import exploration as ex
import networkx as nx
import os

def EDFS(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('EDFS/'):
        os.mkdir('EDFS/')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        for node_num in reduction_list:
            reduced_graph = graph.copy()
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            e = ex.Exploration(reduced_graph,trial)
            reduced_graph = e.EDFS(node_num)
            nx.write_gexf(reduced_graph, 'EDFS/' + str(node_num) + '-EDFS-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del e
                         
