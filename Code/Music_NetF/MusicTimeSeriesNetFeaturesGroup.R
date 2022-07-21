### Set to be ran once for all (specified) midi files


# Run as "rscript ..\MusicTimeSeriesNetFeaturesGroup.R" from NetF's root folder - Not needed with the below line
# Set Working Directory as the NetF main folder
setwd("Code/Music_NetF/NetF")

# To run from Music_NetF
# setwd("NetF")

# Reading the first line which contains the number of quantiles to be used on the QVG
quantile_number_csv <- read.csv(file = "../time_series_group.csv", header = FALSE, sep = ",", nrows = 1)
quantile_number <- quantile_number_csv[1, 1]

# Read from a CSV into a table (skipping the first line)
musicTimeSeriesGroup_table <- read.csv(file = "../time_series_group.csv", header = FALSE, sep = ",", skip = 1)



# Load igraph
library(igraph)

# Load Visibility Graphs and Quantile Graphs mapping source files, as well as NetF source
source("ts_mapping.R")
source("net_features.R")





## Obtain number of rows (to know how many time series we're working on)
num_rows <- nrow(musicTimeSeriesGroup_table)

net_data_frame <- data.frame(matrix(ncol = 15, nrow = 0))
# colnames(df) <- c('var1', 'var2', 'var3') # The 15 features, 5 for each graph


## Work with each Time Series by accessing one row of the table at a time
for (i in seq(num_rows)) {
    musicTimeSeriesGroup_numeric <- as.numeric(musicTimeSeriesGroup_table[i, ]) # Convert row to list
    musicTimeSeriesGroup_matrix <- matrix(musicTimeSeriesGroup_numeric) # Converting to Matrix
    musicTimeSeriesGroup_matrix <- na.omit(musicTimeSeriesGroup_matrix) # Removes rows with NA
    attributes(musicTimeSeriesGroup_matrix)$na.action <- NULL # Removing na.action attribute (that whould show which rows have been removed)


    ## Getting the graphs (input is a matrix)
    musicTimeSeries_NVG_graph <- generate_Graphs(musicTimeSeriesGroup_matrix, 1, length(musicTimeSeriesGroup_matrix), map_type = "NVG", weight_type = TRUE)
    musicTimeSeries_HVG_graph <- generate_Graphs(musicTimeSeriesGroup_matrix, 1, length(musicTimeSeriesGroup_matrix), map_type = "HVG", weight_type = TRUE)
    musicTimeSeries_QG_graph <- generate_Graphs(musicTimeSeriesGroup_matrix, 1, length(musicTimeSeriesGroup_matrix), q = quantile_number, map_type = "QG", weight_type = TRUE)


    ## Obtaining features
    m_wnvg_Music <- calc_metrics(musicTimeSeries_NVG_graph, 1, map_type = "NVG", weight_type = TRUE)
    m_whvg_Music <- calc_metrics(musicTimeSeries_HVG_graph, 1, map_type = "HVG", weight_type = TRUE)
    m_wqg_Music <- calc_metrics(musicTimeSeries_QG_graph, 1, map_type = "QG", weight_type = TRUE)

    # print(is.na(m_wqg_Music[["d"]]))
    # print(is.nan(m_wqg_Music[["d"]]))

    # Convert NA / NaN values to 0, when it is not possible to calculate average path length
    if (is.na(m_wqg_Music[["d"]])) { # "d" is the average path length entry
            m_wqg_Music[["d"]] <- 0
        }

    netf_feature_list <- c(m_wnvg_Music, m_whvg_Music, m_wqg_Music)

    net_data_frame[nrow(net_data_frame) + 1, ] <- netf_feature_list

}

# Add more rows or columns depending on which one it netf_feature_list has


# So this isn't a table but a list. Can I write
# Below however it converts it to a data frame. Can I use that? Can that have several rows?


# net_data_frame <- as.data.frame(netf_feature_list)
# net_data_frame[nrow(net_data_frame) + 1, ] <- netf_feature_list

# net_data_frame


# net_data_frame




# # Exporting list of features (of the three graphs) to CSV on Music_NetF directory
write.table(as.data.frame(net_data_frame), file = "../netf_group_feature_list.csv", quote = F, sep = ",", row.names = F)