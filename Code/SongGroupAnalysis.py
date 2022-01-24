""" Analyze several songs by resorting to Data Science tools, K-means,... """

import networkx as nx
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import Graph_metrics

def music_data(G):
    """ From a network obtains a list of features to be compared to other songs """
    feature_list = [] # average degree, average betweenness, average closeness, average clustering coef

    feature_list.append(Graph_metrics.average_degree(G))
    feature_list.append(Graph_metrics.average_betweenness(G))
    feature_list.append(Graph_metrics.average_closeness(G))
    feature_list.append(Graph_metrics.average_clustering(G))

    return feature_list



def kmeans_analysis(networks_features):
    """ Apply kmeans to the vector of features obtained from the network of the song """


    return




if __name__ == "__main__":
    pass