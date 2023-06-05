# PolyCurve_fit

Developed by Karl Breuer, this tool is available free and open source (Apache License Version 2.0, January 2004).

PolyCurve_fit solves `f(x,p) = y` for `p` in function `f(x,p)` by creating a polynomial standard function `f(X,E,P) = Y` and fitting every `E` with Scipy's curve_fit.

After this, similar datasets can be fitted with the found standard polynomial function (the resulting `E`) in the usual way.

## Introduction

PolyCurve_fit is an advanced curve-fitting tool designed to find the best parameters for polynomial functions within a user-specified range. Acting as a Scipy curve_fit wrapper, it delivers high computational performance despite its lightweight design. This tool is CPU-intensive and designed for long-duration runs, making it perfect for overnight computations or server-based usage. However, it maintains a constant memory footprint throughout its execution.

## Applications

PolyCurve_fit's versatility allows for wide-ranging applications across various fields. While initially designed with engineering, physics, and chemistry in mind, its utility extends far beyond these disciplines.

### Engineering

PolyCurve_fit allows you to model system behaviors, optimize design parameters, and analyze performance metrics. It was originally developed for fitting working curves for centrifugal pumps.

### Physics

Use PolyCurve_fit to unearth mathematical models in experimental data, such as modeling particle trajectories in a field, or to fit curves to experimental data for determining physical constants.

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

Upon successful setup, you can run a test using:

```bash
python testrun.py
```

## Usage

A sample script, `testrun.py`, is provided, complete with inline comments for better understanding. This script uses real-world data for a centrifugal pump, stored in `etanorm_h.csv`. Each row represents a data point, with the final entry being the result. For instance, the first data point is `1450,112,0,4`, indicating
w (rotating speed)=1450 1/s, d (impeller diameter) = 112 mm, Q (flow) = 0 m3/h, and finally h (head or pressure) = 4 m.

Executing `testrun.py` helps verify the proper setup of PolyCurve_fit on your system. The process will take a short time, during which your CPU will operate at full load, but memory usage will remain low and steady.

## Interpreting the results

Upon `testrun` completion, you will find log files for each worker and a separate log file containing the best overall fit. Here's an example:

```json
{"worker_id": 7, "SSR": 1.41711820944752, "P_opt": [1.5251590372839772e-10, -0.13003739958313548], "P_cov": [[3.1229332368877225e-25, -6.527254476558119e-16], [-6.527254476558119e-16, 3.057960866749138e-06]], "E": [[2, 2, 0], [0, -1, 2]]}Total time: 34.98347568511963 seconds
```

The output shows that worker number 7 discovered the optimal fit with the smallest sum of squares residual (SSR). The optimal function based on this output would be:

`f(x,E,P) = 1.5251590372839772e-10 * rpm^2 * d^2 * h^0 + -0.13003739958313548 * rpm^0 * d^-1 * h^2`

Each term in this function corresponds to a part of the polynomial, associated with its coefficient (`P_opt`) and exponents (`E`). The `P_cov` represents the covariance matrix of the parameter estimates, derived from the `curve_fit` function of scipy.optimize.

A pump similar to this specific etanorm might also be described with this equation. Then, the only task left is to find the matching parameters.

## Implementing with your own data

To use PolyCurve_fit with your own data, ensure it follows the same CSV format as `etanorm_h.csv`. The last entry in every row should be the result, with the preceding entries being the parameters.

We recommend running PolyCurve_fit overnight or over a weekend, possibly on a high-performance machine or server. See the following example:

```python
from polyCurve_fit import polyCurve_fit
polyCurve_fit(filename="data.csv", Parameters=2, lower=-3, upper=4)
polyCurve_fit(filename="data.csv", Parameters=3, lower=-5, upper=5)
polyCurve_fit(filename="data.csv", Parameters=4, lower=-5, upper=5)
```

This script runs PolyCurve_fit with different polynomial sizes and exponent ranges, which can be adjusted to meet your requirements. It is recommended to start with the faster runs.

We hope you find this tool beneficial for your data analysis needs.

## Real-World Data

We have been granted permission by KSB [https://www.ksb.com/](https://www.ksb.com/)
to use real pump data for this project. Thank you, KSB! You can find the curve data for 'h' from the `Etanorm 065-040-250` in `etanorm_h.csv`. The data includes rpm in 1/min, diameter in mm, flow in m3/h, and the resultant head in m. Please note that this data was manually transcribed from openly available charts on ksb.com and hence may contain errors.