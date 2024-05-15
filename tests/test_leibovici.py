from geoentropy import leibovici
import numpy as np

matrix = np.array([
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 1, 1, 1, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])

print(leibovici(matrix, critical_distance=3))