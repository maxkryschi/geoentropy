from geoentropy import shannon_z
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 3],
    [2, 1, 3, 3],
    [1, 1, 2, 2],
    [3, 3, 1, 1]
])

result = shannon_z(data_matrix)

print("Shannon Entropy Z:", result['shannon_entropy_z'])
print("Entropy Z Range:", result['shannon_entropy_z_range'])
print("Relative Shannon Entropy Z:", result['relative_entropy_z'])
print("Variance:", result['variance'])
print("Pair Probabilities:\n", result['pair_probabilities'])