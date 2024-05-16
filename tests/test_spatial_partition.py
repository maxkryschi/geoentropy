from geoentropy import spatial_partition
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 3],
    [2, 1, 3, 3],
    [1, 1, 2, 2],
    [3, 3, 1, 1]
])

result = spatial_partition(data_matrix, partitions=5, cell_size=1, window=None, plot_output=True)

print("Partition Coordinates:\n", result['partition_coordinates'])
print("Data with Partitions:\n", result['data_with_partitions'].head())
