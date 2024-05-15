from geoentropy import shannon
import numpy as np

matrix = np.array([
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 1, 1, 1, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])

print(shannon(matrix))
