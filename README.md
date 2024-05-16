# GeoEntropy: A Python Package for Computing Spatial/Geometric Entropy

GeoEntropy is currently in a very early version. There is no guarantee for the accuracy or correctness of the results.

GeoEntropy is a Python package designed to compute various entropy measures for spatial data represented in matrices (
numpy arrays). Inspired by the [R package SpatEntropy](https://cran.r-project.org/web/packages/SpatEntropy/index.html)
by L. Altieri, D. Cocchi, and G. Roli, GeoEntropy offers
tools for analyzing the entropy of spatial data.

With GeoEntropy, you can easily partition spatial data and compute entropy measures such as Batty's entropy, Shannon's
entropy, and more.

## Installation

You can install GeoEntropy using pip:

```bash
pip install geoentropy
```

## Usage

### Convert CSV-Files to numpy arrays

```python
from geoentropy import csv_to_matrix

matrix = csv_to_matrix(['file1.csv', 'file2.csv'], coordinate_columns=[0, 1], cell_size=1, plot=True, priority=1)
```

### Entropy

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
