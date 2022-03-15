import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import config

import MIDI_general


def time_window_metric_plot(metric, time_interval, time_skip, filename, metric_name_list, program = None):
    metric_title, metric_filename = metric_name_list # A title and a (shorter) plot filename

    x_axis = []
    time_window_center = time_interval/2 # The moment (tick) at the center of the current window
    for i in range(len(metric)):
        x_axis.append(time_window_center) # The time window is centered on this time (tick)
        time_window_center += time_skip

    fig1, ax1 = plt.subplots()

    # Design
    if program is None:
        title = metric_title + " - " + filename
    else:
        program_category, program_instrument = MIDI_general.midi_program_num_to_name(program, instrument = True)
        title = metric_title + " - " + filename + "\n" + program_category + " - " + program_instrument
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Center Tick') # The center time (tick) of the window being analyzed
    ax1.set_ylabel(metric_title)

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # y_max = max(10, max(metric)) # Making it 10 on all plots so that we can compare, unless the maximum value is greater than tat
    # y_max = max(metric)
    y_max = 1
    plt.ylim([0, y_max + y_max/10 ]) # Forces the y axis to show only values on the speficied interval. y_max/10 is just a margin for better visibility
    plt.scatter(x_axis, metric, s=10)

    plot_parameters = "_I-" + str(time_interval) + "_S-" + str(time_skip)
    # export_location = "\\Plots\\Time_Window\\" + filename + "_" + metric_filename + plot_parameters + ".png"
    export_location = "\\Plots\\Time_Window\\" + metric_filename + "_" + filename + "_" + metric_filename + plot_parameters + ".png"

    plt.savefig(config.ROOT + export_location)
    # plt.savefig(config.ROOT + "\\Plots\\Time_Window\\Average_Distribution_" + filename + ".png")
    print("Plot at", export_location)
    plt.close()

    return



def time_window_several_metrics_plot(metrics_list, time_interval, time_skip, filename, program = None):
    x_axis = []
    time_window_center = time_interval/2 # The moment (tick) at the center of the current window
    for i in range(len(metrics_list[0])): # Checking the first metric but they should all have the same length
        x_axis.append(time_window_center) # The time window is centered on this time (tick)
        time_window_center += time_skip

    fig1, ax1 = plt.subplots()

    # Design
    if program is None:
        title = "Metrics" + " - " + filename
    else:
        program_category, program_instrument = MIDI_general.midi_program_num_to_name(program, instrument = True)
        title = "Metrics" + " - " + filename + " - " + program_category + ", " + program_instrument
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Center Tick') # The center time (tick) of the window being analyzed
    ax1.set_ylabel('Metrics')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True)) # Sets the ticks to only be integers


    max_metrics = [max(m) for m in metrics_list] # List with the max value of each metric
    plt.ylim([0, max(10, max(max_metrics))]) # Forces the y axis to show only values on the speficied interval. Making it 10 on all plots so that we can compare, unless the maximum value is greater than tat

    plt.scatter(x_axis, metrics_list[0], s=10)
    plt.scatter(x_axis, metrics_list[1], s=10)
    plt.scatter(x_axis, metrics_list[2], s=10)
    plt.scatter(x_axis, metrics_list[3], s=10)

    plot_parameters = "_I-" + str(time_interval) + "_S-" + str(time_skip)
    export_location = "\\Plots\\Time_Window\\" + filename + "_Metrics" + plot_parameters + ".png"

    plt.savefig(config.ROOT + export_location)
    # plt.savefig(config.ROOT + "\\Plots\\Time_Window\\Average_Distribution_" + filename + ".png")
    plt.close()
    print("Plot at", export_location)


    return