# PolyCurve_fit

Created by Karl Breuer [https://www.karlbreuer.com/](https://www.karlbreuer.com/)

## Overview

PolyCurve_fit is a scipy curve_fit wrapper that doesn't just find parameters for a single function but explores the best parameters for every polynomial function within a specified range. Although lightweight, it's a CPU-intensive tool designed to run overnight or on a server. However, memory usage remains constant throughout its operation.

## How It Works

A polynomial function can be expressed as a skeleton form and a matrix 'E' representing all exponents. 

PolyCurve_fit generates all possible polynomial functions by creating unique combinations for 'E'. 

This is accomplished by generating chunks and distributing these chunks evenly across all CPU cores (workers) on your machine. Each worker processes independently, logging only the currently best fit. Finally, all results are compared, and the one with the best fit is returned.

## Usage

An example script, `testrun.py`, with inline comments is provided. This script uses imaginary data for a centrifugal pump, presented in `pumpdata.csv`. Each row represents a data point, with the final entry being the result. For instance, the first data point is `100,0.309,28.5`, which denotes Q=100 m³/h impeller diameter = 0.309 m and the resulting pressure is 28.5m.

Run `testrun.py` to verify if you've set up PolyCurve_fit correctly on your system. The process will take approximately 1-3 minutes. During the run, the CPU will work at full load, but memory usage will remain low and stable.

## Fitting Your Own Data

To fit your own data, follow the same CSV format as in `pumpdata.csv` where the last entry in every row is the result, and the preceding entries are the parameters.

After this, it's recommended to create a small Python function and run PolyCurve_fit overnight or over a weekend, potentially on a high-performance machine or server. 

```python
from polyCurve_fit import polyCurve_fit

polyCurve_fit(filename="yourdata.csv", P_initial_size=1, lower=-4, upper=4)
polyCurve_fit(filename="yourdata.csv", P_initial_size=2, lower=-4, upper=4)
polyCurve_fit(filename="yourdata.csv", P_initial_size=3, lower=-4, upper=4)
polyCurve_fit(filename="yourdata.csv", P_initial_size=3, lower=-5, upper=5)
```

The above script runs PolyCurve_fit with varying polynomial sizes and exponent range, adjusting as per your needs.
