from geoentropy import csv_to_matrix
import numpy as np

file_paths = ['coordinates_category_1.csv', 'coordinates_category_2.csv']
file_paths_with_priorities = {'coordinates_category_1.csv': 2, 'coordinates_category_2.csv': 1}

data_matrix = csv_to_matrix(file_paths_with_priorities, coordinate_columns=[0, 1], max_cell_size=1, min_cell_size=0.01,
                            plot_output=True)

print(data_matrix)
