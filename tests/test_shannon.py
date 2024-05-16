from geoentropy import shannon
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 3],
    [2, 1, 3, 3],
    [1, 1, 2, 2],
    [3, 3, 1, 1]
])

result = shannon(data_matrix)

print("Shannon Entropy:", result['shannon_entropy'])
print("Entropy Range:", result['shannon_entropy_range'])
print("Relative Shannon Entropy:", result['relative_shannon_entropy'])
print("Probability Distribution:\n", result['probability_distribution'])
print("Variance:", result['variance'])