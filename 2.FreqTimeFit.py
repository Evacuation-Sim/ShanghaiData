import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import poisson, binom, chi2

path = r'.\结果输出\freq_time.csv'
df = pd.read_csv(path)

x = np.array([0, 1, 2, 3, 4, 5])
y1 = df['freq'] / np.sum(df['freq'])
y2 = df['time']
print(x)

def fit_function_1(k, lamb):
    return poisson.pmf(k, lamb)

def fit_function_2(x, a, b):
    return a*np.exp(b*x)

parameters, cov_matrix = curve_fit(fit_function_1, x, y1)
print(parameters)
print(cov_matrix)

plt.subplot(121)
plt.bar(x, y1, width=0.5)
plt.plot(
    x,
    fit_function_1(x, *parameters),
    marker='D', linestyle='-',
    color='red',
    label='Fit result',
)

parameters, cov_matrix = curve_fit(fit_function_2, x, y2)
print(parameters)
print(cov_matrix)
plt.subplot(122)
plt.bar(x, y2, width=0.5)
plt.plot(
    x,
    fit_function_2(x, *parameters),
    marker='D', linestyle='-',
    color='red',
    label='Fit result',
)
plt.show()


