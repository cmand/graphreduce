"""
KKD.py
Implements k-core/k-deletion/modified DRE graph reduction
author: Erik Rye
date: 14 June 15
"""
import os, time
import networkx as nx
import random
from math import ceil

def KKD(graph, reduction_list, num_trials, edges, verbose):
    n = reduction_list[0]
    e = edges
    if not os.path.exists('KKD/'):
        os.mkdir('KKD/')
    for trial in range(num_trials):
        random.seed(trial)
        if verbose:
            print "Starting reduction number: " + str(trial)
        num_nodes = graph.number_of_nodes()
        k = 0
        g = nx.k_core(graph,k)
        while (nx.k_core(graph,k+1).number_of_nodes()) > n:
            k +=1 
            if verbose:
                print 'Calculating ' + str(k) + '-core...'
            g = nx.k_core(graph, k)
        if verbose:
            print "Removing nodes..."
        flag = False
        last_node_count = g.number_of_nodes()
        while g.number_of_nodes() > n:
            if not flag:
                rn= random.sample([x for x in g.nodes() if g.degree(x) == k], 50)
            else:
                rn = random.sample([x for x in g.nodes() if g.degree(x) == k], 1)

            edges = []
            for node in rn:
                edges.extend(g.edges(node))
            g.remove_nodes_from(rn)
            if nx.number_connected_components(g) != 1:
                nodes = 0
                for h in nx.connected_component_subgraphs(g):
                    if h.number_of_nodes() > nodes:
                        nodes = h.number_of_nodes()
                        temp = h.copy()
                if temp.number_of_nodes() >= n and temp.number_of_edges() >= e:
                    g = temp.copy()
                else:
                    flag = True
                    g.add_edges_from(edges)
            else:
                if g.number_of_edges() < e or g.number_of_nodes() < n:
                    g.add_edges_from(edges)
                    flag = True
            if verbose and (g.number_of_nodes() != last_node_count):
                print "Graph node/edge count: ", g.number_of_nodes(), g.number_of_edges()
                last_node_count = g.number_of_nodes()
        if verbose:
            print "Done removing nodes."
            print "Removing edges..."
        
        while g.number_of_edges() > e:
            edge = None
            while not edge:
                edge = random.choice(g.edges())
                g.remove_edge(*edge)
                if nx.number_connected_components(g) > 1:
                    g.add_edge(*edge)

        nx.write_gexf(g, 'KKD/KKD-' + str(trial) + '.gexf')
        if verbose:
            print "Reduced graph written."


