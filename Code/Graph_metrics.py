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


def list_betweenness_centrality(G):
    """ Returns a list with all betweenness centrality values """
    betw_values = nx.betweenness_centrality(G, normalized = True, weight = "weight")
    print(type(betw_values))

    rounded_values = []

    for node, value in betw_values.items():
        rounded = round(value, 2) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values

def list_closeness_centrality(G):
    """ Returns a list with all closeness centrality values """
    centr_values = nx.closeness_centrality(G, distance = "weight")

    rounded_values = []

    for node, value in centr_values.items():
        rounded = round(value, 2) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values

def average_degree(G):
    """ Returns the average degree of a graph (ignoring weight) """
    total_degree = 0
    for node, degree in G.degree():
        total_degree += degree

    return total_degree/G.number_of_nodes()