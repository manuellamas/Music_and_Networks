### Set to be ran once per midi file


# Run as "rscript ..\MusicTimeSeriesNetFeatures.R" from NetF's root folder - Not needed with the below line
# Set Working Directory as the NetF main folder
setwd("Code/Music_NetF/NetF")

# To run from Music_NetF
# setwd("NetF")

# Read from a CSV into a list
musicTimeSeries_csv <- scan(file = "../time_series.csv", what = "numeric()", sep = ",")
musicTimeSeries <- as.numeric(musicTimeSeries_csv) # Converting all elements of the list to numeric

musicTimeSeries_matrix <- matrix(musicTimeSeries)

# Load igraph
library(igraph)

# Load Visibility Graphs and Quantile Graphs mapping source files, as well as NetF source
source("ts_mapping.R")
source("net_features.R")



## Getting the graphs (input is a matrix)
musicTimeSeries_NVG_graph <- generate_Graphs(musicTimeSeries_matrix, 1, length(musicTimeSeries_matrix), map_type = "NVG", weight_type = TRUE)
musicTimeSeries_HVG_graph <- generate_Graphs(musicTimeSeries_matrix, 1, length(musicTimeSeries_matrix), map_type = "HVG", weight_type = TRUE)
musicTimeSeries_QG_graph <- generate_Graphs(musicTimeSeries_matrix, 1, length(musicTimeSeries_matrix), q = 4, map_type = "QG", weight_type = TRUE)

## Obtaining features
m_wnvg_Music <- calc_metrics(musicTimeSeries_NVG_graph, 1, map_type = "NVG", weight_type = TRUE)
m_whvg_Music <- calc_metrics(musicTimeSeries_HVG_graph, 1, map_type = "HVG", weight_type = TRUE)
m_wqg_Music <- calc_metrics(musicTimeSeries_QG_graph, 1, map_type = "QG", weight_type = TRUE)

netf_feature_list <- c(m_wnvg_Music, m_whvg_Music, m_wqg_Music)




# Exporting list of features (of the three graphs) to CSV on Music_NetF directory
write.table(as.data.frame(netf_feature_list), file = "../netf_feature_list.csv", quote = F, sep = ",", row.names = F)