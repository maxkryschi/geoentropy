import numpy as np
import pandas as pd
from math import log
import matplotlib.pyplot as plt


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray):
        raise ValueError("This function works for grid data. Please provide the dataset as a numpy array.")
    if data_matrix.ndim != 2:
        raise ValueError("The data matrix must be two-dimensional.")


def _plot_data_matrix(data_matrix):
    plt.imshow(data_matrix, origin='lower', cmap='plasma')
    plt.colorbar()
    plt.title('Data Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def _collect_adjacent_pairs(data_matrix):
    num_rows, num_cols = data_matrix.shape
    data_pairs = []

    # Collect horizontal adjacent pairs
    for i in range(num_rows - 1):
        for j in range(num_cols):
            if not np.isnan(data_matrix[i, j]) and not np.isnan(data_matrix[i + 1, j]):
                data_pairs.append(f"{data_matrix[i, j]}-{data_matrix[i + 1, j]}")

    # Collect vertical adjacent pairs
    for i in range(num_rows):
        for j in range(num_cols - 1):
            if not np.isnan(data_matrix[i, j]) and not np.isnan(data_matrix[i, j + 1]):
                data_pairs.append(f"{data_matrix[i, j]}-{data_matrix[i, j + 1]}")

    if not data_pairs:
        raise ValueError("Insufficient data to compute source.")

    return data_pairs


def _calculate_entropy(data_pairs):
    pair_counts = pd.Series(data_pairs).value_counts()
    probabilities = pair_counts / pair_counts.sum()
    entropy_value = -sum(prob * log(prob) for prob in probabilities if prob > 0)
    return entropy_value, pair_counts, probabilities


def _calculate_entropy_range(unique_elements):
    return [0, log(len(unique_elements) ** 2)]


def oneill(data_matrix, plot_output=False):
    _validate_data_matrix(data_matrix)
    if plot_output:
        _plot_data_matrix(data_matrix)

    unique_elements = np.unique(data_matrix[~np.isnan(data_matrix)])
    if len(unique_elements) == 1:
        raise ValueError("Data matrix must have at least two categories to compute source.")

    data_pairs = _collect_adjacent_pairs(data_matrix)
    entropy_value, pair_counts, probabilities = _calculate_entropy(data_pairs)
    entropy_range = _calculate_entropy_range(unique_elements)

    # Return the entropy measures and details
    probability_distribution = pd.DataFrame({
        'pair': pair_counts.index,
        'absolute_frequency': pair_counts.values,
        'relative_frequency': probabilities.values
    })

    return {
        'oneill_entropy': entropy_value,
        'entropy_range': {'minimum': entropy_range[0], 'maximum': entropy_range[1]},
        'relative_oneill_entropy': entropy_value / entropy_range[1],
        'probability_distribution': probability_distribution
    }
