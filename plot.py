import math
import os
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

w_dir = pathlib.Path.cwd()

print("Looking for files...")

residual_files = []
for root, dirs, files in os.walk(w_dir):
    for file in files:
        if file.startswith("residuals") and file.endswith(".dat"):
            p = os.path.join(root, file)
            residual_files.append(p)
            print(p)

min = 1
max_iter = 0


def orderOfMagnitude(number):
    return math.floor(math.log(number, 10))


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


for file in residual_files:
    iterations = pd.read_csv(file, skiprows=1, delimiter='\s+')['#']
    data = pd.read_csv(file, skiprows=1, delimiter='\s+').iloc[:, 1:].shift(+1, axis=1).drop(["Time"], axis=1)
    min_i = math.pow(10, orderOfMagnitude(data.min().min()))
    if min_i < min and min_i > 0:
        min = min_i
    max_iter_i = data.index.max()
    if max_iter_i > max_iter and max_iter_i > 0:
        max_iter = roundup(max_iter_i)

print("Exporting files...")

for file in tqdm(residual_files):
    iterations = pd.read_csv(file, skiprows=1, delimiter='\s+')['#']
    data = pd.read_csv(file, skiprows=1, delimiter='\s+').iloc[:, 1:].shift(+1, axis=1).drop(["Time"], axis=1)
    data = data.set_index(iterations)
    plot = data.plot(logy=True, figsize=(15, 5))
    fig = plot.get_figure()
    ax = plt.gca()
    ax.legend(loc='upper right')
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Residuals")
    ax.set_ylim(min, 1)
    ax.set_xlim(0, max_iter)
    wind_dir = str(file).split('\\')[-5]
    iteration = str(file).split('\\')[-2]
    plt.savefig(wind_dir + "_" + iteration + "_residuals.png", dpi=600)
    plt.close()

print("Done.")
