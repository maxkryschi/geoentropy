# GeoEntropy: A Python Package for Computing Spatial/Geometric Entropy

GeoEntropy is currently in a very early version. There is no guarantee for the accuracy or correctness of the results.
The [source code is available on GitHub](https://github.com/maxkryschi/geoentropy), meaningful contributions are very
welcome :-).

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

The `csv_to_matrix` function converts multiple CSV files, each representing a different category, into a matrix for
visualization. It processes the coordinates, normalizes them based on the specified cell size, and fills a matrix with
values representing each category. If two points from different CSV files have the same coordinates, the cell size is
first set to one tenth. When `min_cell_size` is reached, the point from the prioritized CSV file remains in place,
while points from other CSV files with lower priority are randomly moved to one of the neighboring cells in the von
Neumann neighborhood.

Parameters:

* `file_paths`: List or dictionary of file paths. If a list, default priorities are assigned. If a dictionary, it
  maps file paths to their respective priorities.
* `coordinate_columns`: List of two integers specifying the columns in the CSV files that contain the x and y
  coordinates. Default is [0, 1].
* `max_cell_size`: Initial size of the cells in the matrix. Default is 1.
* `min_cell_size`: Minimum allowable size of the cells. Default is 0.01.
* `plot_output`: Boolean indicating whether to plot the resulting matrix. Default is False.

```python
from geoentropy import csv_to_matrix
import numpy as np

file_paths = ['coordinates_category_1.csv', 'coordinates_category_2.csv']
file_paths_with_priorities = {'coordinates_category_1.csv': 2, 'coordinates_category_2.csv': 1}

data_matrix = csv_to_matrix(file_paths_with_priorities, coordinate_columns=[0, 1], max_cell_size=1, min_cell_size=0.01,
                            plot_output=True)

print(data_matrix)
```

Output:

```
Cell size changed to 0.1 to resolve overlapping points.
[[0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 ...
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 0.]
 [0. 0. 0. ... 0. 0. 1.]]
```

### Spatial Partitioning

The `spatial_partition` function divides a given 2D data matrix into spatial partitions using Voronoi tessellation. This
helps to analyze the spatial distribution of data by assigning each grid point to a partition based on proximity to
randomly generated or specified partition centers.

### Parameters:

* `data_matrix`: A 2D numpy array representing the grid data. The function validates that the input is a 2D matrix.
* `partitions`: The number of partitions to create. Can be an integer for random generation or a list of coordinates for
  specific partition centers. Default is `10`.
* `cell_size`: The size of the cells in the matrix grid. Default is `1`.
* `window`: Optional parameter to specify the observation window as a tuple (min_x, min_y, max_x, max_y). Default
  is `None`.
* `plot_output`: Boolean indicating whether to plot the partitioned data overlaid with Voronoi diagrams. Default
  is `True`.

The function returns a dictionary containing the partition coordinates and the data with assigned partitions, which can
be further used for spatial analysis or entropy calculations.

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

The `batty` function calculates Batty's entropy, a measure of spatial segregation, for a given 2D data matrix. This
entropy measure helps to understand the spatial distribution and organization of a particular category within the
matrix. The function supports
rescaling to handle small area sizes and can optionally visualize the partitioned data.

### Parameters:

* `data_matrix`: A 2D numpy array representing the grid data. The function validates that the input is a 2D matrix.
* `category`: The category to analyze within the data matrix. Default is `1`.
* `cell_size`: The size of the cells in the matrix for partitioning. Default is `1`.
* `partitions`: The number of partitions to divide the data into. Default is `10`.
* `window`: Optional parameter to specify a window size for partitioning. Default is `None`.
* `rescale`: Boolean indicating whether to rescale small area sizes to avoid computational issues. Default is `True`.
* `plot_output`: Boolean indicating whether to plot the resulting partitions and their distribution. Default is `True`.

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

The `karlstrom` function calculates Karlstrom's entropy, a measure of spatial segregation, for a given 2D data matrix.
This entropy measure helps to understand the spatial distribution and organization of a particular category within the
matrix. The function allows specifying the method for determining neighbors and can optionally visualize the partitioned
data.

### Parameters:

