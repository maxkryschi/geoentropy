import numpy as np
from math import comb, log
from collections import Counter


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray):
        raise ValueError("Input data must be a numpy array.")
    if data_matrix.size == 0:
        raise ValueError("The data matrix has no elements.")
    return data_matrix


def _calculate_category_probabilities(category_counts):
    total_elements = sum(category_counts.values())
    if total_elements == 0:
        raise ValueError("The data matrix has no elements.")
    return np.array([count / total_elements for count in category_counts.values()])


def _calculate_shannon_entropy(probabilities):
    if probabilities.size == 0:
        return 0
    return -np.sum(probabilities * np.log(probabilities))


def _calculate_entropy_variance(probabilities, entropy_value):
    if probabilities.size == 0:
        return 0
    squared_log_probabilities = [log(1 / prob) ** 2 for prob in probabilities]
    return sum(prob * sq_log for prob, sq_log in zip(probabilities, squared_log_probabilities)) - entropy_value ** 2


def shannon(data_matrix):
    data_matrix = _validate_data_matrix(data_matrix)
    flattened_data = data_matrix.flatten()
    category_counts = Counter(flattened_data)
    probabilities = _calculate_category_probabilities(category_counts)
    entropy_value = _calculate_shannon_entropy(probabilities)
    variance = _calculate_entropy_variance(probabilities, entropy_value)

    probability_distribution = [
        {'category': category, 'absolute_frequency': int(count),
         'relative_frequency': count / sum(category_counts.values())}
        for category, count in category_counts.items()
    ]
    entropy_range = [0, log(len(probability_distribution))]

    return {
        'shannon_entropy': entropy_value,
        'shannon_entropy_range': {'minimum': entropy_range[0], 'maximum': entropy_range[1]},
        'relative_shannon_entropy': entropy_value / log(len(probability_distribution)) if len(
            probability_distribution) > 1 else 0,
        'probability_distribution': probability_distribution,
        'variance': variance
    }
