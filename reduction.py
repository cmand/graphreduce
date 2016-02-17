import argparse, sys, CRE, CRVE, DRE, DRV, DRVE, DHYB, EBFS, EDFS, KDD, KKD
import networkx as nx

def check_args():
    """
    Ensures arguments passed are logically valid wrt graph
    """
    if args.verbose:
        print "Checking for valid type."
    types = ["cre", "crve", "dre", "drve", "dre", "drv", "edfs", "ebfs",
            "kdd", "kkd"]
    if args.type.lower() not in types and 'dhyb' not in args.type.lower():
        sys.stderr.write("Reduction type was invalid.\nExiting.\n")
        sys.exit(1)
    else:
        if 'dhyb' in args.type.lower():
            dhyb_prob = check_dhyb()
        else:
            dhyb_prob = None
            args.type = args.type.lower()
        if args.verbose:
            print "Valid type found."
    if args.verbose:
        print "Checking for valid graph."
    try:
        graph = nx.read_gexf(args.graph)
        max_nodes = nx.number_of_nodes(graph)
        args.graph = graph
        if args.verbose:
            print "Graph file read successfully."
    except:
        sys.stderr.write("Graph file not valid.\nExiting.\n")
        sys.exit(1)
    if args.verbose:
        print "Checking reduction end nodes less than initial node number."
    if args.end > max_nodes:
        sys.stderr.write("End number of nodes greater than the number of" +
                " nodes in the initial graph.\nExiting.\n")
        sys.exit(1)
    if args.verbose:
        print "Number of nodes in reduction end graph valid." 
    
    if args.intermediate_points:
        if args.verbose:
            print "Checking for valid intermediate points."
        check_intermediate(args.intermediate_points, args.end, max_nodes)

    if args.type.lower() == 'kdd' or args.type.lower() == 'kkd':
        if not args.edges:
            sys.stderr.write("Error! KDD or KKD reduction methods must have " +
                    "-e flag set with integer number of edges.\nExiting.\n")
            sys.exit(1)
    else:
        if args.edges:
            sys.stderr.write("Error! Only KDD and KKD reduction methods may " +
                    "have -e flag set.\nExiting.\n")
            sys.exit(1)
    return dhyb_prob

def check_dhyb():
    """
    Parses DHYB type and ensures it is valid
    """
    if args.verbose:
        print "Checking for valid DHYB-0.X format."
    try:
        args.type.split("-")
        prob = args.type.split("-")[1]
        prob = float(prob)
    except:
        sys.stderr.write("DHYB type must be in the form:\nDHYB-0.X\nExiting.\n")
        sys.exit(1)
    args.type = 'dhyb'
    if args.verbose:
        print "Valid DHYB-0.X type found."
    return prob

def check_intermediate(l, end, max_nodes):
    """
    Ensures that the intermediate points in the reduction are strictly greater
    than the reduction endpoint
    """
    if args.type.lower() == 'kdd' or args.type.lower() == 'kkd':
        sys.stderr.write("Error! KDD and KKD cannot take intermediate reduction"
                + " points.\nExiting.\n")
        sys.exit(1)
    else:
        s = set(l) 
        l = sorted(list(s), reverse=True)
    if not (min(l) > end and max(l) < max_nodes):
        sys.stderr.write("Error! Intermediate points must be greater than the" +
                " number of nodes in the reduction endpoint graph and less " +
                "than the number of nodes in the initial instance.\n")
        sys.stderr.write("These intermediate points caused this error:\n")
        bad = [y for y in l if (y <= end or y >= max_nodes)]
        for x in bad: 
            sys.stderr.write(str(x) + " ")
        sys.stderr.write("\n")
        sys.exit(1)
    args.intermediate_points = l
    if args.verbose:
        print "Intermediate reduction points are valid."



parser = argparse.ArgumentParser()
parser.add_argument("graph", help="Initial graph to be reduced in .gexf file format")
parser.add_argument("type", help="Reduction method type -- Options are CRE,\
        CRVE, DRE, DRV, DRVE, DHYB-0.X, EBFS, EDFS, KDD, KKD")
parser.add_argument("end", help="Number of nodes at reduction end", type=int)
parser.add_argument("num_trials", help="Number of reductions with different\
        random seeds", type=int)
parser.add_argument("intermediate_points", help="Intermediate points to write\
        reduced graphs", type=int, nargs="*")
parser.add_argument("-v", "--verbose", help="Increases verbosity",
        action="store_true")
parser.add_argument("-e", "--edges", help="Number of edges for KDD/KKD\
        methods", type=int)
        
args = parser.parse_args()

if args.verbose:
    print "Verbosity is enabled."
print args.edges

dhyb_prob = check_args()

args.intermediate_points.append(args.end)

print "Starting reduction by " + args.type.upper()
if args.type == 'cre':
    CRE.CRE(args.graph, args.intermediate_points, args.num_trials, args.verbose)
elif args.type == 'crve':
    CRVE.CRVE(args.graph, args.intermediate_points, args.num_trials,
            args.verbose)
elif args.type == 'drv':
    DRV.DRV(args.graph, args.intermediate_points, args.num_trials, args.verbose)
elif args.type == 'dre':
    DRE.DRE(args.graph, args.intermediate_points, args.num_trials, args.verbose)
elif args.type == 'drve':
    DRVE.DRVE(args.graph, args.intermediate_points, args.num_trials,
            args.verbose)
elif args.type == 'dhyb':
    DHYB.DHYB(args.graph, args.intermediate_points, args.num_trials,
            dhyb_prob, args.verbose)
elif args.type == 'ebfs':
    EBFS.EBFS(args.graph, sorted(args.intermediate_points), args.num_trials,
            args.verbose)
elif args.type == 'edfs':
    EDFS.EDFS(args.graph, sorted(args.intermediate_points), args.num_trials,
            args.verbose)
elif args.type == 'kdd':
    KDD.KDD(args.graph, sorted(args.intermediate_points), args.num_trials,
            args.edges, args.verbose)
elif args.type == 'kkd':
    KKD.KKD(args.graph, sorted(args.intermediate_points), args.num_trials,
            args.edges, args.verbose)
else:
    sys.stderr.write("Error! Invalid graph reduction method.\nExiting.\n")
    sys.exit(1)
