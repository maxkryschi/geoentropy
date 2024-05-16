from geoentropy import oneill
import numpy as np

data_matrix = np.array([
    [1, 2, 1, np.nan],
    [2, 1, np.nan, 2],
    [1, 1, 2, 1],
    [np.nan, 2, 1, 2]
])

result = oneill(data_matrix, plot_output=True)

print("O'Neill Entropy:", result['oneill_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative O'Neill Entropy:", result['relative_oneill_entropy'])
print("Probability Distribution:\n", result['probability_distribution'])