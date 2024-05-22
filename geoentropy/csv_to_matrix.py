import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import random


def _validate_coordinate_columns(coordinate_columns):
    if not isinstance(coordinate_columns, list) or not all(isinstance(idx, int) for idx in coordinate_columns):
        raise ValueError("Coordinate_columns should be a list of integers representing column indices.")


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


def _get_von_neumann_neighborhood(x, y, max_y, max_x):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < max_x - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < max_y - 1:
        neighbors.append((x, y + 1))
    return neighbors


def _find_empty_cell(data_matrix, x, y, max_y, max_x):
    visited = set()
    to_visit = [(x, y)]

    while to_visit:
        cx, cy = to_visit.pop(0)
        neighbors = _get_von_neumann_neighborhood(cx, cy, max_y, max_x)
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if (nx, ny) not in visited:
                if data_matrix[ny, nx] == 0:
                    return nx, ny
                visited.add((nx, ny))
                to_visit.append((nx, ny))
    return None, None


def _fill_matrix(all_coordinates, max_y, max_x, category_values, paths):
    data_matrix = np.zeros((max_y, max_x))
    prioritized_coordinates = all_coordinates[0]
    prioritized_value = category_values[0]

    for x, y in prioritized_coordinates:
        data_matrix[y, x] = prioritized_value

    for category_index, coordinates in enumerate(all_coordinates):
        if category_index == 0:
            continue
        category_value = category_values[category_index]
        for x, y in coordinates:
            if data_matrix[y, x] == 0:
                data_matrix[y, x] = category_value
            else:
                neighbors = _get_von_neumann_neighborhood(x, y, max_y, max_x)
                random.shuffle(neighbors)
                for nx, ny in neighbors:
                    if data_matrix[ny, nx] == 0:
                        data_matrix[ny, nx] = category_value
                        break
                else:
                    nx, ny = _find_empty_cell(data_matrix, x, y, max_y, max_x)
                    if nx is not None and ny is not None:
                        data_matrix[ny, nx] = category_value
                        print(f"Moved point from {paths[category_index]} from ({x}, {y}) to ({nx}, {ny})")
    return data_matrix


def _plot_data_matrix(data_matrix, file_paths):
    file_names = [path.split('/')[-1].replace('.csv', '') for path in file_paths]

    colors = ['white'] + [plt.cm.viridis(i) for i in np.linspace(0, 1, len(file_names))]
    cmap = ListedColormap(colors)

    norm = BoundaryNorm(np.arange(len(colors) + 1) - 0.5, len(colors) + 1)

    fig, ax = plt.subplots()
    cax = ax.imshow(data_matrix, origin='lower', cmap=cmap, norm=norm)

    cbar = fig.colorbar(cax, ticks=np.arange(len(colors)))
    cbar.ax.set_yticklabels(['Background'] + file_names, rotation=45, va='center')

    plt.title('Data Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()


def _check_overlaps(data_matrix, flattened_coordinates, max_y, max_x):
    return any(
        data_matrix[y, x] != 0 and sum(row == [x, y] for row in flattened_coordinates) > 1
        for y in range(max_y)
        for x in range(max_x)
    )


def _resolve_overlaps(all_coordinates, data_matrix, category_values, paths, max_y, max_x):
    print(
        "The minimum cell size is reached. Resolving overlaps by randomly moving lower priority points to cells in their direct von Neumann neighborhood.")
    for category_index, coordinates in enumerate(all_coordinates):
        if category_index == 0:
            continue
        for x, y in coordinates:
            if data_matrix[y, x] != category_values[category_index]:
                neighbors = _get_von_neumann_neighborhood(x, y, max_y, max_x)
                random.shuffle(neighbors)
                moved = False
                for nx, ny in neighbors:
                    if data_matrix[ny, nx] == 0:
                        data_matrix[ny, nx] = category_values[category_index]
                        print(f"Moved point from {paths[category_index]} from ({x}, {y}) to ({nx}, {ny})")
                        moved = True
                        break
                if not moved:
                    nx, ny = _find_empty_cell(data_matrix, x, y, max_y, max_x)
                    if nx is not None and ny is not None:
                        data_matrix[ny, nx] = category_values[category_index]
                        print(f"Moved point from {paths[category_index]} from ({x}, {y}) to ({nx}, {ny})")


def csv_to_matrix(file_paths, coordinate_columns=[0, 1], max_cell_size=1, min_cell_size=0.01, plot_output=False):
    _validate_coordinate_columns(coordinate_columns)

    if isinstance(file_paths, list):
        file_paths = {path: i + 1 for i, path in enumerate(file_paths)}

    sorted_files = sorted(file_paths.items(), key=lambda item: item[1], reverse=True)
    paths = [item[0] for item in sorted_files]

    category_values = np.linspace(1, len(paths), len(paths))

    cell_size = max_cell_size
    while True:
        all_coordinates = [_load_coordinates(file_path, coordinate_columns, cell_size) for file_path in paths]

        flattened_coordinates = [coord for sublist in all_coordinates for coord in sublist]
        max_y, max_x = _determine_matrix_size(flattened_coordinates)

        data_matrix = _fill_matrix(all_coordinates, max_y, max_x, category_values,
                                   paths) if max_y > 0 and max_x > 0 else np.array([])

        if not _check_overlaps(data_matrix, flattened_coordinates, max_y, max_x):
            break

        if cell_size <= min_cell_size:
            _resolve_overlaps(all_coordinates, data_matrix, category_values, paths, max_y, max_x)
            break

        cell_size /= 10
        print(f"Cell size changed to {cell_size} to resolve overlapping points.")

    if plot_output:
        _plot_data_matrix(data_matrix, paths)

    return data_matrix
