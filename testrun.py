from polyCurve_fit import polyCurve_fit

# This is your Testrun
# I think the filename is clear. ;-)
# Parameters is the number of fitting Paramaters you want.
# lower is the lower border Value for your exponents.
# upper is the upper border value for your exponents.
polyCurve_fit(filename="etanorm_h.csv", Parameters=2, lower=-3, upper=5)

# Production:
# In production you can just chain your runs like this, and you should start with the faster ones:
# Then leave this running on your server or overnight. If you need to interupt the log files will be there.

#polyCurve_fit(filename="data.csv", Parameters=2, lower=-3, upper=4)
#polyCurve_fit(filename="data.csv", Parameters=3, lower=-5, upper=5)
#polyCurve_fit(filename="data.csv", Parameters=4, lower=-5, upper=5)
