#!/usr/bin/env python
#
# Program:          brite2gexf.py
# Author:           Robert Beverly <rbeverly@cmand.org>
# Purpose:          Convert BRITE (https://www.cs.bu.edu/brite/) topologies to Gephi GEXF
import xml.etree.ElementTree as ET
import sys

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

def readbrite(infile, nodes, edges):
  (read_nodes, read_edges) = (False, False)
  for line in open(infile):
    if len(line) <= 1: continue
    if line.find('Nodes:') == 0:
      read_nodes = True  
      continue
    if line.find('Edges:') == 0:
      read_nodes = False
      read_edges = True  
      continue
    if read_nodes:
      (nid, x, y, indeg, outdeg, asn, typ) = line.strip().split()
      node = ET.SubElement(nodes, "node", {'id' : nid, 'label' : asn})
    if read_edges:
      (eid, vom, zu, length, delay, bw, asvom, aszu, typ, tmp) = line.strip().split()
      edge = ET.SubElement(edges, "edge", {'id' : eid, 'source' : vom, 'target' : zu})

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Usage: %s <BRITE input>" % sys.argv[0]
    sys.exit(0)

  (root, nodes, edges) = stubxml()
  readbrite(sys.argv[1], nodes, edges)
  print ET.tostring(root)
