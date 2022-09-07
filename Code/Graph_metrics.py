import networkx as nx
import networkx.algorithms.community as nx_comm

# def count_self_loops(G):
#     """ Counts the number of self loops in a graph """
#     num_self_loops = 0

#     for edge in list(G.edges()):
#         if edge[0] == edge[1]:
#             num_self_loops += 1

#     # return 0
#     return num_self_loops

def multidigraph_unique_edges(G):
    """ Gives the number of unique edges of a graph, i.e., number of directed pairs of nodes that are connected by at least one edge """

    if isinstance(G,nx.multidigraph.MultiDiGraph):
        total_unique_edges = 0
        for node in G:
            total_unique_edges += len(G[node]) # Size of G[node] which is a dictionary. And multiple edges are contained in the same entry (which is also a dictionary). Section 1.7 of NetworkX reference
        return total_unique_edges
    else:
        print("This graph is not a MultiDiGraph")
        return G.number_of_edges()


def list_betweenness_centrality(G, normalize = False, weighted = False):
    """ Returns a list with all betweenness centrality values """

    if weighted:
        betw_values = nx.betweenness_centrality(G, normalized = normalize, weight = "weight") # Using weight
    else:
        betw_values = nx.betweenness_centrality(G, normalized = normalize, weight = None)

    rounded_values = []

    for node, value in betw_values.items():
        rounded = round(value, 2) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values

def list_closeness_centrality(G, weighted = False):
    """ Returns a list with all closeness centrality values """

    if weighted:
        centr_values = nx.closeness_centrality(G, distance = "weight")
    else:
        centr_values = nx.closeness_centrality(G)


    rounded_values = []

    for node, value in centr_values.items():
        rounded = round(value, 5) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values

def list_clustering_coefficient(G):
    """ Returns a list with all the clustering coefficient values """
    clust_values = nx.clustering(G)

    rounded_values = []

    for node, value in clust_values.items():
        rounded = round(value, 2) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values


##################
# Average values #
##################

def average_indegree(G, normalize = False, weighted = False):
    """ Returns the average in-degree of a node (ignoring weight) """
    total_degree = 0

    if weighted:
        for node, degree in G.in_degree(weight = "weight"): # Summing in-degrees. Since it's weighted the total can be anything >= 0
            total_degree += degree

        # Normalizing by the dataset, so it's done after all features have been collected

        if normalize:
            total_degree = total_degree/(G.number_of_nodes()) # For Directed Unweighted Grahs (with loops)
        #     # total_degree = total_degree/(G.number_of_nodes() - 1) * G.number_of_nodes() # For Undirected (Unweighted) Graphs

    else:
        for node, degree in G.in_degree(weight = None): # Summing in-degrees. Since we're allowing self-loops the total degree ranges from [0,n^2], n being the total number of nodes
            total_degree += degree

        if normalize:
            total_degree = total_degree/(G.number_of_nodes()) # For Directed Unweighted Grahs
            # total_degree = total_degree/(129**2) # Dividing for the entire number of pairs between all possible notes. Because all graphs will be within this


    total_degree /= G.number_of_nodes() # The average of the values
    return total_degree


def average_betweenness(G, normalize = False, weighted = False):
    """ Returns the average betweenness centrality of a node """
    total = 0
    between_list = list_betweenness_centrality(G, normalize = normalize, weighted = weighted)

    for value in between_list:
        total += value

    if not weighted and total/len(between_list) > 1:
        print("Avg Bet Higher than 1")

    # Get the average value
    total /= G.number_of_nodes()

    return total


def average_closeness(G, weighted = False):
    """ Returns the average closeness centrality of a node """
    total = 0
    closeness_list = list_closeness_centrality(G, weighted = weighted)

    for value in closeness_list:
        total += value

    if total/len(closeness_list) > 1:
        print("Avg Clos Higher than 1")
    return total/len(closeness_list)


def average_clustering(G):
    """ Returns the average clustering coefficient of a node """
    total = 0
    clustering_list = list_clustering_coefficient(G)

    for value in clustering_list:
        total += value

    if total/len(clustering_list) >= 1:
        print("Avg Clust Higher than 1")
    return total/len(clustering_list)


# Modularity


def modularity_louvain(G):
    """ Returns modularity value from communities (Louvain Algorithm) """

    G_undirected = nx.to_undirected(G) # Using an undirected version of the graph

    # Obtain Communities
    # print("If the program stopped it's stuck at the louvain_communities algorithm")
    communities = nx_comm.louvain_communities(G_undirected, seed = 123)
    # communities = nx_comm.girvan_newman(G)

    # Modularity value based on those communities
    modularity = nx_comm.modularity(G_undirected, communities)

    return modularity, len(communities)
# Then return this as a feature in SongGroupAnalysis