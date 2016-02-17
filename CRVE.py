'''
CRVE.py
Implements the Contraction of a Random Vertex's Edge (CRVE) graph reduction
method
author: Erik Rye
date: 13 Jun 15
'''

import contraction as ct
import networkx as nx
import os

def CRVE(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('CRVE/'):
        os.mkdir('CRVE/')
    for trial in range(num_trials): 
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            c = ct.Contraction(reduced_graph,trial)
            reduced_graph = c.CRVE(node_num)
            nx.write_gexf(reduced_graph, 'CRVE/' + str(node_num) + '-CRVE-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del c
