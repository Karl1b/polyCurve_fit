# PolyCurve_fit

Created by Karl Breuer
[https://www.karlbreuer.com/](https://www.karlbreuer.com/)

## Overview

PolyCurve_fit is a scipy curve_fit wrapper that doesn't just find parameters for a single function but explores the best parameters for every polynomial function within a specified range. Although lightweight, it's a CPU-intensive tool designed to run overnight or on a server. However, memory usage remains constant throughout its operation.

## Potential Applications

PolyCurve_fit is a versatile tool with a wide range of applications, particularly useful for fitting various types of data. While it was initially conceived with a focus on engineering, physical, and chemical properties, its uses extend beyond these domains. 

### Engineering

In engineering, you might use PolyCurve_fit to model system behaviors, optimize design parameters, or analyze performance metrics. It was developed while I did fit working curves for centrifugal pumps.

### Physics

In physics, PolyCurve_fit could help to uncover underlying mathematical models in experimental data, such as modelling the trajectory of a particle in a field, or fitting a curve to experimental data to determine physical constants.

### Chemistry

In the field of chemistry, you could utilize PolyCurve_fit to model reaction rates, analyze spectroscopic data, or model thermodynamic properties as a function of temperature or pressure.

These examples only scratch the surface of the tool's potential. The power of PolyCurve_fit lies in its ability to explore a broad range of polynomial functions to provide the best fit for your data, whatever your field or data might be.


## How It Works

A polynomial function can be expressed as a skeleton form and a matrix 'E' representing all exponents. 

PolyCurve_fit generates all possible polynomial functions by creating unique combinations for 'E'. 

This is accomplished by generating chunks and distributing these chunks evenly across all CPU cores (workers) on your machine. Each worker processes independently, logging only the currently best fit. Finally, all results are compared, and the one with the best fit is returned.

## Setup
Initial Setup on Linux:

```bash
git clone git@github.com:Karl1b/polyCurve_fit.git
cd polyCurve_fit/
source venv/bin/activate
pip install -r requirements.txt 
```
After this you are ready to do the testrun:
```bash
python testrun.py
```

## Usage

An example script, `testrun.py`, with inline comments is provided. This script uses imaginary data for a centrifugal pump, presented in `pumpdata.csv`. Each row represents a data point, with the final entry being the result. For instance, the first data point is `100,0.309,28.5`, which denotes Q=100 m³/h impeller diameter = 0.309 m and the resulting pressure is 28.5m.

Run `testrun.py` to verify if you've set up PolyCurve_fit correctly on your system. The process will take approximately 1-3 minutes. During the run, the CPU will work at full load, but memory usage will remain low and stable.

## Interpreting the Results

Upon completion of the `testrun`, you will find log files for each worker and a separate log file containing the best fit. The log file with the best fit will look similar to the following:

```
{
  "worker_id": 3,
  "SSR": 0.2509802334221808,
  "P_opt": [8702282.774546381, 2831.9150438165398, -1.2495031489638852e-07],
  "P_cov": [
    [457980421688.7199, -10938071.113623565, 0.0010411735815124667],
    [-10938071.113623565, 502.83522199533803, -4.892526703287442e-08],
    [0.0010411735815124667, -4.892526703287442e-08, 7.0646501491573e-18]
  ],
  "E": [[-3, 1], [0, 4], [3, 0]]
}

Total time: 84.75276207923889 seconds
```

This output informs us that worker 3 found the optimal fit with the least sum of squares residual (SSR). The resulting function derived from this data is:

```python
def f(X):
    y = (8702282.77454638 * X1 ** -3 * X2 ** 1) +
        (2831.9150438165398 * X1 ** 0 * X2 ** 4) +
        (-1.2495031489638852e-07 * X1 ** 3 * X2 ** 0)
    return y
```

In this function, each term represents a part of the polynomial, with its corresponding coefficient (`P_opt`) and exponents (`E`).

The P_cov in the output represents the covariance matrix of the parameter estimates. It is derived from the curve_fit function of scipy.optimize.

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

Have fun and may it work well for your needs.
