from polyCurve_fit import polyCurve_fit

# This is your Testrun
# I think the filename is clear. ;-)
# Parameters is the number of fitting Paramaters you want.
# lower is the lower border Value for your exponents.
# upper is the upper border value for your exponents.
polyCurve_fit(filename="pumpdata.csv", Parameters=3, lower=-3, upper=4)

#This is my result:
#{"worker_id": 3, "SSR": 0.2509802334221808,
# "P_opt": [8702282.774546381, 2831.9150438165398, -1.2495031489638852e-07],
# "P_cov": [[457980421688.7199, -10938071.113623565, 0.0010411735815124667], [-10938071.113623565, 502.83522199533803, -4.892526703287442e-08], [0.0010411735815124667, -4.892526703287442e-08, 7.0646501491573e-18]],
# "E": [[-3, 1], [0, 4], [3, 0]]}
# Total time: 98.83465695381165 seconds


# Production:
# In production you can just chain your runs like this, and you should start with the faster ones:
# Then leave this running on your server or overnight. If you need to interupt the log files will be there.


#polyCurve_fit(filename="pumpdata.csv", P_initial_size=1, lower=-4, upper=4)
#polyCurve_fit(filename="pumpdata.csv", P_initial_size=2, lower=-4, upper=4)
#polyCurve_fit(filename="pumpdata.csv", P_initial_size=3, lower=-4, upper=4)
#polyCurve_fit(filename="pumpdata.csv", P_initial_size=3, lower=-5, upper=5)
