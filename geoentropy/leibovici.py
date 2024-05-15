import numpy as np
import pandas as pd
from math import sqrt, log
import matplotlib.pyplot as plt
from shapely.geometry import Polygon


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray):
        raise ValueError("For grid data, please provide the dataset as a numpy array.")
    if data_matrix.ndim != 2:
        raise ValueError("The data matrix must be two-dimensional.")


def _validate_cell_size(cell_size):
    if np.isscalar(cell_size):
        return np.array([cell_size, cell_size])
    return np.asarray(cell_size)


def _validate_critical_distance(critical_distance, cell_size, num_rows, num_cols):
    if critical_distance < min(cell_size):
        raise ValueError("The distance of interest is too small for building any couple.")
    max_distance = sqrt((num_rows * cell_size[0]) ** 2 + (num_cols * cell_size[1]) ** 2)
    if critical_distance >= max_distance:
        raise ValueError(
            "The chosen distance is equal or larger than the maximum distance over the observation area. Maybe you wish to compute the non-spatial Shannon's entropy of Z instead?")


def _count_adjacent_pairs_within_distance(data_matrix, cell_size, critical_distance):
    num_rows, num_cols = data_matrix.shape
    data_pairs = []
    for i in range(num_rows):
        for j in range(num_cols):
            if np.isnan(data_matrix[i, j]):
                continue
            for i2 in range(i, num_rows):
                for j2 in range(num_cols):
                    if i2 == i and j2 <= j:
                        continue
                    if np.isnan(data_matrix[i2, j2]):
                        continue
                    distance = sqrt((i2 - i) ** 2 * cell_size[0] ** 2 + (j2 - j) ** 2 * cell_size[1] ** 2)
                    if distance <= critical_distance:
                        data_pairs.append(f"{data_matrix[i, j]}-{data_matrix[i2, j2]}")
    return data_pairs


def _calculate_entropy(data_pairs):
    if not data_pairs:
        raise ValueError("Insufficient data to compute source.")
    pair_counts = pd.Series(data_pairs).value_counts()
    probabilities = pair_counts / pair_counts.sum()
    entropy_value = -sum(p * log(p) for p in probabilities if p > 0)
    return entropy_value, pair_counts, probabilities


def _determine_entropy_range(data_matrix):
    num_categories = len(np.unique(data_matrix[~np.isnan(data_matrix)]))
    return [0, log(num_categories ** 2)]


def _plot_data_matrix(data_matrix):
    plt.imshow(data_matrix, cmap='plasma', interpolation='nearest')
    plt.colorbar()
    plt.title("Data Visualization")
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def leibovici(data_matrix, cell_size=1, critical_distance=1, plot_output=True):
    _validate_data_matrix(data_matrix)
    num_rows, num_cols = data_matrix.shape
    cell_size = _validate_cell_size(cell_size)
    _validate_critical_distance(critical_distance, cell_size, num_rows, num_cols)

    data_pairs = _count_adjacent_pairs_within_distance(data_matrix, cell_size, critical_distance)
    entropy_value, pair_counts, probabilities = _calculate_entropy(data_pairs)
    entropy_range = _determine_entropy_range(data_matrix)

    results = {
        "leibovici_entropy": entropy_value,
        "entropy_range": {'minimum': entropy_range[0], 'maximum': entropy_range[1]},
        "relative_leibovici_entropy": entropy_value / entropy_range[1],
        "probability_distribution": pd.DataFrame({
            "pair": pair_counts.index,
            "absolute_frequency": pair_counts.values,
            "relative_frequency": probabilities.values
        })
    }

    if plot_output:
        _plot_data_matrix(data_matrix)

    return results
