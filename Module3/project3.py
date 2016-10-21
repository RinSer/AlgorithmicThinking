"""
My implementation of the Algorithmic thinking 
project #3.

created by RinSer
"""

from cluster import Cluster as Cluster
import csv
import math



def set_of_county_tuples(cluster_list):
    """
    Input: A list of Cluster objects
    Output: Set of sorted tuple of counties corresponds to counties in each cluster
    """
    set_of_clusters = set([])
    for cluster in cluster_list:
        counties_in_cluster = cluster.fips_codes()
        
        # convert to immutable representation before adding to set
        county_tuple = tuple(sorted(list(counties_in_cluster)))
        set_of_clusters.add(county_tuple)
    return set_of_clusters


def slow_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a closest pair where the pair is represented by the tuple (dist, idx1, idx2) with idx1 < idx2 where dist is the distance between the closest pair cluster_list[idx1] and cluster_list[idx2].
    Returns tuple (dist, idx1, idx2).
    """
    distance = float('inf')
    idx1 = -1
    idx2 = -1
    for idx_i in range(len(cluster_list)):
        for idx_j in range(len(cluster_list)):
            if idx_i != idx_j:
                ij_distance = cluster_list[idx_i].distance(cluster_list[idx_j])
                if ij_distance < distance:
                    distance = ij_distance
                    if idx_i < idx_j:
                        idx1 = idx_i
                        idx2 = idx_j
                    else:
                        idx1 = idx_j
                        idx2 = idx_i
    return (distance, idx1, idx2)


def fast_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a closest pair where the pair is represented by the tuple (dist, idx1, idx2) with idx1 < idx2 where dist is the distance between the closest pair cluster_list[idx1] and cluster_list[idx2].
    Returns tuple (dist, idx1, idx2).
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    list_length = len(cluster_list)
    if list_length < 4:
        return slow_closest_pair(cluster_list)
    else:
        # Find the smallest distances in two set halfs
        list_middle = list_length/2
        left_half = cluster_list[:list_middle]
        right_half = cluster_list[list_middle:]
        left_tuple = fast_closest_pair(left_half)
        right_tuple = fast_closest_pair(right_half)
        if left_tuple[0] < right_tuple[0]:
            closest_pair = left_tuple
        else:
            closest_pair = (right_tuple[0], right_tuple[1]+list_middle, right_tuple[2]+list_middle)
        middle_strip = (cluster_list[list_middle-1].horiz_center()+cluster_list[list_middle].horiz_center())/2
        # Find the smallest distance in the set center
        strip_pair = closest_pair_strip(cluster_list, middle_strip, closest_pair[0])
        # Find the final closest pair
        if strip_pair[0] < closest_pair[0]:
            closest_pair = strip_pair
        return closest_pair


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Takes a list of Cluster objects and two floats horiz_center and half_width. horiz_center specifies the horizontal position of the center line for a vertical strip. half_width specifies the maximal distance of any point in the strip from the center line.
    Returns tuple (dist, idx1, idx2).
    """
    closest_points = list()
    for cluster in cluster_list:
        if abs(cluster.horiz_center()-horiz_center) < half_width:
            closest_points.append((cluster, cluster_list.index(cluster)))
    closest_points.sort(key = lambda cluster: cluster[0].vert_center())
    length = len(closest_points)
    distance = float('inf')
    idx1 = -1
    idx2 = -1
    for idx_u in range(length-1):
        for idx_v in range(idx_u+1, min(idx_u+4, length)):
            uv_distance = closest_points[idx_u][0].distance(closest_points[idx_v][0])
            if uv_distance < distance:
                distance = uv_distance
                if closest_points[idx_u][1] < closest_points[idx_v][1]:
                    idx1 = closest_points[idx_u][1]
                    idx2 = closest_points[idx_v][1]
                else:
                    idx1 = closest_points[idx_v][1]
                    idx2 = closest_points[idx_u][1]
    return (distance, idx1, idx2)


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        closest_pair = fast_closest_pair(cluster_list)
        first_merge = cluster_list[closest_pair[1]]
        second_merge = cluster_list[closest_pair[2]]
        cluster_list.remove(first_merge)
        cluster_list.remove(second_merge)
        new_cluster = first_merge.merge_clusters(second_merge)
        cluster_list.append(new_cluster)
    return cluster_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    length = len(cluster_list)
    # Initialize k centers as clusters with the largest population
    largest_population = list(cluster_list)
    largest_population.sort(key = lambda cluster: cluster.total_population())
    k_centers = list()
    for idx_k in range(1, num_clusters+1):
        x_coordinates = largest_population[len(largest_population)-idx_k].horiz_center()
        y_coordinates = largest_population[len(largest_population)-idx_k].vert_center()
        k_centers.append((x_coordinates, y_coordinates))
    assert len(k_centers) == num_clusters
    # Clustering
    for indx_i in range(num_iterations):
        # Initialize k empty clusters
        clusters = list()
        for idx_k in range(num_clusters):
            clusters.append(Cluster(set(), k_centers[idx_k][0], k_centers[idx_k][1], 0, 0))
        # Distribute the closest points
        for idx_j in range(length):
            min_distance = float('inf')
            for idx_k in range(num_clusters):
                # Compute the distance
                vert_distance = cluster_list[idx_j].vert_center() - k_centers[idx_k][1]
                horiz_distance = cluster_list[idx_j].horiz_center() - k_centers[idx_k][0]
                distance = math.sqrt(vert_distance**2 + horiz_distance**2)
                if distance < min_distance:
                    merge_cluster = clusters[idx_k]
                    min_distance = distance
            merge_cluster.merge_clusters(cluster_list[idx_j])
        # Adjust the cluster centers
        if indx_i < num_iterations-1:
            for idx_f in range(num_clusters):
                x_coordinates = clusters[idx_f].horiz_center()
                y_coordinates = clusters[idx_f].vert_center()
                k_centers[idx_f] = (x_coordinates, y_coordinates)
    return clusters



