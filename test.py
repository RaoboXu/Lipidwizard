import numpy as np
import scipy.stats as stats
import random

def quadratic_regression(x: list[float], y: list[float], confidence_level: float = 0.95) -> tuple:
    # Convert input lists to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Design matrix
    A = np.vstack([x**2, x, np.ones(len(x))]).T

    # Perform quadratic regression
    coefficients, residuals, _, _ = np.linalg.lstsq(A, y, rcond=None)

    # Calculate the standard error
    n = len(x)
    p = len(coefficients)
    dof = n - p
    residual_std_error = np.sqrt(residuals[0] / dof)

    # Calculate the confidence intervals
    t_value = stats.t.ppf(1 - (1 - confidence_level) / 2, dof)
    std_error_matrix = np.sqrt(np.diagonal(np.linalg.inv(A.T @ A))) * residual_std_error
    conf_intervals = []
    for coef, std_error in zip(coefficients, std_error_matrix):
        lower_bound = coef - t_value * std_error
        upper_bound = coef + t_value * std_error
        conf_intervals.append((lower_bound, upper_bound))

    return coefficients, conf_intervals

# x = [1.0, 2.0, 3.0, 4.0, 5.0]
# y = [1.1, 1.9, 3.2, 4.0, 5.1]

# coefficients, conf_intervals = quadratic_regression(x, y)

# print(f"Coefficients: {coefficients}")
# print(f"Confidence Intervals: {conf_intervals}")

import numpy as np
import matplotlib.pyplot as plt

def plot_quadratic_regression(x: list[float], y: list[float], coefficients: list[float], conf_intervals: list[float]) -> None:
    x = np.array(x)
    y = np.array(y)

    # Create a range of x values for plotting the fitted curve
    x_plot = np.linspace(min(x), max(x), 100)

    # Calculate the corresponding y values using the coefficients
    y_plot = coefficients[0] * x_plot**2 + coefficients[1] * x_plot + coefficients[2]

    # Calculate the corresponding y values using the confidence intervals
    y_delta =  conf_intervals[0][1] * x_plot**2 + conf_intervals[1][1] * x_plot + conf_intervals[2][1]

    y_upper = y_plot + y_delta
    y_lower = y_plot - y_delta



    # Plot the original data points
    plt.scatter(x, y, label="Data Points")

    # Plot the fitted curve
    plt.plot(x_plot, y_plot, 'r', label="Fitted Curve")

    plt.fill_between(x_plot, y_lower, y_upper, alpha=0.2, label="Confidence Interval")

    # Configure the plot
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title("Quadratic Regression")

    # Show the plot
    plt.show()

x = [12.0, 13.0, 15.0, 15.6, 16.0, 16.75, 17.77, 18.10, 19.033, 20.98]
y = [0.0097*v*v - 0.0864*v + 5.9080 + random.random()*2-1 for v in x ]

coefficients, conf_intervals = quadratic_regression(x, y)
plot_quadratic_regression(x, y, coefficients, conf_intervals)
