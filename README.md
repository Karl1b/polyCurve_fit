# PolyCurve_fit

Developed by Karl Breuer
Visit my website: [https://www.karlbreuer.com/](https://www.karlbreuer.com/)

## Introduction

PolyCurve_fit is an advanced curve-fitting tool designed to explore the best parameters for polynomial functions within a user-specified range. As a scipy curve_fit wrapper, it delivers high computational performance despite its lightweight design. The tool is CPU-intensive and intended for long-duration runs, making it perfect for overnight computations or server-based usage. Yet, it maintains a constant memory footprint throughout its execution.

## Applications

PolyCurve_fit's versatility allows for wide-ranging applications across various fields. While initially designed with engineering, physics, and chemistry in mind, its utility extends far beyond.

### Engineering

PolyCurve_fit allows you to model system behaviors, optimize design parameters, or analyze performance metrics. It was developed originally for fitting working curves for centrifugal pumps.

### Physics

Utilize PolyCurve_fit to unearth mathematical models in experimental data, such as modelling particle trajectories in a field, or to fit curves to experimental data for determining physical constants.

### Chemistry

In the realm of chemistry, use PolyCurve_fit to model reaction rates, analyze spectroscopic data, or model thermodynamic properties as a function of temperature or pressure.

These instances merely hint at the potential of this tool. PolyCurve_fit's power lies in its ability to survey a wide range of polynomial functions, thereby providing the optimal fit for your data, irrespective of the field or data type.

## Functionality

PolyCurve_fit operates by expressing a polynomial function as a skeleton form and a matrix 'E', representing all exponents. It generates all possible polynomial functions by creating unique combinations for 'E'. This is accomplished by distributing chunks of combinations across all available CPU cores (workers) in your system. Each worker processes independently, logging the best fit it finds. Upon completion, the tool compares all results and returns the optimal fit.

## Setup

To set up PolyCurve_fit on a Linux system, execute the following commands:

```bash
git clone git@github.com:Karl1b/polyCurve_fit.git
cd polyCurve_fit/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Upon successful setup, run a test using:

```bash
python testrun.py
```

## Usage

A sample script, `testrun.py`, is provided, complete with inline comments for better understanding. This script uses fictional data for a centrifugal pump, stored in `pumpdata.csv`. Each row represents a data point, with the final entry being the result. For instance, the first data point is `100,0.309,28.5`, indicating Q=100 m³/h, impeller diameter=0.309 m, and the resultant pressure=28.5m.

Executing `testrun.py` helps verify the proper setup of PolyCurve_fit on your system. The process will take approximately 1-3 minutes, during which your CPU will operate at full load, but memory usage will remain low and steady.

## Interpreting the Results

Upon `testrun` completion, you will find log files for each worker and a separate log file containing the best fit. Here's an example:

```
{
  "worker_id": 3,
  "SSR": 0.2509802334221808,
  "P_opt": [8702282.774546381, 2831.9150438165398, -1.2495031489638852e-07],
  "P_cov": [
    [457980421688.7199, -10938071.113623565, 0.001041173581

5124667],
    [-10938071.113623565, 502.83522199533803, -4.892526703287442e-08],
    [0.0010411735815124667, -4.892526703287442e-08, 7.0646501491573e-18]
  ],
  "E": [[-3, 1], [0, 4], [3, 0]]
}

Total time: 84.75276207923889 seconds
```

The output shows that worker 3 discovered the optimal fit with the smallest sum of squares residual (SSR). The optimal function based on this output would be:

```python
def f(X):
    y = (8702282.77454638 * X1 ** -3 * X2 ** 1) +
        (2831.9150438165398 * X1 ** 0 * X2 ** 4) +
        (-1.2495031489638852e-07 * X1 ** 3 * X2 ** 0)
    return y
```

Each term in this function corresponds to a part of the polynomial, associated with its coefficient (`P_opt`) and exponents (`E`). The `P_cov` represents the covariance matrix of the parameter estimates, derived from the `curve_fit` function of scipy.optimize.

## Implementing with Your Own Data

To use PolyCurve_fit with your own data, ensure it follows the same CSV format as `pumpdata.csv`. The last entry in every row should be the result, with the preceding entries being the parameters.

We recommend running PolyCurve_fit overnight or over a weekend, possibly on a high-performance machine or server. See the following example:

```python
from polyCurve_fit import polyCurve_fit
polyCurve_fit(filename="data.csv", Parameters=2, lower=-3, upper=4)
polyCurve_fit(filename="data.csv", Parameters=3, lower=-5, upper=5)
polyCurve_fit(filename="data.csv", Parameters=4, lower=-5, upper=5)
```

This script runs PolyCurve_fit with different polynomial sizes and exponent ranges, which can be adjusted to meet your requirements.

We hope you find this tool beneficial for your data analysis needs.

## Real-World Data

We have been granted permission by KSB to use real pump data for this project. You can find the curve data for 'h' from the etanorm 065-040-250 in `etanorm_h.csv`. The data includes rpm in 1/min, diameter in mm, flow in m3/h, and the resultant head in m. Please note that this data was manually transcribed from openly available charts on ksb.com and may contain errors.