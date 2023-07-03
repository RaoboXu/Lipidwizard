import numpy as np
import scipy.stats as stats
from scipy.stats import t
import xlHelper as xlh
import re
from config import config
import os.path
import util

from matching import MatchResult
from molecule import IsotopicVariants

class ECNProfile:
    def __init__(self,name:str,k:float, equation, coefficients:list[float],r_square:float,confidence_level:float,ecn_data:list[float],rt_data:list[float]) -> None:
        self.name = name
        self.k = k
        self.equation = equation
        self.coefficients = coefficients
        self.r_square = r_square
        self.confidence_level = confidence_level
        self.ecn_data = ecn_data
        self.rt_data = rt_data
    
    def predict(self,ecn:float):
        return self.equation([ecn])
    def predict(self,ecn:list[float]):
        return self.equation(ecn)
    def __str__(self) -> str:
        str = "y={:.6f}x^2{}{:.6f}x{}{:.6f}, k={:.2f}, R^2={:.6f}, confidence level={:.2f}".format(self.coefficients[0], "+" if self.coefficients[1] > 0 else "", self.coefficients[1], "+" if self.coefficients[2] > 0 else "", self.coefficients[2],self.k,self.r_square,self.confidence_level)
        return str


def predict(coefficients, x):
    return coefficients[0]*x**2+coefficients[1]*x+coefficients[2]


def get_CND_from_abbr(abbr: str):
    CND = re.findall(r'[\d.]+:[\d.]+', abbr)
    if (len(CND) > 0):
        CND = CND[0]
        CND = [int(i) for i in CND.split(':')]
        return CND
    return 'ERROR'


def ECN_data_exist(category: str):
    return os.path.exists(config.ECN_DATA_DIRECTORY+category)


def cal_ecn(c, d, k=2.00):
    return c-k*d

def quadratic_regression(x_values,y_values):
    coeffs,residuals = np.polyfit(np.array(x_values), np.array(y_values), 2)
    return coeffs,residuals



def get_quadratic_regression_with_ci(x: list[float], y: list[float], confidence_level: float = 0.95):
    assert len(x) == len(y) and confidence_level >= 0 and confidence_level <= 1

    n = len(x)
    # Construct the design matrix A
    A = np.vstack([np.array(x)**2, np.array(x), np.ones(n)]).T

    # Perform least squares to find the coefficients
    coefficients, residual, _, _ = np.linalg.lstsq(A, y, rcond=None)

    # Calculate the standard error of the predictions
    p = len(coefficients)
    dof = n - p
    residuals = np.array(y) - (A @ coefficients)
    residual_std_error = np.sqrt(np.sum(residuals**2) / dof)

    # Calculate R^2 and the standard error of the predictions
    r_squared = (1 - residual / (n * np.var(y, ddof=1)))[0]

    # Calculate the t-value for the given confidence level
    t_value = t.ppf(1 - (1 - confidence_level) / 2, dof)
    
    # Define the nested prediction function
    def predict_with_ci(x_value: float):
        # Calculate the predicted values
        y_pred = coefficients[0] * x_value**2 + coefficients[1] * x_value + coefficients[2]
        # Calculate the standard error of the predicted values
        x_array = np.array([x_value])
        A_pred = np.vstack([x_array**2, x_array, np.ones(1)]).T
        y_std_error_m = residual_std_error * \
            np.sqrt(0 + np.diagonal(A_pred @ np.linalg.inv(A.T @ A) @ A_pred.T))
        y_std_error = residual_std_error * \
            np.sqrt(1 + np.diagonal(A_pred @ np.linalg.inv(A.T @ A) @ A_pred.T))
        # Calculate the lower and upper bounds of the confidence intervals
        conf_i = t_value * y_std_error_m[0]
        pred_i = t_value * y_std_error[0]
        return y_pred, conf_i, pred_i
       
    return predict_with_ci, residual_std_error, coefficients, r_squared


def errors(X, Y, eq):
    error = 0.
    for i in range(len(X)):
        error += (eq(X[i])-Y[i]) ** 2
    return error


