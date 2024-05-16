from geoentropy import karlstrom
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 1],
    [1, 1, 2, 2],
    [2, 2, 1, 1],
    [1, 1, 2, 2]
])

result = karlstrom(data_matrix, category=1, cell_size=1, partition=4, observation_window=None, neighbors=4,
                   method="number", plot_output=True)

print("Karlström Entropy:", result['karlstrom_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative Karlström Entropy:", result['relative_karlstrom_entropy'])