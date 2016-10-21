"""
My implementation of the Algorithmic thinking 
project #3.

created by RinSer
"""

from cluster import Cluster as Cluster
import csv

# File paths
DATA_24 = '../unifiedCancerData_24.csv'
DATA_111 = '../unifiedCancerData_111.csv'
DATA_290 = '../unifiedCancerData_290.csv'
DATA_896 = '../unifiedCancerData_896.csv'
DATA_3108 = '../unifiedCancerData_3108.csv'


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
    largest_population = list(cluster_list)
    largest_population.sort(key = lambda cluster: cluster.total_population())
    k_centers = list()
    for idx_k in range(1, num_clusters+1):
        k_centers.append(largest_population[len(largest_population)-idx_k])
    assert len(k_centers) == num_clusters
    for cluster in k_centers:
        print cluster.total_population()


# Initialize a list of clusters and populate it
clusters24 = list()
with open(DATA_24, 'r') as datafile:
    data_reader = csv.reader(datafile)
    for row in data_reader:
        clusters24.append(Cluster(set([row[0]]), float(row[1]), float(row[2]), int(row[3]), float(row[4])))


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

# test data of the form [size of output cluster, sets of county tuples]
hierdata_24 = [[23, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36061',), ('36005',), ('36047',), ('36059',), ('36081',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [22, set([('11001', '51013'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36061',), ('36005',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [21, set([('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [20, set([('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34039',), ('34013', '34017'), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [19, set([('34013', '34017', '34039'), ('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [18, set([('34013', '34017', '34039'), ('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('36005', '36047', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [17, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('34013', '34017', '34039', '36005', '36047', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [16, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [15, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',)])],
                   [14, set([('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013')])],
                   [13, set([('06037', '06059'), ('01073',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013')])],
                   [12, set([('06037', '06059'), ('01073',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013', '51840')])],
                   [11, set([('06029', '06037', '06059'), ('01073',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013', '51840')])],
                   [10, set([('06029', '06037', '06059'), ('01073',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '51013', '51760', '51840')])],
                   [9, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '51013', '51760', '51840')])],
                   [8, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840')])],
                   [7, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('41051', '41067'), ('55079',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
                   [6, set([('06029', '06037', '06059', '06071', '06075'), ('01073',), ('08031',), ('41051', '41067'), ('55079',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
                   [5, set([('06029', '06037', '06059', '06071', '06075'), ('08031',), ('41051', '41067'), ('01073', '55079'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
                   [4, set([('06029', '06037', '06059', '06071', '06075'), ('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('08031',), ('41051', '41067')])],
                   [3, set([('06029', '06037', '06059', '06071', '06075', '41051', '41067'), ('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('08031',)])],
                   [2, set([('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('06029', '06037', '06059', '06071', '06075', '08031', '41051', '41067')])],
                   ]

kmeans_clustering(clusters24, 3, 50)
'''
print set_of_county_tuples(clusters24)
print set_of_county_tuples(hierarchical_clustering(clusters24, 23))
print hierdata_24[0][1]

clusters111 = list()
with open(DATA_111, 'r') as datafile:
    data_reader = csv.reader(datafile)
    for row in data_reader:
        clusters111.append(Cluster(row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])))

clusters290 = list()
with open(DATA_290, 'r') as datafile:
    data_reader = csv.reader(datafile)
    for row in data_reader:
        clusters290.append(Cluster(row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])))

clusters896 = list()
with open(DATA_896, 'r') as datafile:
    data_reader = csv.reader(datafile)
    for row in data_reader:
        clusters896.append(Cluster(row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])))

clusters3108 = list()
with open(DATA_3108, 'r') as datafile:
    data_reader = csv.reader(datafile)
    for row in data_reader:
        clusters3108.append(Cluster(row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])))


print slow_closest_pair(clusters111)
print fast_closest_pair(clusters111)
print slow_closest_pair(clusters290)
print fast_closest_pair(clusters290)
print slow_closest_pair(clusters896)
print fast_closest_pair(clusters896)
print slow_closest_pair(clusters3108)
print fast_closest_pair(clusters3108)
'''

