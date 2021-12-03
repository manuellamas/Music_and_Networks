import networkx as nx

def multidigraph_unique_edges(G): # Gives the number of unique edges of a graph, i.e., number of directed pairs of nodes that are connected by at least one edge
    if isinstance(G,nx.multidigraph.MultiDiGraph):
        total_unique_edges = 0
        for node in G:
            total_unique_edges += len(G[node]) # Size of G[node] which is a dictionary. And multiple edges are contained in the same entry (which is also a dictionary). Section 1.7 of NetworkX reference
        return total_unique_edges
    else:
        print("This graph is not a MultiDiGraph")
        return G.number_of_edges()