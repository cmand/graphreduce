#!/usr/bin/env python
#
# Program:          mrt2gexf.py
# Author:           Robert Beverly <rbeverly@cmand.org>
# Purpose:          Convert MRT BGP table to AS graph in Gephi GEXF
import networkx as nx
from mrtparse import *
import sys
from itertools import tee, izip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def stubxml():
  root = ET.Element('gexf')
  root.set('xmlns', 'http://www.gexf.net/1.2draft')
  root.set('version', '1.2')
  meta = ET.SubElement(root, "meta")
  meta.set('lastmodifieddate', '2009-03-20')
  creator = ET.SubElement(meta, "creator")
  creator.text = "CMAND"
  descr  = ET.SubElement(meta, "description")
  descr.text = "brite2gexf"
  graph = ET.SubElement(root, "graph")
  graph.set('mode', 'static')
  graph.set('defaultedgetype', 'directed')
  nodes = ET.SubElement(graph, "nodes")
  edges = ET.SubElement(graph, "edges")
  return root, nodes, edges

def readMRT(infile, G, n=0, verbose=False):
  d = Reader(sys.argv[1])
  while True: 
    try:
      m = d.next()
    except StopIteration:
      return
    n-=1
    if n == 0: return 
    m = m.mrt
    if m.err: continue
    if (m.type == MRT_T['TABLE_DUMP'] and m.subtype == TD_ST['AFI_IPv4']):
      for attr in m.td.attr:
        if attr.type == BGP_ATTR_T['AS_PATH']:
          aspath = attr.as_path[0]['val']
          for u, v in pairwise(aspath):
            (u,v) = (int(u), int(v))
            if verbose: print "%d -> %d" % (u,v)
            G.add_node(u)
            G.add_node(v)
            G.add_edge(u, v)
          

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Usage: %s <MRT input>" % sys.argv[0]
    sys.exit(0)

  G = nx.Graph()
  readMRT(sys.argv[1], G) 
  #print "Stats: %d nodes %d edges" % (G.number_of_nodes(), G.number_of_edges())
  for l in nx.generate_gexf(G) :
    print l
  sys.exit(0)
