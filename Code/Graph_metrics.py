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

def multidigraph_unique_edges(G): # Gives the number of unique edges of a graph, i.e., number of directed pairs of nodes that are connected by at least one edge
    if isinstance(G,nx.multidigraph.MultiDiGraph):
        total_unique_edges = 0
        for node in G:
            total_unique_edges += len(G[node]) # Size of G[node] which is a dictionary. And multiple edges are contained in the same entry (which is also a dictionary). Section 1.7 of NetworkX reference
        return total_unique_edges
    else:
        print("This graph is not a MultiDiGraph")
        return G.number_of_edges()


def list_betweenness_centrality(G, normalize = False):
    """ Returns a list with all betweenness centrality values """
    betw_values = nx.betweenness_centrality(G, normalized = normalize, weight = "weight")

    rounded_values = []

    for node, value in betw_values.items():
        rounded = round(value, 2) # Pay attention to how much rounding is useful to do to obtain 'meaningful' info from the data
        rounded_values.append(rounded)

    return rounded_values

def list_closeness_centrality(G, normalize = False):
    """ Returns a list with all closeness centrality values (normalized) """
    centr_values = nx.closeness_centrality(G, distance = "weight")

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

def average_indegree(G, normalize = False):
    """ Returns the average in-degree of a node (ignoring weight) """
    total_degree = 0
    for node, degree in G.in_degree(): # Summing in degrees. Since we're allowing self-loops the total degree ranges from [0,n^2], n being the total number of nodes
        total_degree += degree

    if normalize:
        total_degree = total_degree/(G.number_of_nodes()**2)

    # if total_degree > 1:
    #     print("Avg Deg Higher than 1")
    #     print("Num Self-loops", count_self_loops(G))
    #     print(total_degree, G.number_of_nodes())
    #     for node, degree in G.degree():
    #         print(degree)


    return total_degree/G.number_of_nodes()


def average_betweenness(G, normalize = False):
    """ Returns the average betweenness centrality of a node """
    total = 0
    between_list = list_betweenness_centrality(G, normalize = normalize)

    for value in between_list:
        total += value

    if total/len(between_list) > 1:
        print("Avg Bet Higher than 1")
    return total/len(between_list)


def average_closeness(G, normalize = False):
    """ Returns the average closeness centrality of a node """
    total = 0
    closeness_list = list_closeness_centrality(G)

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
    print("If the program stopped it's stuck at the louvain_communities algorithm")
    communities = nx_comm.louvain_communities(G_undirected, seed = 123)
    # communities = nx_comm.girvan_newman(G)
    print(communities)

    # Modularity value based on those communities
    modularity = nx_comm.modularity(G_undirected, communities)
    print(modularity)

    return modularity
# Then return this as a feature in SongGroupAnalysis