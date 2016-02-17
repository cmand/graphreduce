'''
Faloutsos Deletion Methods
    deletion.py
    
CS4910

Created on Jan 11, 2015

@author: Erik Rye
'''

import networkx as nx
from random import randint, uniform, seed
import sys

class Deletion:
    def __init__(self, graph, sd):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.num_edges = graph.number_of_edges()
        self.nodes = graph.nodes()
        self.edges = graph.edges()
        seed(sd)
 
    def _updateMetrics(self):
        if nx.number_connected_components(self.graph) == 1:
            self.num_nodes = self.graph.number_of_nodes()
            self.num_edges = self.graph.number_of_edges()
            self.nodes = self.graph.nodes()
            self.edges = self.graph.edges()
        else:
            self.num_nodes = 0
            for graph in nx.connected_component_subgraphs(self.graph):
                if graph.number_of_nodes() > self.num_nodes:
                    self.num_nodes = graph.number_of_nodes()
                    self.graph = graph
            
            self.num_edges = self.graph.number_of_edges()
            self.nodes = self.graph.nodes()
            self.edges = self.graph.edges()
                        
        return None

    #Deletion of Random Vertex
    def DRV(self, num_desired):
        self._updateMetrics()
        while num_desired < self.num_nodes:
            #need to get a random vertex to pop
            random_vertex = self.nodes[randint(0, self.num_nodes-1)]
            self.graph.remove_node(random_vertex)
            self._updateMetrics()
        return self.graph
       
    #Deletion of Random Edge
    def DRE(self, num_desired=0, _pure=True):
        self._updateMetrics()
        if _pure:
            while num_desired < self.num_nodes:
                #need to get a random edge to pop
                random_edge = self.edges[randint(0, self.num_edges-1)]
                self.graph.remove_edge(*random_edge)
                self._updateMetrics()
            return self.graph
        else:
            #need to get a random edge to pop
            random_edge = self.edges[randint(0, self.num_edges-1)]
            self.graph.remove_edge(*random_edge)
            self._updateMetrics()
    
    #Deletion of Random Vertex/Edge
    def DRVE(self, num_desired=0, _pure=True):
        self._updateMetrics()
        if _pure:
            while num_desired < self.num_nodes:
                random_vertex = self.nodes[randint(0, self.num_nodes-1)]
                #find the edges incident to that vertex
                incident_edges = self.graph.edges(random_vertex)
                #select one, then delete it
                random_edge = incident_edges[randint(0, len(incident_edges)-1)]

                self.graph.remove_edge(*random_edge)                
                self._updateMetrics()
            
	    return self.graph
    
        else:
            random_vertex = self.nodes[randint(0, self.num_nodes-1)]
            #find the edges incident to that vertex
            incident_edges = self.graph.edges(random_vertex)
            #select one, then delete it
            random_edge = incident_edges[randint(0, len(incident_edges)-1)]

            self.graph.remove_edge(*random_edge)                
            self._updateMetrics()
    
    
    #Hybrid DRVE and DRE, where probability is of DVRE
    #DHYB-1 == DRVE and DHYB-0 == DRE
    def DHYB(self, probability, num_desired):
        while num_desired < self.num_nodes:
            magic_number = uniform(0,1)
            if magic_number < probability:
                self.DRVE(0,False)
            else:
                self.DRE(0,False)
        return self.graph
        
