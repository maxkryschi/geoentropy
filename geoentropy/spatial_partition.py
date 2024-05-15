import numpy as np
import pandas as pd
from scipy.spatial import KDTree, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


def _validate_data_matrix(data_matrix):
    if not isinstance(data_matrix, np.ndarray) or data_matrix.ndim != 2:
        raise ValueError("Please provide the dataset as a 2D matrix.")


def _initialize_parameters(data_matrix, cell_size, window):
    num_rows, num_cols = data_matrix.shape
    if isinstance(cell_size, (int, float)):
        x_cell_size = y_cell_size = cell_size
    else:
        x_cell_size, y_cell_size = cell_size

    if window is None:
        min_x, min_y = 0, 0
        max_x, max_y = num_cols * x_cell_size, num_rows * y_cell_size
    else:
        min_x, min_y, max_x, max_y = window

    return num_rows, num_cols, x_cell_size, y_cell_size, min_x, min_y, max_x, max_y


def _generate_grid_coordinates(num_rows, num_cols, x_cell_size, y_cell_size, min_x, min_y, max_x, max_y):
    x_coordinates = np.linspace(min_x + x_cell_size / 2, max_x - x_cell_size / 2, num_cols)
    y_coordinates = np.linspace(min_y + y_cell_size / 2, max_y - y_cell_size / 2, num_rows)
    grid_coordinates = np.array(np.meshgrid(x_coordinates, y_coordinates)).T.reshape(-1, 2)
    return grid_coordinates


def _generate_partition_coordinates(partitions, min_x, max_x, min_y, max_y):
    if isinstance(partitions, int):
        random_x = np.random.uniform(min_x, max_x, partitions)
        random_y = np.random.uniform(min_y, max_y, partitions)
        partition_coordinates = np.vstack((random_x, random_y)).T
    else:
        partition_coordinates = np.array(partitions)
        if np.any(partition_coordinates[:, 0] < min_x) or np.any(partition_coordinates[:, 0] > max_x) or \
                np.any(partition_coordinates[:, 1] < min_y) or np.any(partition_coordinates[:, 1] > max_y):
            raise ValueError(
                "The given coordinates for the area partition are outside the boundaries of the data observation window")
    return partition_coordinates


def _assign_partitions_to_grid(grid_coordinates, partition_coordinates):
    tree = KDTree(partition_coordinates)
    _, nearest_partition_indices = tree.query(grid_coordinates)
    return nearest_partition_indices


def _create_data_frame(grid_coordinates, data_matrix, nearest_partition_indices):
    data_flattened = data_matrix.ravel()
    data_with_partitions = pd.DataFrame({
        'x': grid_coordinates[:, 0],
        'y': grid_coordinates[:, 1],
        'category': data_flattened,
        'partition': nearest_partition_indices + 1
    })
    return data_with_partitions


def _plot_partitioned_data(data_matrix, min_x, max_x, min_y, max_y, partition_coordinates):
    plt.figure(figsize=(8, 8))
    plt.imshow(data_matrix, extent=(min_x, max_x, min_y, max_y), cmap='tab20c', origin='lower', aspect='equal')
    plt.colorbar(label='Data values')
    vor = Voronoi(partition_coordinates)
    voronoi_plot_2d(vor, show_vertices=False, line_colors='black', line_width=2, line_alpha=0.6, point_size=2,
                    ax=plt.gca())
    plt.title('Voronoi Partitioning Overlaid on Data Heatmap')
    plt.gca().invert_yaxis()
    plt.grid(False)
    plt.show()


def spatial_partition(data_matrix, partitions=10, cell_size=1, window=None, plot_output=True):
    _validate_data_matrix(data_matrix)
    num_rows, num_cols, x_cell_size, y_cell_size, min_x, min_y, max_x, max_y = _initialize_parameters(data_matrix,
                                                                                                      cell_size, window)
    grid_coordinates = _generate_grid_coordinates(num_rows, num_cols, x_cell_size, y_cell_size, min_x, min_y, max_x,
                                                  max_y)
    partition_coordinates = _generate_partition_coordinates(partitions, min_x, max_x, min_y, max_y)
    nearest_partition_indices = _assign_partitions_to_grid(grid_coordinates, partition_coordinates)
    data_with_partitions = _create_data_frame(grid_coordinates, data_matrix, nearest_partition_indices)

    if plot_output:
        _plot_partitioned_data(data_matrix, min_x, max_x, min_y, max_y, partition_coordinates)

    return {
        'partition_coordinates': partition_coordinates,
        'data_with_partitions': data_with_partitions
    }