* `data_matrix`: A 2D numpy array representing the grid data. The function validates that the input is a 2D matrix.
* `category`: The category to analyze within the data matrix. Default is `1`.
* `cell_size`: The size of the cells in the matrix for partitioning. Default is `1`.
* `partition`: The number of partitions to divide the data into. Default is `10`.
* `observation_window`: Optional parameter to specify a window size for partitioning. Default is `None`.
* `neighbors`: The number of neighbors or distance for determining neighbors. Default is `4`.
* `method`: The method for determining neighbors, either by a specific number ("number") or by a distance ("distance").
  Default is `"number"`.
* `plot_output`: Boolean indicating whether to plot the resulting partitions and their distribution. Default is `True`.

The function processes the input data matrix, partitions it using Voronoi tessellation, calculates the frequencies and
areas of the partitions, and then computes Karlstrom's entropy based on the specified method for determining neighbors.
It returns a dictionary containing Karlstrom's entropy, the entropy range, the relative Karlstrom entropy, detailed area
data, and partition coordinates. This provides a comprehensive overview of the spatial segregation and distribution of
the specified category within the data matrix.

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

The `leibovici` function calculates Leibovici's entropy, a measure of spatial association, for a given 2D data matrix.
This entropy measure helps to understand the spatial relationships and organization of different categories within the
matrix based on a specified critical distance.

### Parameters:

* `data_matrix`: A 2D numpy array representing the grid data. The function validates that the input is a 2D matrix.
* `cell_size`: The size of the cells in the matrix. Can be a scalar or an array specifying the size for each dimension.
  Default is `1`.
* `critical_distance`: The critical distance within which to count adjacent pairs. Default is `1`.
* `plot_output`: Boolean indicating whether to plot the data matrix. Default is `True`.

The function processes the input data matrix, validates the cell size and critical distance, counts adjacent pairs
within the specified distance, and calculates Leibovici's entropy. It returns a dictionary containing Leibovici's
entropy, the entropy range, the relative Leibovici entropy, and the probability distribution of observed pairs. The
function also provides an option to visualize the data matrix, offering a comprehensive view of spatial associations
within the data.

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

The `oneill` function calculates O'Neill's entropy, a measure of spatial association, for a given 2D data matrix. This
entropy measure helps to understand the spatial relationships and organization of different categories within the matrix
by analyzing adjacent pairs of data points.

### Parameters:

* `data_matrix`: A 2D numpy array representing the grid data. The function validates that the input is a 2D matrix.
* `plot_output`: Boolean indicating whether to plot the data matrix. Default is `False`.

The function processes the input data matrix, collects adjacent pairs of data points, and calculates O'Neill's entropy
based on the frequency of these pairs. It returns a dictionary containing O'Neill's entropy, the entropy range, the
relative O'Neill entropy, and the probability distribution of observed pairs. The function also provides an option to
visualize the data matrix, offering a comprehensive view of spatial associations within the data.

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

The `shannon` function calculates Shannon's entropy, a measure of information entropy, for a given data matrix. Unlike
other entropy measures in this library, Shannon's entropy does not account for spatial relationships; it simply measures
the uncertainty or diversity of categories within the dataset.

### Parameters:

* `data_matrix`: A numpy array representing the data. The function validates that the input is a non-empty numpy array.

The function processes the input data matrix, calculates the probabilities of each category, and computes Shannon's
entropy based on these probabilities. It also calculates the variance of the entropy and provides a range for the
entropy values. The function returns a dictionary containing Shannon's entropy, the entropy range, the relative Shannon
entropy, the probability distribution of categories, and the variance of the entropy. This provides a comprehensive
overview of the informational diversity within the data, without considering spatial arrangement.

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

The `shannon_z` function calculates Shannon's entropy for pairs of categories, known as Shannon Z entropy. This measure
extends Shannon's entropy to consider the distribution of pairs of categories within the data. Similar to Shannon's
entropy, Shannon Z entropy does not account for spatial relationships.

### Parameters:

* `data_matrix`: A numpy array representing the data. The function validates that the input is a non-empty numpy array.

The function processes the input data matrix, calculates the probabilities of pairs of categories, and computes Shannon
Z entropy based on these probabilities. It also calculates the variance of the entropy and provides a range for the
entropy values. The function returns a dictionary containing Shannon Z entropy, the entropy range, the relative Shannon
Z entropy, the probability distribution of category pairs, and the variance of the entropy. This provides a
comprehensive overview of the informational diversity of category pairs within the data, without considering spatial
arrangement.

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