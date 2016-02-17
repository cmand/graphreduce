'''
Faloutsos Exploration Methods
    exploration.py
    
CS4910


Created on Jan 11, 2015

@author: Erik Rye
'''

import networkx as nx
from random import randint, seed
import sys


class Exploration:
    def __init__(self, graph, sd):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.num_edges = graph.number_of_edges()
        self.nodes = graph.nodes()
        self.edges = graph.edges()
        self.resultant_graph = nx.Graph()
        self.BFS_white, self.BFS_gray, self.BFS_black = [], [], []
        self.DFS_white, self.DFS_gray, self.DFS_black = [], [], []
   	seed(sd)
 
    def _stop(self, num_desired):
        if self.resultant_graph.number_of_nodes() < num_desired:
            return False
        else:
            return True
        
    #Exploration by Breadth-First Search
    def EBFS(self, num_desired):
        self.BFS_white = list(self.nodes)
        start_node = self.BFS_white.pop(randint(0, self.num_nodes - 1))
        self.resultant_graph.add_node(start_node), self.BFS_gray.append(start_node)
        neighborhood = self.graph.neighbors(start_node) 

        for neighbor in neighborhood:
            self.resultant_graph.add_edge(start_node, neighbor)
            self.BFS_white.remove(neighbor), self.BFS_gray.append(neighbor)
        self.BFS_gray.remove(start_node), self.BFS_black.append(start_node)

        while not self._stop(num_desired):
            next_node = self.BFS_gray.pop(0)
            neighborhood = self.graph.neighbors(next_node)
            for neighbor in neighborhood:
                if neighbor in self.BFS_gray or neighbor in self.BFS_black:
                    pass
                else:
                    self.resultant_graph.add_edge(next_node, neighbor)
                    self.BFS_white.remove(neighbor), self.BFS_gray.append(neighbor)
                    if self._stop(num_desired):
                        break
            self.BFS_black.append(next_node)
            
        result_graph_nodes = self.resultant_graph.nodes()

        return self.graph.subgraph(result_graph_nodes)
    
    #Exploration by Depth-First Search
    def EDFS(self, num_desired):
        self.DFS_white = list(self.nodes)
        start_node = self.DFS_white.pop(randint(0, self.num_nodes - 1 ))
        self.resultant_graph.add_node(start_node), self.DFS_gray.append(start_node)
        self.DFS_visit(start_node, num_desired)  

        result_graph_nodes = self.resultant_graph.nodes()

        return self.graph.subgraph(result_graph_nodes)

    def DFS_visit(self, predecessor, num_desired):
        neighborhood = self.graph.neighbors(predecessor)
        while not self._stop(num_desired):
            while neighborhood != []:
                neighbor = neighborhood.pop(randint(0, len(neighborhood) - 1))
                if neighbor in self.DFS_white:
                    self.resultant_graph.add_edge(predecessor, neighbor)
                    self.DFS_white.remove(neighbor), self.DFS_gray.append(neighbor)
                    if self._stop(num_desired):
                        break
                    else:
                        predecessor = neighbor
                        neighborhood = self.graph.neighbors(neighbor)
                        continue
            
            self.DFS_black.append(predecessor), self.DFS_gray.remove(predecessor)
            if self.DFS_gray != []:
                predecessor = self.DFS_gray[-1]
                neighborhood = self.graph.neighbors(predecessor)
            else:
                return None
            
        return None  
