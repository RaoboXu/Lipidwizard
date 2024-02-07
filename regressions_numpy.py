import numpy as np
from matplotlib import pyplot
from scipy.stats import t
from math import sqrt
from xlHelper import readXlsx
import re
from config import config
import os.path

def equation_str(coefficients):
    str = "y={:.6f}x^2{}{:.6f}x{}{:.6f}".format(
        coefficients[0], "+" if coefficients[1] > 0 else "", coefficients[1], "+" if coefficients[2] > 0 else "", coefficients[2])
    return str

def get_CND_from_abbr(abbr:str):
    CND = re.findall(r'[\d.]+:[\d.]+', abbr)
    if(len(CND)>0):
        CND = CND[0]
        CND = [int(i) for i in CND.split(':')]
        return CND
    return 'ERROR'

def ECN_data_exist(category:str):
    return os.path.exists(config.ECN_DATA_DIRECTORY+category)

def cal_ecn(c, d, k=2.00):
    return c-k*d


def regression_quad(ecn, rt):
    assert len(ecn) == len(rt)
    params = np.polyfit(ecn, rt, 2)
    return np.poly1d(params)


def errors(X, Y, eq):
    error = 0.
    for i in range(len(X)):
        error += (eq(X[i])-Y[i]) ** 2
    return error


def cnd_rt_quad_regression_optimal(cnd, rt):
    k = 3.0
    ecn = [cal_ecn(i[0], i[1], k) for i in cnd]
    eq = regression_quad(ecn, rt)
    error = errors(ecn, rt, eq)
    ks = []
    es = []
    for _k in np.arange(1.0, 3.0, 0.01):
        _ecn = [cal_ecn(i[0], i[1], _k) for i in cnd]
        _eq = regression_quad(_ecn, rt)
        _error = errors(_ecn, rt, _eq)
        ks.append(_k)
        es.append(_error)
        if _error < error:
            eq = _eq
            ecn = _ecn
            error = _error
            k = _k
    return eq, error, k, ecn


def cnd_rt_quad_regression_with_k(cnd, rt, k):
    ecn = [cal_ecn(i[0], i[1], k) for i in cnd]
    eq = regression_quad(ecn, rt)
    error = errors(ecn, rt, eq)
    return eq, error, k, ecn


def confident_interval(X, eq, confidence_value):
    m = np.mean(X)
    s = np.std(X)
    n = len(X)
    internal = t.ppf(1-confidence_value/2, n-2) * s / sqrt(n)

    def ci(x):
        return eq(x) - internal, eq(x) + internal
    return ci

def remove_null_cells(X:list,Y:list):
    i=0
    while i < len(X):
        if X[i] is None or Y[i] is None:
            X.pop(i)
            Y.pop(i)
        else:
            i += 1
    
def draw_regression(canva:pyplot.Axes,CND,RT):
    remove_null_cells(CND,RT)
    eq, error, k, ecn = cnd_rt_quad_regression_optimal(CND, RT)
    canva.scatter(ecn, RT, color='gray')
    X = np.arange(np.min(ecn)-1, np.max(ecn)+1, 1)
    Y = [eq(i) for i in X]
    ci = confident_interval(ecn, eq, 0.75)
    Y_down = [ci(i)[0] for i in X]
    Y_up = [ci(i)[1] for i in X]

    fit_line, = canva.plot(X, Y, label="{},\nk={:.2f},\nerror={:.2f}".format(
        equation_str(eq.coefficients), k, error))
    canva.fill_between(X, Y_down, Y_up, alpha=0.4, linewidth=0)
    canva.legend(loc='upper left')






def test_FA():
    CND = [[14, 0], [15, 0], [16, 1], [16, 1], [16, 0], [16, 0], [18, 4], [18, 3], [18, 3], [18, 3], [18, 2], [18, 2], [18, 1], [18, 1], [18, 0], [
        19, 0], [20, 5], [20, 4], [20, 3], [20, 2], [20, 1], [20, 0], [21, 0], [22, 6], [22, 5], [22, 4], [22, 1], [22, 0], [24, 1]]
    RT = [6.52, 6.72, 6.59, 6.66, 7.01, 7.3, 6.28, 6.44, 6.47, 6.5, 6.68, 6.8, 7.09, 7.19,
          7.57, 7.84, 6.4, 6.62, 6.79, 7.2, 7.6, 8.24, 8.49, 6.54, 6.66, 7, 8.24, 8.75, 8.74]
    return CND, RT


