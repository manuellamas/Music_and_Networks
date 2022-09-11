import matplotlib.pyplot as plt
import numpy as np

from Plotting import check_dir, interval_mapping

import config




def feature_table(network_features, feature_names, file_names, files_directory, model = None):
    """ Plots a table with all features being analyzed """


    network_feature_list = [[] for i in range(len(network_features))]

    for i in range(len(network_features)): # Going through every song
        # File Name
        # network_feature_list[i].append(file_names[i])
        network_feature_list[i].append(file_names[i])

        # Features
        network_feature_list[i] += network_features[i] # Adding the features to the list
        
        if len(network_feature_list[i]) != len(feature_names): # For the networks that don't have the length feature for some reason
            network_feature_list[i].append(0)


    # Making a different list because the values as numbers will be used for the ordering of the colours
    # To round values in text to appear in the table
    network_feature_list_text = [x[:] for x in network_feature_list] # For a deep copy we need to copy the nested lists and not just the "main" list

    for i in range(len(network_features)): # Going through every song
        for j in range(1, len(network_feature_list_text[i])): # Rounding Values
            network_feature_list_text[i][j] = "{:.3f}".format(network_feature_list_text[i][j])






    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes


    columns = feature_names



    # rows = [] #, rowLabels = rows
    tab = ax.table(cellText = network_feature_list_text, colLabels = columns, loc = "center", cellLoc = "center")
    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below

    tab.set_fontsize(8)
    tab.auto_set_column_width(col = list(range(len(columns)))) # Sets Column width automatically

    ##########
    # Colors #
    ##########

    num_songs = len(network_feature_list)
    num_features = len(network_feature_list[0]) # Any index would do


    min_feature_values = []
    max_feature_values = []
    for j in range(1, num_features): # Columns
        min_value = network_feature_list[0][j]
        max_value = network_feature_list[0][j]

        for i in range(num_songs): # Rows
            # Song i, Feature j
            min_value = min(min_value, network_feature_list[i][j])
            max_value = max(max_value, network_feature_list[i][j])

        min_feature_values.append(min_value)
        max_feature_values.append(max_value)





    # A Matrix with len(network_feature_list) + 1 rows and len(columns) columns
    cell_colors = [[[] for j in range(len(columns))] for i in range(len(network_feature_list) + 1)]

    for col_index in range(len(columns)): # Features
        for row_index in range(1, len(network_feature_list) + 1): # Songs
            if col_index == 0:
                cell_colors[row_index][col_index] = "white"

            else:
                # Mapping the value from [min,max] to [1,0] because for (1,1,1) we get white (min_value) and for (1,1,0) we get "full" red (max_value)
                color_value = interval_mapping(network_feature_list[row_index - 1][col_index] ,[min_feature_values[col_index - 1], max_feature_values[col_index - 1]], [1, 0]) # col_index - 1 to skip the first column (without numbers) and row_index because it's considering the headers. It needs some clarity... pni

                cell_colors[row_index][col_index] = (1, color_value, color_value) # Red with varying (at the same "pace") Green and Blue



    tab = modify_table(tab, num_rows = len(network_feature_list), num_columns =  len(columns), cell_colors = cell_colors)

    # To alternate colors for readability
    # row_colors = ["white" if i%2 == 0 else "#BFBFBF"  for i in range(len(network_feature_list) + 1)] # A list with alternating colors
    # tab = modify_table(tab, num_rows = len(network_feature_list), num_columns =  len(columns), row_colors = row_colors)
    

    # fig.tight_layout()


    ###################
    # Exporting Image #
    ###################

    # Adapting plot filename to the model
    features_type = "_features"
    if model == "time":
        features_type = "_time_features"
    elif model == "netf":
        features_type = "_netf_features"

    # Getting the folder's name
    group_name = files_directory.rsplit("\\")[-1]

    # Creating the directory if it doesn't already exist
    export_directory = files_directory + "\\FeatureAnalysis"
    check_dir(export_directory)

    # Setting the plot file name and the full path of the file to be created with it
    plot_filename = group_name + features_type + ".png"
    export_directory += "\\" + plot_filename

    # Saving and closing the file
    plt.savefig(export_directory, bbox_inches='tight')
    plt.close()
    print("Plot at", export_directory)

    return