def cnd_rt_quad_regression_optimal(cnd, rt, confidence_level=0.95):
    k = 3.0
    ecn = [cal_ecn(i[0], i[1], k) for i in cnd]
    eq, std_error, coefficients,r_square = get_quadratic_regression_with_ci(
        ecn, rt, confidence_level)
    for _k in np.arange(config.ECN_K_RANGE[0], config.ECN_K_RANGE[1], config.ECN_K_RANGE[2]):
        _ecn = [cal_ecn(i[0], i[1], _k) for i in cnd]
        _eq, _std_error, _coefficients, _r_square = get_quadratic_regression_with_ci(
            _ecn, rt, confidence_level)
        if _std_error < std_error:
            eq = _eq
            ecn = _ecn
            std_error = _std_error
            k = _k
            coefficients = _coefficients
            r_square = _r_square
    return eq, std_error, k, ecn, coefficients, r_square


def remove_null_cells(X: list, Y: list):
    i = 0
    while i < len(X):
        if X[i] is None or Y[i] is None:
            X.pop(i)
            Y.pop(i)
        else:
            i += 1


def ReadECNProfiles():
    ecn_profile = dict()
    file_list = os.listdir(config.ECN_DATA_DIRECTORY)
    for file_name in file_list:
        pure_name = util.GetPureNameOfFile(file_name)
        cat_file_exist = False
        cat_name = ''
        for cat in config.CATEGORIES:
            name_r = cat.replace('[', '').replace(']', '')
            if pure_name == name_r:
                cat_file_exist = True
                cat_name = cat
                break

        if cat_file_exist:
            file_path = config.ECN_DATA_DIRECTORY+file_name
            sheet_names = xlh.getSheetNames(file_path)
            ecn_profile[cat_name] = []
            if len(sheet_names) > 0:
                for sheet in sheet_names:
                    data = []
                    xlh.readXlsx(file_path, data, sheet)
                    conf_v = data.pop(0)[1]
                    data.pop(0)
                    abbr_list = []
                    rt_list = []
                    for row in data:
                        if row[1] and row[2] and row[1] != '' and row[2] != '':
                            abbr_list.append(row[1])
                            rt_list.append(row[2])
                    CND_list = [get_CND_from_abbr(abbr) for abbr in abbr_list]
                    eq, error, k, ecn, coefficients,r_square = cnd_rt_quad_regression_optimal(
                        CND_list, rt_list, conf_v)
                    profile_item = ECNProfile(sheet,k,eq,coefficients,r_square,conf_v,ecn,rt_list)
                    ecn_profile[cat_name].append(profile_item)
    return ecn_profile


def pass_ecn_filter_mr(item: MatchResult, ecn_profiles: dict[str,list[ECNProfile]], filter_type: str):
    if item.category not in ecn_profiles.keys():
        return True
    profile = ecn_profiles[item.category]
    if (item.abbreviation and item.abbreviation != ''):
        for profile_item in profile:
            k = profile_item.k
            eq_with_ci = profile_item.equation
            cnd = get_CND_from_abbr(item.abbreviation)
            ecn = cal_ecn(cnd[0], cnd[1], k)
            x, ci, pi = eq_with_ci(ecn)
            if filter_type == "CONFIDENCE":
                if item.retention_time >= x-ci and item.retention_time <= x+ci:
                    return True
            elif filter_type == "PREDICTION":
                if item.retention_time >= x-pi and item.retention_time <= x+pi:
                    return True
        return False
    else:
        return True

def pass_ecn_filter_iso(item: IsotopicVariants, rt: float, ecn_profiles: dict[str,list[ECNProfile]], filter_type: str):
    category = item.mol.getValue("CATEGORY")
    abbr = item.mol.getValue("ABBREVIATION")

    if category not in ecn_profiles.keys():
        return True
    profile = ecn_profiles[category]
    if (abbr and abbr != ''):
        for profile_item in profile:
            k = profile_item.k
            eq_with_ci = profile_item.equation
            cnd = get_CND_from_abbr(abbr)
            ecn = cal_ecn(cnd[0], cnd[1], k)
            x, ci, pi = eq_with_ci(ecn)
            if filter_type == "CONFIDENCE":
                if rt >= x-ci and rt <= x+ci:
                    return True
            elif filter_type == "PREDICTION":
                if rt >= x-pi and rt <= x+pi:
                    return True
        return False
    else:
        return True

ecn_profile:dict[str,list[ECNProfile]] = dict()

if __name__ == "__main__":
    pass
