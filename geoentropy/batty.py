import numpy as np
import pandas as pd
from .spatial_partition import spatial_partition


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray) or data_matrix.ndim != 2:
        raise ValueError("For grid data, please provide the dataset as a 2D matrix.")
    return data_matrix


def _dichotomize_data_matrix(data_matrix, category):
    data_vector = data_matrix.ravel()
    unique_values = np.unique(data_vector)
    if category not in unique_values:
        raise ValueError("Please select a category among the ones in the dataset.")
    return (data_vector == category).astype(int).reshape(data_matrix.shape)


def _calculate_area_data(data_with_partitions):
    area_data = data_with_partitions.groupby('partition').agg(
        abs_freq=pd.NamedAgg(column='category', aggfunc='sum'),
        area_size=pd.NamedAgg(column='partition', aggfunc='count')
    )
    area_data['rel_freq'] = area_data['abs_freq'] / area_data['abs_freq'].sum()
    return area_data


def _calculate_batty_entropy(area_data, sub_area_sizes, rescale):
    if min(sub_area_sizes) < 1:
        if not rescale:
            raise ValueError(
                "Results may be unreliable due to computational issues in taking logarithms of the sub-areas size, since there are areas with size < 1. We suggest to re-run the function with rescale = True")
        else:
            cc = 1 / min(sub_area_sizes) + 1e-02
            resc_Tg = sub_area_sizes * cc
            batty_terms_rescaled = np.where(area_data['rel_freq'] > 0,
                                            area_data['rel_freq'] * np.log(resc_Tg / area_data['rel_freq']), 0)
            batty_entropy = np.sum(batty_terms_rescaled) - np.log(cc)
            print(
                "Some sub-areas have size < 1, so they have been internally rescaled to avoid computational issues. The entropy in the output refers to the original area scale.")
    else:
        batty_entropy = np.sum(
            np.where(area_data['rel_freq'] > 0, area_data['rel_freq'] * np.log(sub_area_sizes / area_data['rel_freq']), 0))
    return batty_entropy


def _calculate_batty_entropy_range(sub_area_sizes):
    return [max(0, np.log(min(sub_area_sizes))), np.log(sum(sub_area_sizes))]


def batty(data_matrix, category=1, cell_size=1, partitions=10, window=None, rescale=True, plot_output=True):
    data_matrix = _validate_data_matrix(data_matrix)
    dichotomized_data_matrix = _dichotomize_data_matrix(data_matrix, category)

    partition_result = spatial_partition(dichotomized_data_matrix, partitions=partitions, cell_size=cell_size,
                                         window=window, plot_output=plot_output)
    partition_coordinates = partition_result['partition_coordinates']
    data_with_partitions = partition_result['data_with_partitions']

    area_data = _calculate_area_data(data_with_partitions)
    Tg = area_data['area_size'].values

    batty_entropy = _calculate_batty_entropy(area_data, Tg, rescale)
    batty_entropy_range = _calculate_batty_entropy_range(Tg)

    return {
        'batty_entropy': batty_entropy,
        'entropy_range': {'minimum': batty_entropy_range[0], 'maximum': batty_entropy_range[1]},
        'relative_batty_entropy': batty_entropy / np.log(sum(Tg)),
        'area_data': area_data.reset_index(),
        'partition_coordinates': partition_coordinates
    }
