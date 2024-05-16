# GeoEntropy: A Python Package for Computing Spatial/Geometric Entropy

GeoEntropy is currently in a very early version. There is no guarantee for the accuracy or correctness of the results.

GeoEntropy is a Python package designed to compute various entropy measures for spatial data represented in matrices (
numpy arrays). GeoEntropy is inspired by
the [R package SpatEntropy](https://cran.r-project.org/web/packages/SpatEntropy/index.html)
by L. Altieri, D. Cocchi, and G. Roli and offers
tools for analyzing the entropy of spatial data.

With GeoEntropy, you can easily partition spatial data and compute entropy measures such as Batty's entropy, Shannon's
entropy, and more.

## Installation

You can install GeoEntropy using pip:

```bash
pip install geoentropy
```

## Usage

### Convert CSV-Files to a 2D numpy array

The ```csv_to_matrix``` function converts CSV files containing coordinate data into a 2D numpy array (data matrix).
Each CSV
file represents a different category, and the function maps these categories to unique values in the data matrix. It
includes options for prioritizing certain files and plotting the resulting matrix. If two points from different CSV
files have the same coordinates, the point from the prioritized file remains in place, while the point from the other
files is moved randomly to one of the neighboring cells in the von Neumann neighborhood.

```python
from geoentropy import csv_to_matrix
import numpy as np

file_paths = ['coordinates_category_1.csv', 'coordinates_category_2.csv']

data_matrix = csv_to_matrix(file_paths, coordinate_columns=[0, 1], cell_size=1, plot_output=False, priority=0)

print(data_matrix)
```

Output:

```
[[0. 0. 0. 0. 0. 0. 0. 0. 0. 2.]
 [0. 0. 0. 0. 2. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 2. 1. 0. 0. 1. 0.]
 [0. 0. 1. 0. 0. 0. 0. 2. 0. 0.]
 [1. 2. 0. 0. 0. 0. 0. 1. 0. 0.]
 [0. 0. 0. 1. 0. 0. 2. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 2. 1.]
 [0. 0. 2. 0. 0. 0. 1. 0. 0. 0.]
 [0. 0. 0. 1. 2. 0. 0. 0. 0. 0.]
 [2. 1. 0. 0. 0. 0. 0. 0. 0. 0.]]
```

### Spatial Partitioning

The ```spatial_partition``` function partitions a 2D data matrix into spatial regions using Voronoi tessellation, which
assigns each cell in the grid to the nearest partition center. This process helps analyze spatial data by grouping cells
based on their proximity to these centers.

```python
from geoentropy import spatial_partition
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 3],
    [2, 1, 3, 3],
    [1, 1, 2, 2],
    [3, 3, 1, 1]
])

result = spatial_partition(data_matrix, partitions=5, cell_size=1, window=None, plot_output=False)

print("Partition Coordinates:\n", result['partition_coordinates'])
print("Data with Partitions:\n", result['data_with_partitions'].head())
```

Output:

```
Partition Coordinates:
 [[3.2190276  2.7650245 ]
 [0.54426262 0.16163646]
 [2.66600046 2.83171161]
 [3.93007506 2.1637025 ]
 [0.84704577 3.96334437]]
Data with Partitions:
      x    y  category  partition
0  0.5  0.5         1          2
1  0.5  1.5         2          2
2  0.5  2.5         1          5
3  0.5  3.5         3          5
4  1.5  0.5         2          2
```

### Batty Entropy

The ```batty``` function calculates the Batty entropy, a measure of spatial segregation, for a given 2D data matrix.
It
processes the data through validation, dichotomization, spatial partitioning, and finally calculates the entropy and its
range.

```python
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
```

Output:

```
Batty Entropy: 2.7656685561977836
Entropy Range: {'minimum': np.float64(0.6931471805599453), 'maximum': np.float64(2.772588722239781)}
Relative Batty Entropy: 0.9975040776922705
```

### Karlström Entropy

The ```karlstrom``` function calculates the Karlström entropy, a measure of spatial segregation, for a given 2D data
matrix. The function processes the data through validation, dichotomization, spatial partitioning, and entropy
calculation while considering neighbor relationships.

```python
from geoentropy import karlstrom
import numpy as np

data_matrix = np.array([
    [1, 2, 1, 1],
    [1, 1, 2, 2],
    [2, 2, 1, 1],
    [1, 1, 2, 2]
])

result = karlstrom(data_matrix, category=1, cell_size=1, partition=4, observation_window=None, neighbors=4,
                   method="number", plot_output=False)

print("Karlström Entropy:", result['karlstrom_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative Karlström Entropy:", result['relative_karlstrom_entropy'])
```

Output:

```
Karlström Entropy: 1.324293923495886
Entropy Range: {'minimum': 0, 'maximum': np.float64(2.772588722239781)}
Relative Karlström Entropy: 0.47763806902672573
```

### Leibovici Entropy

The ```leibovici``` function calculates the Leibovici entropy, a measure of spatial organization, for a given
2D data matrix. This function validates inputs, counts adjacent pairs within a specified critical distance, computes
entropy, and optionally plots the data matrix.

```python
from geoentropy import leibovici
import numpy as np

data_matrix = np.array([
    [1, 2, 1, np.nan],
    [2, 1, np.nan, 2],
    [1, 1, 2, 1],
    [np.nan, 2, 1, 2]
])

result = leibovici(data_matrix, cell_size=1, critical_distance=2, plot_output=False)

print("Leibovici Entropy:", result['leibovici_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative Leibovici Entropy:", result['relative_leibovici_entropy'])
print("Probability Distribution:\n", result['probability_distribution'])
```

Output:

```
Leibovici Entropy: 1.3521103558155638
Entropy Range: {'minimum': 0, 'maximum': 1.3862943611198906}
Relative Leibovici Entropy: 0.9753414525348629
Probability Distribution:
       pair  absolute_frequency  relative_frequency
0  1.0-2.0                  13            0.333333
1  1.0-1.0                  10            0.256410
2  2.0-1.0                  10            0.256410
3  2.0-2.0                   6            0.153846
```

### O'Neill Entropy

The ```oneill``` function calculates the O'Neill entropy, a measure of spatial organization, for a
given 2D data matrix. The function processes the data by validating inputs, collecting adjacent pairs, computing
entropy, and optionally plotting the data matrix.

```python
from geoentropy import oneill
import numpy as np

data_matrix = np.array([
    [1, 2, 1, np.nan],
    [2, 1, np.nan, 2],
    [1, 1, 2, 1],
    [np.nan, 2, 1, 2]
])

result = oneill(data_matrix, plot_output=False)

print("O'Neill Entropy:", result['oneill_entropy'])
print("Entropy Range:", result['entropy_range'])
print("Relative O'Neill Entropy:", result['relative_oneill_entropy'])
print("Probability Distribution:\n", result['probability_distribution'])
```

Output:

```
O'Neill Entropy: 0.9743147528693494
Entropy Range: {'minimum': 0, 'maximum': 1.3862943611198906}
Relative O'Neill Entropy: 0.7028195311147832
Probability Distribution:
       pair  absolute_frequency  relative_frequency
0  2.0-1.0                   8               0.500
1  1.0-2.0                   6               0.375
2  1.0-1.0                   2               0.125
```

### Shannon Entropy

The ```shannon``` function calculates the Shannon entropy, which quantifies the uncertainty or diversity within a 2D
data matrix. It processes the data by validating inputs, calculating probabilities of different categories, computing
the entropy, and determining the variance.

```python
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
```

Output:

```
Shannon Entropy: 1.0717300941124526
Entropy Range: {'minimum': 0, 'maximum': 1.0986122886681098}
Relative Shannon Entropy: 0.9755307720176264
Probability Distribution:
 [{'category': np.int64(1), 'absolute_frequency': 7, 'relative_frequency': 0.4375}, {'category': np.int64(2), 'absolute_frequency': 4, 'relative_frequency': 0.25}, {'category': np.int64(3), 'absolute_frequency': 5, 'relative_frequency': 0.3125}]
Variance: 0.05362144899780308
```

### Shannon Z Entropy

The ```shannon_z``` function calculates the Shannon entropy for pairs of categories in a 2D data matrix. This type of
entropy quantifies the uncertainty or diversity of category pairs within the data. It is
important to note that Shannon entropy Z is not a spatial entropy, meaning it does not consider the spatial arrangement
of elements, only the frequency distribution of category pairs.

```python
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
```

Output:

```
Shannon Entropy Z: 1.6594506357352485
Entropy Z Range: {'minimum': 0, 'maximum': 1.791759469228055}
Relative Shannon Entropy Z: 0.9261570340410652
Variance: 0.21318393262341617
Pair Probabilities:
 [{'pair': '1-1', 'absolute_frequency': 21, 'relative_frequency': np.float64(0.175)}, {'pair': '1-2', 'absolute_frequency': 28, 'relative_frequency': np.float64(0.23333333333333334)}, {'pair': '1-3', 'absolute_frequency': 35, 'relative_frequency': np.float64(0.2916666666666667)}, {'pair': '2-2', 'absolute_frequency': 6, 'relative_frequency': np.float64(0.05)}, {'pair': '2-3', 'absolute_frequency': 20, 'relative_frequency': np.float64(0.16666666666666666)}, {'pair': '3-3', 'absolute_frequency': 10, 'relative_frequency': np.float64(0.08333333333333333)}]
```