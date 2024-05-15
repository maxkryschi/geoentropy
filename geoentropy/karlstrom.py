import numpy as np
import pandas as pd
from scipy.spatial import KDTree
from .spatial_partition import spatial_partition


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray) or data_matrix.ndim != 2:
        raise ValueError("For grid data, please provide the dataset as a 2D matrix.")


def _dichotomize_data_matrix(data_matrix, category):
    data_vector = data_matrix.ravel()
    unique_values = np.unique(data_vector)
    if category not in unique_values:
        raise ValueError("Please select a category among the ones in the dataset.")
    return (data_vector == category).astype(int).reshape(data_matrix.shape)


def _calculate_area_data(data_with_partitions, total_positive):
    area_data = data_with_partitions.groupby('partition').agg(
        abs_freq=pd.NamedAgg(column='category', aggfunc='sum'),
        area_size=pd.NamedAgg(column='partition', aggfunc='count')
    )
    area_data['rel_freq'] = area_data['abs_freq'] / total_positive
    return area_data.reset_index()


def _determine_neighbors(centroids, tree, method, neighbors):
    if method == "number":
        if not isinstance(neighbors, int):
            raise ValueError("If method is 'number', 'neighbors' must be an integer.")
        distances, indices = tree.query(centroids, k=neighbors + 1)  # +1 because query includes the point itself
        indices = [index[1:] for index in indices]  # Remove the point itself from its list of neighbors
    elif method == "distance":
        if not isinstance(neighbors, (int, float)):
            raise ValueError("If method is 'distance', 'neighbors' must be a number (int or float).")
        indices = tree.query_ball_point(centroids, r=neighbors)
    else:
        raise ValueError("Method should be set to either 'number' or 'distance'.")
    return indices


def _compute_karlstrom_entropy(area_data, neighbor_indices):
    neighbor_means = []
    for idx in neighbor_indices:
        if len(idx) > 0:
            neighbor_means.append(area_data.loc[area_data['partition'].isin(idx), 'rel_freq'].mean())
        else:
            neighbor_means.append(0)
    neighbor_means = np.array(neighbor_means)
    neighbor_means = np.where(neighbor_means == 0, np.nan, neighbor_means)
    karl_terms = np.where(area_data['rel_freq'] > 0, area_data['rel_freq'] * np.log(1 / neighbor_means), 0)
    karl_terms = np.nan_to_num(karl_terms)  # Convert NaNs to zero
    karl_entropy = np.sum(karl_terms)
    return karl_entropy


def _calculate_karlstrom_entropy_range(area_data):
    total_area = area_data['area_size'].sum()
    min_area = area_data['area_size'].min()
    return [max(0, np.log(min_area)), np.log(total_area)], total_area


def _apply_karlstrom_entropy_limit(karl_entropy, centroids):
    max_karl_entropy = np.log(len(centroids)) - 1e-5
    return min(karl_entropy, max_karl_entropy)


def karlstrom(data_matrix, category=1, cell_size=1, partition=10, observation_window=None, neighbors=4, method="number",
              plot_output=True):
    _validate_data_matrix(data_matrix)
    dichotomized_data_matrix = _dichotomize_data_matrix(data_matrix, category)
    partition_result = spatial_partition(dichotomized_data_matrix, partitions=partition, cell_size=cell_size,
                                         window=observation_window, plot_output=plot_output)

    centroids = partition_result['partition_coordinates']
    tree = KDTree(centroids)
    neighbor_indices = _determine_neighbors(centroids, tree, method, neighbors)

    total_positive = np.sum(dichotomized_data_matrix)
    area_data = _calculate_area_data(partition_result['data_with_partitions'], total_positive)

    karl_entropy = _compute_karlstrom_entropy(area_data, neighbor_indices)
    karl_entropy = _apply_karlstrom_entropy_limit(karl_entropy, centroids)
    karl_entropy_range, total_area = _calculate_karlstrom_entropy_range(area_data)

    return {
        'karlstrom_entropy': karl_entropy,
        'entropy_range': {'minimum': karl_entropy_range[0], 'maximum': karl_entropy_range[1]},
        'relative_karlstrom_entropy': karl_entropy / np.log(total_area),
        'area_data': area_data,
        'area_centroids': partition_result['partition_coordinates']
    }
