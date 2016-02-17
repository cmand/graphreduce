"""
KDD.py
Implements k-core/modified DRVE/modified DRE graph reduction 
author: Erik Rye
date: 14 June 15
Note that this method may not work for arbitrary graphs and has been primarily
tested with AS-level Internet instances. Problems occur in arbitrary graphs when
the k-core for highest value of k does not have a large excess of edges during
the node-reduction stage; this has not occurred in our Internet graph sampling.
"""
import os
import networkx as nx
import random
from math import ceil

def KDD(graph, reduction_list, num_trials, edges, verbose):
    n = reduction_list[0]
    e = edges
    if not os.path.exists('KDD/'):
        os.mkdir('KDD/')
    for trial in range(num_trials):
        random.seed(trial)
        if verbose:
            print "Staring reduction number: " + str(trial)
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
        node_removed_number = int(g.number_of_nodes() - n)/4
        last_node_count = g.number_of_nodes()
        while g.number_of_nodes() > n:
            if verbose and (g.number_of_nodes() != last_node_count):
                print "Graph node/edge count:", g.number_of_nodes(), g.number_of_edges()
                last_node_count = g.number_of_nodes()
            rn = random.sample(g.nodes(), node_removed_number) 
            if node_removed_number > 1:
                node_removed_number -= 1
            else:
                node_removed_number = 1
            edges = []
            for node in rn:
                edges.append(random.choice(g.edges(node)))

            g.remove_edges_from(edges)
            if nx.number_connected_components(g) != 1:
                nodes = 0
                for h in nx.connected_component_subgraphs(g):
                    if h.number_of_nodes() > nodes:
                        nodes = h.number_of_nodes()
                        temp = h.copy()
                if temp.number_of_nodes() >= n and temp.number_of_edges() >= e:
                    g = temp.copy()
                else:
                    g.add_edges_from(edges)
            
            else:
                if g.number_of_edges() < e:
                    g.add_edges_from(edges)
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
        nx.write_gexf(g, 'KDD/KDD-' + str(trial) + '.gexf')
        if verbose:
            print "Reduced graph written."