def test_CL_1():
    CND = [[56, 0], [68, 2], [64, 4], [56, 4], [
        72, 4],       [64, 0], [72, 8], [57, 4], [61, 1]]
    RT = [47.44, 48.6, 47.62, 44.35, 48.6, 48.6, 48.06, 44.82, 48.48]
    return CND, RT


def test_CL_2():
    CND = [[56, 0], [68, 2], [64, 4], [56, 4], [72, 4],
           [72, 0], [64, 0], [72, 8], [57, 4], [61, 1]]
    RT = [67.68, 68.59, 67.85, 64.83, 68.59, 68.69, 68.59, 68.27, 65.25, 68.5]
    return CND, RT


def test_CL_3():
    CND = [[56, 0], [68, 2], [64, 4], [56, 4], [72, 4],
           [72, 0], [64, 0], [72, 8], [57, 4], [61, 1]]
    RT = [80.9, 81.85, 80.95, 79.84, 81.85, 82.55, 81.85, 81.1, 79.98, 81.29]
    return CND, RT


def test_PG():
    xlsx_content = []
    headers = ['name',	'abbr',	'CN',	'DB',	'calculated ECN',
               'R.T 1 (min)',	'R.T 2 (min)',	'RT 3 (min)',	'R.T 4 (min)','m/z POS', 'm/z POS']
    if 'SUCCESS' == readXlsx('./data/ECN DATA.xlsx', xlsx_content, 'Phosphatidylglycerol PG',headers):
        xlsx_content.pop(0)
        CND = [[item[2],item[3]] for item in xlsx_content]
        RT=[]
        RT.append([item[5] for item in xlsx_content])
        RT.append([item[6] for item in xlsx_content])
        RT.append([item[7] for item in xlsx_content])
        RT.append([item[8] for item in xlsx_content])
        return CND,RT
    else:
        return [[],[]]

def test_PE():
    xlsx_content = []
    headers = ['name',	'abbr',	'CN',	'DB',	'calculated ECN',
               'R.T 1 (min)',	'R.T 2 (min)',	'RT 3 (min)']
    if 'SUCCESS' == readXlsx('./data/ECN DATA.xlsx', xlsx_content, 'Phosphatidylethanolamine PE',headers):
        xlsx_content.pop(0)
        CND = [[item[2],item[3]] for item in xlsx_content]
        RT=[]
        RT.append([item[5] for item in xlsx_content])
        RT.append([item[6] for item in xlsx_content])
        RT.append([item[7] for item in xlsx_content])
        return CND,RT
    else:
        return [[],[]]

def test_PC():
    xlsx_content = []
    headers = ['name',	'abbr',	'CN',	'DB',	'calculated ECN',
               'R.T 1 (min)',	'R.T 2 (min)']
    if 'SUCCESS' == readXlsx('./data/ECN DATA.xlsx', xlsx_content, 'Phosphatidylcholine PC',headers):
        xlsx_content.pop(0)
        CND = [[item[2],item[3]] for item in xlsx_content]
        RT=[]
        RT.append([item[5] for item in xlsx_content])
        RT.append([item[6] for item in xlsx_content])
        return CND,RT
    else:
        return [[],[]]

def test_PS():
    xlsx_content = []
    headers = ['name',	'abbr',	'CN',	'DB',	'calculated ECN',
               'R.T 1 (min)']
    if 'SUCCESS' == readXlsx('./data/ECN DATA.xlsx', xlsx_content, 'Phosphatidylserine PS',headers):
        xlsx_content.pop(0)
        CND = [[item[2],item[3]] for item in xlsx_content]
        RT=[]
        RT.append([item[5] for item in xlsx_content])
        return CND,RT
    else:
        return [[],[]]
    


if __name__ == "__main__":
    

    CND,RTS = test_FA()
    fig, ([sub1,sub2])=pyplot.subplots(1,2)

    draw_regression(sub1,CND,RTS)
    # draw_regression(sub2,CND,RTS[1])
    pyplot.show()

    # abbr = "PE36:0"
    # cnd = get_CND_from_abbr(abbr)
    # print(cnd)

