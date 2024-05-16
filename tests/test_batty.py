from geoentropy import batty
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 1],
    [1, 1, 2, 2],
    [2, 2, 1, 1],
    [1, 1, 2, 2]
])

result = batty(data_matrix, category=1, cell_size=1, partitions=4, window=None, rescale=True, plot_output=False)

print("Batty Entropy:", result['batty_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative Batty Entropy:", result['relative_batty_entropy'])

matrix = np.array([
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 1, 1, 1, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])

# print(batty(matrix))
