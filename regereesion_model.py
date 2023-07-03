import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import t as t_dist

# Define the function for the model


def model(X, k, a, b, c):
    x, y = X
    u = x - k*y
    return a*u**2 + b*u + c


def predict_equation(c: list[float], d: list[float], t: list[float]):
    # Perform the curve fit
    t = np.array(t)
    c=np.array(c)
    d=np.array(d)
    params, params_covariance = curve_fit(model, (c, d), t)

    # Extract the optimal k, a, b, c
    k_optimal, a_optimal, b_optimal, c_optimal = params

    # Compute the residuals and the standard deviation of the residuals
    residuals = t - model((c, d), k_optimal, a_optimal, b_optimal, c_optimal)
    residual_std_error = np.sqrt(np.sum(residuals**2) / (len(t) - len(params)))

    # Compute the 95% prediction interval
    # 95% quantile of t-distribution
    t_value = t_dist.ppf(0.975, len(t) - len(params))
    prediction_interval = t_value * residual_std_error

    

    print(f"Optimal k: {k_optimal}")
    print(f"Prediction Equation for ECN: e=c-{k_optimal}d")
    print(
        f"Prediction Equation for ECN-RT: y={a_optimal}e^2+{b_optimal}e+{c_optimal}")
    print(f"Residual standard error: {residual_std_error}")
    print(f"Prediction interval: {prediction_interval}")


if __name__ == "__main__":

    abbr = [
        "FA 14:0",
        "FA 15:0",
        "FA 16:1",
        "FA 16:1",
        "FA 16:0",
        "FA 16:0",
        "FA 18:4",
        "FA 18:3",
        "FA 18:3",
        "FA 18:3",
        "FA 18:2",
        "FA 18:2",
        "FA 18:1",
        "FA 18:1",
        "FA 18:0",
        "FA 19:0",
        "FA 20:5",
        "FA 20:4",
        "FA 20:3",
        "FA 20:2",
        "FA 20:1",
        "FA 20:0",
        "FA 21:0",
        "FA 22:6",
        "FA 22:5",
        "FA 22:4",
        "FA 22:1",
        "FA 22:0",
        "FA 24:1"
    ]
    t = [
    6.52,
    6.72,
    6.59,
    6.66,
    7.01,
    7.30,
    6.28,
    6.44,
    6.47,
    6.50,
    6.68,
    6.80,
    7.09,
    7.19,
    7.57,
    7.84,
    6.40,
    6.62,
    6.79,
    7.20,
    7.60,
    8.24,
    8.49,
    6.54,
    6.66,
    7.00,
    8.24,
    8.75,
    8.74
    ]
    from ecn_filter import get_CND_from_abbr
    c = []
    d = []
    for item in abbr:
        cnd=get_CND_from_abbr(item)
        c.append(float(cnd[0]))
        d.append(float(cnd[1]))
    predict_equation(c, d, t)
    


