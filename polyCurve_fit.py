import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import itertools
import json
import time
from multiprocessing import Pool, cpu_count


# This is the form for polynomial functions
def polynom(X, E, P):
    result = 0
    for i in range(len(P)):
        term = P[i]
        for j in range(X.shape[1]):
            term *= X[:, j].astype(float) ** E[i, j]
        result += term
    return result




# This is the chunk generator.
def chunking_generator(lower, upper, rows, cols, num_workers, current_worker):
    all_combinations = itertools.product(range(lower, upper + 1), repeat=rows * cols)
    worker_combinations = itertools.islice(
        all_combinations, current_worker, None, num_workers
    )
    for comb in worker_combinations:
        matrix = np.array(comb).reshape(rows, cols)
        if len(np.unique(matrix, axis=0)) == rows:
            yield matrix


def findFit(
    E, worker_id, input_data, output_data, P_initial, best_fit, lower, upper, filename
):
    try:
        P_opt, P_cov = curve_fit(
            lambda X, *P: polynom(X, E, P),
            input_data,
            output_data,
            p0=P_initial,
        )
        residuals = output_data - polynom(input_data, E, P_opt)
        SSR = np.sum(residuals**2)
        if SSR < best_fit["SSR"]:
            best_fit["SSR"] = SSR
            best_fit["P_opt"] = P_opt
            best_fit["P_cov"] = P_cov
            best_fit["E"] = E
            print(f"current best fit for worker:{worker_id} is {SSR}")
            with open(
                f"w_{worker_id}_{filename}_{len(P_initial)}_{lower}_{upper}_best.log",
                "w",
            ) as f:
                data = {
                    "worker_id": worker_id,
                    "SSR": best_fit["SSR"],
                    "P_opt": best_fit["P_opt"].tolist(),
                    "P_cov": best_fit["P_cov"].tolist(),
                    "E": best_fit["E"].tolist(),
                }
                json.dump(data, f)

    except RuntimeError as e:
        print(f"Optimization failed for this E: {e}")


def worker_func(
    worker_id,
    lower,
    upper,
    rows,
    cols,
    num_workers,
    input_data,
    output_data,
    P_initial,
    filename,
):
    best_fit = {"SSR": float("inf"), "P_opt": None, "P_cov": None, "E": None}
    generator = chunking_generator(lower, upper, rows, cols, num_workers, worker_id)
    for Es in generator:
        findFit(
            Es,
            worker_id,
            input_data,
            output_data,
            P_initial,
            best_fit,
            lower,
            upper,
            filename,
        )


# This is the main function.
def polyCurve_fit(**kwargs):
    start_time = time.time()

    filename = kwargs.get("filename", "data.csv")
    P_initial_size = kwargs.get("Parameters", 2)
    P_initial = np.zeros(P_initial_size)
    lower = kwargs.get("lower", -3)
    upper = kwargs.get("upper", 3)

    data = pd.read_csv(filename, header=None)
    input_data = data.iloc[:, :-1]
    output_data = data.iloc[:, -1]
    input_data = input_data.to_numpy()
    output_data = output_data.to_numpy()
    rows = len(P_initial)
    cols = input_data.shape[1]

    num_workers = cpu_count()

    with Pool(num_workers) as p:
        p.starmap(
            worker_func,
            [
                (
                    i,
                    lower,
                    upper,
                    rows,
                    cols,
                    num_workers,
                    input_data,
                    output_data,
                    P_initial,
                    filename,
                )
                for i in range(num_workers)
            ],
        )

    end_time = time.time()
    total_time = end_time - start_time

    def read_best_fit(worker_id, P_initial, lower, upper, filename):
        with open(
            f"w_{worker_id}_{filename}_{len(P_initial)}_{lower}_{upper}_best.log", "r"
        ) as f:
            return json.load(f)

    best_fit_overall = {"SSR": float("inf")}
    for i in range(num_workers):
        worker_best_fit = read_best_fit(i, P_initial, lower, upper, filename)
        if worker_best_fit["SSR"] < best_fit_overall["SSR"]:
            best_fit_overall = worker_best_fit
    print("##########################################")
    print(f"polyCurve_fit has finished in{total_time}s:")
    print("##########################################")
    print("best_fit_overall")
    print(best_fit_overall)
    print("##########################################")

    with open(f"best_fit_{filename}_{len(P_initial)}_{lower}_{upper}.log", "w") as f:
        json.dump(best_fit_overall, f)
        f.write(f"Total time: {total_time} seconds")
