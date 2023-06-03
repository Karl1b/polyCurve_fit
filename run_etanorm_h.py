#This is the production run. It will take a long time.

from polyCurve_fit import polyCurve_fit


polyCurve_fit(filename="etanorm_h.csv", Parameters=2, lower=-3, upper=5)
polyCurve_fit(filename="etanorm_h.csv", Parameters=3, lower=-3, upper=5)
polyCurve_fit(filename="etanorm_h.csv", Parameters=3, lower=-5, upper=5)
polyCurve_fit(filename="etanorm_h.csv", Parameters=4, lower=-3, upper=5)
polyCurve_fit(filename="etanorm_h.csv", Parameters=4, lower=-5, upper=5)