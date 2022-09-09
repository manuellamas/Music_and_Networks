""" Display the values of a set of Features (metrics) on a dataset of MIDI files """

# Similar to how SongGroupAnalysis work
# But this time make the code more readable, compact and modular
# One Function One Action whenever possible

# Remember that I'll also use this (or at least have a function that uses this) for the tests with the Random Models.
# Where I'll create n instances of it and take the average and standard deviation and show it.

# Test exporting it as SVG so that there's better quality on the LaTeX file^
# It should only need minor adaptations
# [python - How can I get the output of a matplotlib plot as an SVG? - Stack Overflow](https://stackoverflow.com/questions/24525111/how-can-i-get-the-output-of-a-matplotlib-plot-as-an-svg)





# Move music_data() to here


def feature_analysis():
    """ Displaying a set of features for a dataset """


    return



def normalize_min_max(feature_list, feature_names, features_to_normalize):
    """ Normalizes features given the min and max of its values on a dataset """
    
    # Setting which features will be normalized given the names on the list features_to_normalize
    feature_indices_to_norm = []
    for i, feature in enumerate(feature_names[1:]):
        if feature in features_to_normalize:
            feature_indices_to_norm.append(i)


    for feature_index in feature_indices_to_norm: # Per Feature to be normalized
        # Finding the min and max values
        min_feature_value = feature_list[0][feature_index]
        max_feature_value = feature_list[0][feature_index]
        for i in range(1, len(feature_list)): # Per Song
            song_feature_value = feature_list[i][feature_index]
            min_feature_value = min(min_feature_value, song_feature_value)
            max_feature_value = max(max_feature_value, song_feature_value)
        
        # Normalizing
        for i in range(len(feature_list)): # Per Song
            feature_list[i][feature_index] -= min_feature_value
            feature_list[i][feature_index] /= (max_feature_value - min_feature_value)

    return feature_list



if __name__ == "__main__":
    pass