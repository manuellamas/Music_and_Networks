import networkx as nx
import mido
import sys
import os.path
from os import listdir
import Plotting
import MIDI_general
import Music_Mapping





if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]
    files_directory = parent_directory + "\\SongArena" # Where the MIDI files to be compared are

    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    # Create the Graphs
    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        network = Music_Mapping.graph_note_pairs_weighted(mid_file)
        filename = MIDI_general.midi_filename(mid_file)

        networks.append([network, mid_file, filename])


    ########## Plots ##########
    # Degree Distribution
    Plotting.degree_distribution_comparison_plot(networks)
    Plotting.degree_distribution_comparison_plot(networks, "loglog")
    
    # Betweenness
    Plotting.betwenness_comparison_plot(networks)

    
    diameters = []
    clust_coef = [] # Clustering coefficient

    print("Name", "Diameter", "Clustering Coefficient")
    for network, mid_file, filename in networks:
        diameter = nx.diameter(network)
        clust = nx.clustering(network)

        diameters.append(diameter)
        clust_coef.append(clust)

        print(filename, diameter, clust)


    # SongComparisonOutputFiles