def cluster_feature_table(networks, cluster_predictions, model, network_features, feature_names, files_directory = ""):
    """ Seeing the clusters and the features in the same table """

    cluster_list = []
    for i in range(len(networks)):
        cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename



    network_feature_list = [[] for i in range(len(network_features))]

    for i in range(len(network_features)): # Going through every song
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


    colors = []
    for i in range(len(final_list)): # For each row
        chosen_color = color_list[cluster_predictions[i]]
        colors.append([chosen_color for i in range(len(columns))])







    rows = [] #, rowLabels = rows
    tab = ax.table(cellText = final_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)

    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below
    tab.set_fontsize(8)
    tab.auto_set_column_width(col=list(range(len(columns)))) # Sets Column width automatically


    tab = modify_table(tab, num_rows = len(final_list), num_columns = len(columns))

    fig.tight_layout()


    ###################
    # Exporting Image #
    ###################

    # Adapting plot directory according to files_directory
    if files_directory == "":
        export_directory = config.ROOT + "\\Plots\\SongGroupAnalysis" + plot_filename
        group_name = ""
    else:
        export_directory = files_directory + "\\SongGroupAnalysis"
        group_name = files_directory.rsplit("\\",1)[-1]

    check_dir(export_directory)

    plot_filename = group_name + "_" + model + "_clusteringAndFeatures.png"


    plt.savefig(export_directory + "\\" + plot_filename, bbox_inches =  "tight")
    plt.close()
    print("Plot at", export_directory + "\\" + plot_filename)
    
    return



def clustering_table(networks, cluster_predictions, model, files_directory, labels = None, time = False):
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

    # Export to PNG
    group_name = files_directory.rsplit("\\",1)[-1]
    export_directory = files_directory + "\\SongGroupAnalysis"
    check_dir(export_directory)

    plot_filename = group_name + "_" + model + "_clustering.png"

    plt.savefig(export_directory + "\\" + plot_filename)
    plt.close()
    print("Plot at", export_directory + "\\" + plot_filename)



#####################
# Support Functions #
#####################

def modify_table(tab, num_rows, num_columns, row_colors = None, cell_colors = None):
    cells = tab.properties()["celld"]

    # cell_colors has indices [0, num_rows + 1][0, num_columns] So, including header
    # num_rows should be changed to match the total number of rows, just like num_columns is

    CELL_HEIGHT = 0.055

    # First column (0) (excluding the header row)
    for i in range(1, num_rows + 1): # For each row. +1 because the column headers cells are included
        cells[i, 0].set_text_props(ha = "left") # Aligning column 0 to the left
        cells[i, 0].PAD = 0.05 # Setting padding. Since it's aligned to the left (I think) it's only controlling the padding to the left side (and not up and down as well)
        if row_colors is not None:
            cells[i, 0].set(fc = row_colors[i]) # Setting alternating colors for better readability
        elif cell_colors is not None:
            cells[i, 0].set(fc = cell_colors[i][0]) # Setting colors for...
        cells[i,0].set(height = CELL_HEIGHT) # Adjust Cell's height


    # All columns except the first one(0) (excluding the header row)
    # Overriding the cellLoc = "center"
    for j in range(1, num_columns):
        for i in range(1, num_rows + 1): # For each row. +1 because the column headers cells are included
            cells[i, j].set_text_props(ha = "center") # Aligning column j to the center
            if row_colors is not None:
                cells[i, j].set(fc = row_colors[i]) # Setting alternating colors for better readability
            elif cell_colors is not None:
                cells[i, j].set(fc = cell_colors[i][j]) # Setting colors for...
            cells[i,j].set(height = CELL_HEIGHT) # Adjust Cell's height

    return tab