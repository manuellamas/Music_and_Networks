""" Plotting functions related to the Analysis via Time Series """

import config

import matplotlib.pyplot as plt

def simple_time_series_plot(series, filename):
    # Scatter plot
    fig1, ax1 = plt.subplots()

    x = []
    y = []
    for value, time_stamp in series[:300]: # Showing just the first 300 values
        x.append(time_stamp)
        y.append(value)

    # ax1.scatter(x,y) # Scatter Plot
    ax1.plot(x,y) # Line

    export_location = "\\Plots\\Time_Series\\" + filename + "_TimeSeries" + ".png"

    plt.savefig(config.ROOT + export_location)
    plt.close()
    print("Plot at", export_location)
    