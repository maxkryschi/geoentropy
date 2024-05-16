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
                coords = [int(float(row[index]) / cell_size) for index in coordinate_columns]
                coordinates.append(coords)
            except (ValueError, IndexError):
                continue
    return coordinates


def _determine_matrix_size(all_coordinates):
    if all_coordinates:
        max_x = max(coords[0] for coords in all_coordinates) + 1
        max_y = max(coords[1] for coords in all_coordinates) + 1
        return max_y, max_x
    return 0, 0


def _fill_matrix(all_coordinates, max_y, max_x, category_values, priority):
    data_matrix = np.zeros((max_y, max_x))
    prioritized_coordinates = all_coordinates[priority]
    prioritized_value = category_values[priority]

    # Fill the matrix with the highest-priority file first
    for x, y in prioritized_coordinates:
        data_matrix[y, x] = prioritized_value

    # Fill the matrix with the remaining files without overwriting priority values
    for category_index, coordinates in enumerate(all_coordinates):
        if category_index == priority:
            continue
        category_value = category_values[category_index]
        for x, y in coordinates:
            if data_matrix[y, x] == 0:  # Only fill if the cell is empty
                data_matrix[y, x] = category_value

    return data_matrix


def _plot_data_matrix(data_matrix):
    plt.imshow(data_matrix, origin='lower', cmap='plasma')
    plt.colorbar()
    plt.title('Data Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def csv_to_matrix(file_paths, coordinate_columns=[0, 1], cell_size=1, plot=False, priority=0):
    _validate_coordinate_columns(coordinate_columns)

    if not (0 <= priority < len(file_paths)):
        raise ValueError("Priority index out of range")

    all_coordinates = []
    category_values = np.linspace(1, len(file_paths), len(file_paths))  # Assign unique values for each category

    for file_path in file_paths:
        coordinates = _load_coordinates(file_path, coordinate_columns, cell_size)
        all_coordinates.append(coordinates)

    flattened_coordinates = [coord for sublist in all_coordinates for coord in sublist]
    max_y, max_x = _determine_matrix_size(flattened_coordinates)
    data_matrix = _fill_matrix(all_coordinates, max_y, max_x, category_values,
                               priority) if max_y > 0 and max_x > 0 else np.array([])

    if plot:
        _plot_data_matrix(data_matrix)

    return data_matrix
