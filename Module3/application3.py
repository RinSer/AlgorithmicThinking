#!/usr/bin/env python
"""
This is my implementation of Application #3 from 
the Algorithmic thinking course.

created by RinSer
"""

import random
import time
import project3
from cluster import Cluster as Cluster
import matplotlib.pyplot as plot
import csv
import project3_viz as data


def initialize_cluster_list(data_table):
    """
    Helper function to initialize a list of clusters.
    Takes a data table as input.
    Returns a list of clusters.
    """
    cluster_list = list()
    for row in data_table:
        cluster_list.append(Cluster(set([row[0]]), row[1], row[2], row[3], row[4]))
    return cluster_list


def gen_random_clusters(num_clusters):
    """
    Creates a list of clusters where each cluster 
    corresponds to one randomly generated point in
    the square with corners (+-1, +-1).
    Takes the number of clusters as input.
    Returns a list of random clusters.
    """
    clusters = list()
    for idx_c in range(num_clusters):
        # Initialize random coordinates
        x_coordinate = random.uniform(-1, 1)
        y_coordinate = random.uniform(-1, 1)
        # Initialize random cluster and add it
        new_cluster = Cluster(0, x_coordinate, y_coordinate, 0, 0)
        clusters.append(new_cluster)
    return clusters


def compute_distortion(cluster_list, data_table):
    """
    Takes a list of clusters and uses cluster_error to compute its distortion.
    Returns the destortion value.
    """
    # Compute the distortion
    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion


# Question 1
def Question1():
    """
    Computes the running times of the functions slow_closest_pair and fast_closest_pair
    for lists of clusters of size 2 to 200 and plots them.
    """
    number_of_clusters = list()
    slow_times = list()
    fast_times = list()
    for idx_l in range(2, 201):
        number_of_clusters.append(idx_l)
        # Create a list of random clusters
        test_clusters = gen_random_clusters(idx_l)
        # Test slow_closest_pair function
        slow_start = time.time()
        project3.slow_closest_pair(test_clusters)
        slow_stop = time.time()
        slow_times.append(slow_stop-slow_start)
        # Test fast_closest_pair function
        fast_start = time.time()
        project3.fast_closest_pair(test_clusters)
        fast_stop = time.time()
        fast_times.append(fast_stop-fast_start)
    # Draw the plots
    plot.plot(number_of_clusters, slow_times, 'b', label='slow_closest_pair')
    plot.plot(number_of_clusters, fast_times, 'r', label='fast_closest_pair')
    plot.legend()
    plot.title("Fast and slow closest pair functions' running time comparison")
    plot.xlabel("Number of clusters")
    plot.ylabel("Running time")
    plot.grid(True)
    plot.savefig("q1.png")
    plot.close()
    return "The comparison graph has been saved as q1.png"


# Question 7
def Question7(data_url):
    """
    Helper function for Question 7.
    """
    # Initial data table
    data_table = data.load_data_table(data_url)
    # Hierarchical clustering
    clusters = initialize_cluster_list(data_table)
    hierarchical_clusters = project3.hierarchical_clustering(clusters, 9)
    hierarchical_distortion = compute_distortion(hierarchical_clusters, data_table)
    print "Hierarchical clustering distortion: "+str(hierarchical_distortion)
    # K-means clustering
    clusters = initialize_cluster_list(data_table)
    kmeans_clusters = project3.kmeans_clustering(clusters, 9, 5)
    kmeans_distortion = compute_distortion(kmeans_clusters, data_table)
    print "K-means clustering distortion: "+str(kmeans_distortion)
    return (hierarchical_distortion, kmeans_distortion)
    

# Question 10
def Question10(data_url, number_of_counties, output_name):
    """
    Helper function for Question 10.
    """
    # Data set
    data_table = data.load_data_table(data_url)
    # Hierarchical clustering
    clusters = initialize_cluster_list(data_table)
    hierarchical_distortions = list()
    hierarchical_clusters = project3.hierarchical_clustering(clusters, 20)
    hierarchical_distortion = compute_distortion(hierarchical_clusters, data_table)
    hierarchical_distortions.append(hierarchical_distortion)
    for idx_l in range(19, 5, -1):
        hierarchical_clusters = project3.hierarchical_clustering(clusters, idx_l)
        hierarchical_distortion = compute_distortion(hierarchical_clusters, data_table)
        hierarchical_distortions = [hierarchical_distortion] + hierarchical_distortions
    # K-means clustering
    clusters = initialize_cluster_list(data_table)
    kmeans_distortions = list()
    number_of_clusters = list()
    for idx_l in range(6, 21):
        number_of_clusters.append(idx_l)
        kmeans_clusters = project3.kmeans_clustering(clusters, idx_l, 5)
        kmeans_distortions.append(compute_distortion(kmeans_clusters, data_table))
    # Draw the plots
    plot.plot(number_of_clusters, hierarchical_distortions, 'r', label="Hierarchical distortions")
    plot.plot(number_of_clusters, kmeans_distortions, 'b', label="K-means distortions")
    plot.legend()
    plot.title("Comparison of clustering distortions for "+str(number_of_counties)+" counties data set", fontdict={'fontsize':'small'})
    plot.xlabel("Number of clusters")
    plot.ylabel("Distortion value")
    plot.grid(True)
    plot.savefig(output_name)
    plot.close()
    return "The comparison graph has been saved as "+output_name
    

#Question7(data.DATA_111_URL)
print Question10(data.DATA_111_URL, 111, "q10_111.png")
print Question10(data.DATA_290_URL, 290, "q10_290.png")
print Question10(data.DATA_896_URL, 896, "q10_896.png")
