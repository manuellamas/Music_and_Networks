import matplotlib.pyplot as plt
import numpy as np

import config

def clustering_table(networks, cluster_predictions, model, group_name = "", labels = None, time = False):
    """ Plots a table with the songs/networks and its cluster resulting of the specified model """

    cluster_list = []
    if labels is None:
        for i in range(len(networks)):
            cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename

    else:
        num_clusters = len(np.unique(cluster_predictions))
        list_artists = np.unique(labels)
        num_artists = len(list_artists)
        cluster_artist_count = [[0 for x in range(num_artists)] for x in range(num_clusters)] # Each entry will be a list corresponding to each cluster
        # And in that list will be the count for each artist [artist_a_count, artist_b_count,...]

        # Creating dictionary
        dict_artists = {}
        for i in range(num_artists):
            dict_artists[list_artists[i]] = i # From artist to num

        for i in range(len(networks)):
            cluster_list.append([networks[i][2], cluster_predictions[i], labels[i]]) # filename, labels

            if cluster_predictions[i] != -1: # Not noise points in DBSCAN
                cluster_artist_count[cluster_predictions[i]][dict_artists[labels[i]]] += 1

        cluster_artist = []
        for a in range(num_artists):
            max_value = 0
            max_cluster = -1
            for c in range(num_clusters):
                cluster_artist_count[c][a]
                max_value = max(max_value, cluster_artist_count[c][a])
                if max_value == cluster_artist_count[c][a]:
                    max_cluster = c
            
            cluster_artist.append(max_cluster) # Storing the number of the cluster that corresponds to the artist


    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    color_list = ["#ffffb3", "#ff803e", "#ffff68", "#ffa6bd", "#ffc100", "#ffcea2", "#ff8170"]
    # color_list = ["#ffffb300", "#ff803e75", "#ffff6800", "#ffa6bdd7", "#ffc10020", "#ffcea262", "#ff817066"]
    color_right = "green"
    color_wrong = "red"

    colors = []
    for i in range(len(cluster_predictions)):
        chosen_color = color_list[cluster_predictions[i]]
        if labels is None:
            colors.append([chosen_color, chosen_color])
        else:
            artist_cluster = cluster_artist[dict_artists[labels[i]]] # The cluster corresponding to the artist of the i song

            if artist_cluster == cluster_predictions[i]:
                cluster_color = color_right
            else:
                cluster_color = color_wrong
            colors.append([chosen_color, chosen_color, cluster_color])

    if labels is None:
        columns = ["Song", "Cluster"]
    else:
        columns = ["Song", "Cluster", "Artist/Band"]

    rows = [] #, rowLabels = rows
    tab = ax.table(cellText = cluster_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)

    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below
    tab.set_fontsize(8)
    tab.auto_set_column_width(col=list(range(len(columns)))) # Sets Column width automatically

    fig.tight_layout()

    export_directory = config.ROOT + "\\Plots\\SongGroupAnalysis\\" + group_name + "_" + model + "_clustering.png"


    plt.savefig(export_directory)
    plt.close()
    print("Plot at", export_directory)



def feature_table(network_features, feature_names, file_names, group_name = "", type = None):
    """ Plots a table with all features being analyzed """


    network_feature_list = [[] for i in range(len(network_features))]

    for i in range(len(network_features)): # Going through every song
        # File Name
        network_feature_list[i].append(file_names[i])

        # Features
        network_feature_list[i] += network_features[i] # Adding the features to the list
        
        if len(network_feature_list[i]) != len(feature_names): # For the networks that don't have the length feature for some reason
            network_feature_list[i].append(0)

        for j in range(1, len(network_feature_list[i])): # Rounding Values
            network_feature_list[i][j] = "{:.3f}".format(network_feature_list[i][j])






    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes


    columns = feature_names



    # rows = [] #, rowLabels = rows
    tab = ax.table(cellText = network_feature_list, colLabels = columns, loc = "center", cellLoc = "center")
    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below

    tab.set_fontsize(8)
    tab.auto_set_column_width(col = list(range(len(columns)))) # Sets Column width automatically

    cells = tab.properties()["celld"]

    row_colors = ["white" if i%2 == 0 else "#BFBFBF"  for i in range(len(network_feature_list) + 1)] # A list with alternating colors

    # Aligning the cells of the first column (0) to the left (excluding the header row)
    for i in range(1, len(network_feature_list) + 1): # For each row. +1 because the column headers cells are included
        cells[i, 0].set_text_props(ha = "left") # Aligning column 0 to the left
        cells[i, 0].PAD = 0.05 # Setting padding. Since it's aligned to the left (I think) it's only controlling the padding to the left side (and not up and down as well)
        cells[i, 0].set(fc = row_colors[i]) # Setting alternating colors for better readability


    # Aligning the cells of all columns except the first one(0) to the right (excluding the header row)
    # Overriding the cellLoc = "center"
    for j in range(1, len(columns)):
        for i in range(1, len(network_feature_list) + 1): # For each row. +1 because the column headers cells are included
            cells[i, j].set_text_props(ha = "right") # Aligning column j to the right
            cells[i, j].set(fc = row_colors[i]) # Setting alternating colors for better readability




    fig.tight_layout()

    features_type = "_features"
    if type == "time":
        features_type = "_time_features"
    elif type == "netf":
        features_type = "_netf_features"


    export_directory = config.ROOT + "\\Plots\\SongGroupAnalysis\\" + group_name + features_type + ".png"
    plt.savefig(export_directory, bbox_inches='tight')
    plt.close()
    print("Plot at", export_directory)

    return



