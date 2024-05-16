from geoentropy import csv_to_matrix
import numpy as np

file_paths = ['coordinates_category_1.csv', 'coordinates_category_2.csv']

data_matrix = csv_to_matrix(file_paths, coordinate_columns=[0, 1], cell_size=1, plot_output=True, priority=0)

print(data_matrix)
