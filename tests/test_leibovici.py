from geoentropy import leibovici
import numpy as np

data_matrix = np.array([
    [1, 2, 1, np.nan],
    [2, 1, np.nan, 2],
    [1, 1, 2, 1],
    [np.nan, 2, 1, 2]
])

result = leibovici(data_matrix, cell_size=1, critical_distance=2, plot_output=True)

print("Leibovici Entropy:", result['leibovici_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative Leibovici Entropy:", result['relative_leibovici_entropy'])
print("Probability Distribution:\n", result['probability_distribution'])
