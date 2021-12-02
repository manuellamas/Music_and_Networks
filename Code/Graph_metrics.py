import networkx as nx

def multidigraph_unique_edges(G): # Gives the number of unique edges of a graph, i.e., number of directed pairs of nodes that are connected by at least one edge
    if isinstance(G,nx.multidigraph.MultiDiGraph):
        
        return
    else:
        print("This graph is not a MultiDiGraph")
        return G.number_of_edges()