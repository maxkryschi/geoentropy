# GeoEntropy

GeoEntropy is a Python package designed to compute various entropy measures for spatial data. It provides several functions to partition spatial data and compute entropy measures such as Batty's entropy, Shannon's entropy, and others.

## Installation

You can install GeoEntropy using pip:

```bash
pip install geoentropy
```

## Usage

### Batty's Entropy
```python
from geoentropy import batty, karlstrom, leibovici, oneill, shannon, shannon_z
import numpy as np

# Example data matrix
matrix = np.array([
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 1, 1, 1, 2, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])

# Compute metrics for geometric/spatial entropy
print(batty(matrix))
print(karlstrom(matrix))
print(leibovici(matrix))
print(oneill(matrix))
print(shannon(matrix))
print(shannon_z())
```
