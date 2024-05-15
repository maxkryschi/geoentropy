import numpy as np
import csv
import matplotlib.pyplot as plt


def _validate_coordinate_columns(coordinate_columns):
    if not isinstance(coordinate_columns, list) or not all(isinstance(idx, int) for idx in coordinate_columns):
        raise ValueError("coordinate_columns should be a list of integers representing column indices.")


def _load_coordinates(file_path, coordinate_columns, cell_size):
    coordinates = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header
        for row in reader:
            try:
                # Convert floats to ints after dividing by cell_size
                coords = [int(float(row[index]) / cell_size) for index in coordinate_columns]
                coordinates.append(coords)
            except (ValueError, IndexError):
                continue
    return coordinates


def _determine_matrix_size(coordinates):
    if coordinates:
        max_x = max(coords[0] for coords in coordinates) + 1
        max_y = max(coords[1] for coords in coordinates) + 1
        return max_y, max_x
    return 0, 0


def _fill_matrix(coordinates, max_y, max_x):
    data_matrix = np.zeros((max_y, max_x))
    for x, y in coordinates:
        data_matrix[y, x] += 1
    return data_matrix


def _plot_data_matrix(data_matrix):
    plt.imshow(data_matrix, origin='lower', cmap='plasma')
    plt.colorbar()
    plt.title('Data Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def csv_to_matrix(file_path, coordinate_columns=[0, 1], cell_size=1, plot=False):
    _validate_coordinate_columns(coordinate_columns)
    coordinates = _load_coordinates(file_path, coordinate_columns, cell_size)
    max_y, max_x = _determine_matrix_size(coordinates)
    data_matrix = _fill_matrix(coordinates, max_y, max_x) if max_y > 0 and max_x > 0 else np.array([])

    if plot:
        _plot_data_matrix(data_matrix)

    return data_matrix
