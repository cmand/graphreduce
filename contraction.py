'''
Faloutsos Contraction Methods
    contraction.py
    
CS4910

Created on Jan 11, 2015

@author: Erik Rye
'''

import networkx as nx
from random import randint, seed, choice

class Contraction:
    def __init__(self, graph, sd):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.num_edges = graph.number_of_edges()
        self.nodes = graph.nodes()
        self.edges = graph.edges()
	seed(sd)
    
    def _updateMetrics(self):
        self.num_edges = self.graph.number_of_edges()
        self.num_nodes = self.graph.number_of_nodes()
        self.nodes = self.graph.nodes()
        self.edges = self.graph.edges()

        return None
    
    def _contract_endpoints(self, node_1, node_2):
        num_node1_neighbors = len(self.graph.neighbors(node_1))
        num_node2_neighbors = len(self.graph.neighbors(node_2))

        if num_node1_neighbors <= num_node2_neighbors:
            for neighbor in self.graph.neighbors(node_1):
                if neighbor != node_2:
                    self.graph.add_edge(neighbor, node_2)
            self.graph.remove_node(node_1)
        else:
            for neighbor in self.graph.neighbors(node_2):
                if neighbor != node_1:
                    self.graph.add_edge(neighbor, node_1)  
            self.graph.remove_node(node_2)      
        
        return None
    
    #Contraction of Random Edge
    def CRE(self, num_desired):
        self._updateMetrics()
        while num_desired < self.num_nodes:
            try:
                random_edge = choice(self.edges)
            except:
                print self.edges
                sys.exit()

            node_1, node_2 = random_edge
            self._contract_endpoints(node_1, node_2)
            self._updateMetrics()
        return self.graph
    
    #Contraction of a random vertex/edge
    #Picks a random vertex, then contracts with random neighbor
    def CRVE(self, num_desired):
        self._updateMetrics()
        while num_desired < self.num_nodes:
            random_vertex = choice(self.nodes)
            neighbors =  self.graph.neighbors(random_vertex)
            if neighbors:
                random_neighbor = choice(neighbors)
                self._contract_endpoints(random_vertex, random_neighbor)
            else:
                pass
            self._updateMetrics()
        
        return self.graph
    
