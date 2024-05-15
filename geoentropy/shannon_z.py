import numpy as np
from math import comb, log
from collections import Counter
from itertools import combinations_with_replacement


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray):
        raise ValueError("Input data must be a numpy array.")
    if data_matrix.size == 0:
        raise ValueError("The matrix has no elements.")
    return data_matrix


def _calculate_category_probabilities(category_counts):
    total_elements = sum(category_counts.values())
    if total_elements == 0:
        raise ValueError("The matrix has no elements.")
    return np.array([count / total_elements for count in category_counts.values()])


def _calculate_entropy(probabilities):
    if probabilities.size == 0:
        return 0
    return -np.sum(probabilities * np.log(probabilities))


def _calculate_entropy_variance(probabilities, entropy_value):
    if probabilities.size == 0:
        return 0
    squared_log_probabilities = [log(1 / prob) ** 2 for prob in probabilities]
    return sum(prob * sq_log for prob, sq_log in zip(probabilities, squared_log_probabilities)) - entropy_value ** 2


def _calculate_pair_frequencies(category_counts, categories):
    pair_absolute_frequencies = []
    for category1, category2 in combinations_with_replacement(categories, 2):
        count1 = category_counts[category1]
        count2 = category_counts[category2]
        freq = comb(count1, 2) if category1 == category2 else count1 * count2
        pair_absolute_frequencies.append(freq)
    return np.array(pair_absolute_frequencies)


def shannon_z(data_matrix):
    data_matrix = _validate_data_matrix(data_matrix)
    flattened_data = data_matrix.flatten()
    category_counts = Counter(flattened_data)
    categories = list(category_counts.keys())

    pair_absolute_frequencies = _calculate_pair_frequencies(category_counts, categories)
    total_pairs = pair_absolute_frequencies.sum()
    if total_pairs == 0:
        raise ValueError("Sum of pair frequencies is zero, cannot divide by zero")

    pair_relative_frequencies = pair_absolute_frequencies / total_pairs
    entropy_z_value = _calculate_entropy(pair_relative_frequencies)
    variance = _calculate_entropy_variance(pair_relative_frequencies, entropy_z_value)

    entropy_z_range = [0, log(comb(len(categories) + 1, 2))]
    pair_probabilities = [{'pair': f"{category1}-{category2}", 'absolute_frequency': int(af), 'relative_frequency': rf}
                          for (category1, category2), af, rf in
                          zip(combinations_with_replacement(categories, 2), pair_absolute_frequencies,
                              pair_relative_frequencies)]

    return {
        'shannon_entropy_z': entropy_z_value,
        'shannon_entropy_z_range': {'minimum': entropy_z_range[0], 'maximum': entropy_z_range[1]},
        'relative_entropy_z': entropy_z_value / log(comb(len(categories) + 1, 2)) if len(categories) > 1 else 0,
        'variance': variance,
        'pair_probabilities': pair_probabilities
    }