def cluster_feature_table(networks, cluster_predictions, model, network_features, feature_names, file_names, type = None, group_name = "", time = False):
    """ Seeing the clustering and the features in the same table """

    cluster_list = []
    for i in range(len(networks)):
        cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename



    network_feature_list = [[] for i in range(len(network_features))]

    for i in range(len(network_features)): # Going through every song
        # File Name
        # network_feature_list[i].append(file_names[i])

        # Features
        network_feature_list[i] += network_features[i] # Adding the features to the list
        
        # if len(network_feature_list[i]) != len(feature_names): # For the networks that don't have the length feature for some reason
        #     network_feature_list[i].append(0)

        for j in range(0, len(network_feature_list[i])): # Rounding Values
            network_feature_list[i][j] = "{:.3f}".format(network_feature_list[i][j])



    # Join cluster_list and network_feature_list
    final_list = []
    for i in range(len(networks)): # Per row
        final_list.append(cluster_list[i] + network_feature_list[i])













    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    color_list = ["#ffffb3", "#ff803e", "#ffff68", "#ffa6bd", "#ffc100", "#ffcea2", "#ff8170"]
    # color_list = ["#ffffb300", "#ff803e75", "#ffff6800", "#ffa6bdd7", "#ffc10020", "#ffcea262", "#ff817066"]
    color_right = "green"
    color_wrong = "red"

    columns = ["Song", "Cluster"] + feature_names[1:] # Removing the Song Column Header (that comes repeated) from feature_names
    # columns = ["Song", "Cluster"] + feature_names # Removing the Song Column Header (that comes repeated) from feature_names

    print(len(columns))

    colors = []
    for i in range(len(final_list)): # For each row
        chosen_color = color_list[cluster_predictions[i]]
        colors.append([chosen_color for i in range(len(columns))])







    rows = [] #, rowLabels = rows
    tab = ax.table(cellText = final_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)

    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below
    tab.set_fontsize(8)
    tab.auto_set_column_width(col=list(range(len(columns)))) # Sets Column width automatically



    cells = tab.properties()["celld"]

    # Aligning the cells of the first column (0) to the left (excluding the header row)
    for i in range(1, len(final_list) + 1): # For each row. +1 because the column headers cells are included
        cells[i, 0].set_text_props(ha = "left") # Aligning column 0 to the left
        cells[i, 0].PAD = 0.05 # Setting padding. Since it's aligned to the left (I think) it's only controlling the padding to the left side (and not up and down as well)
        # cells[i, 0].set(fc = row_colors[i]) # Setting alternating colors for better readability


    # Aligning the cells of all columns except the first one(0) to the right (excluding the header row)
    # Overriding the cellLoc = "center"
    for j in range(1, len(columns)):
        for i in range(1, len(network_feature_list) + 1): # For each row. +1 because the column headers cells are included
            cells[i, j].set_text_props(ha = "right") # Aligning column j to the right
            # cells[i, j].set(fc = row_colors[i]) # Setting alternating colors for better readability




    fig.tight_layout()

    export_directory = config.ROOT + "\\Plots\\SongGroupAnalysis\\" + group_name + "_" + model + "_clusteringAndFeatures.png"


    plt.savefig(export_directory, bbox_inches =  "tight")
    plt.close()
    print("Plot at", export_directory)    
    
    return