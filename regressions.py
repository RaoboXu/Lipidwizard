from numpy import arange
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from math import sqrt

def mean(data:list):
    n = len(data)
    x_mean = 0
    y_mean = 0
    for i in range(n):
        x_mean += data[i][0]
        y_mean += data[i][1]
    return float(x_mean)/n,float(y_mean)/n

def SS_res(data:list,func):
    r=0
    for i in range(len(data)):
        yi=data[i][1]
        fi=func(data[i][0])
        # r += (data[i][1] - func(data[i][0])) ** 2
        r += (yi- fi) ** 2
    return float(r)

# def ECN(k,c,d):
#     return c-k*d

def SS_tot(data:list,y_mean):
    r=0
    for i in range(len(data)):
        r += (data[i][1]-y_mean) ** 2
    return float(r)

def R_square(data:list,func):
    x_mean,y_mean = mean(data)
    r = 1 - (SS_res(data,func))/(SS_tot(data,y_mean))
    return r

def R_square1(data:list,func):
    n = len(data)
    u=0
    b1=0
    b2=0
    x_mean,y_mean = mean(data)
    for i in range(n):
        u+=(data[i][0]-x_mean)*(data[i][1]-y_mean)
        b1+=(data[i][0]-x_mean) ** 2
        b2+=(data[i][1]-y_mean) ** 2
    return u / (sqrt(b1)*sqrt(b2))

def quad_regression(x: list[float], y: list[float]):
    assert len(x) == len(y)
    poly = PolynomialFeatures(degree=2)
    x_poly = poly.fit_transform(x)
    poly.fit(x_poly, y)
    linear = LinearRegression()
    linear.fit(x_poly, y)
    y_predicted = linear.predict(x_poly)
    error = 0
    for i in range(len(y)):
        error += (y[i][0]-y_predicted[i][0]) ** 2
    return poly,linear,error

def quad_regression_with_k(CND,RT):
    poly_optimal=None
    linear_optimal=None
    error_min = 1000000
    k_optimal = None
    for k in arange(1.0,3.0,0.01):
        ECN =[]
        for item in CND:
            ECN.append([item[0]-k*item[1]])
        poly, linear,error = quad_regression(ECN, RT)
        if error < error_min:
            poly_optimal = poly
            linear_optimal = linear
            error_min = error
            k_optimal = k
    x_poly=poly_optimal.fit_transform([[0],[1],[-1]])
    y=linear_optimal.predict(x_poly)
    c=y[0][0]
    b=0.5*(y[1][0]-y[2][0])
    a=y[1][0]-c-b
    print("The optimal K value is\t{:.3f}\nThe regression equation is\ty={:.4f}x^2+({:.4f}x)+({:.4f})\nThe error is\t{:.4f}\n".format(k_optimal,a,b,c,error_min))
    def func(x):
        return a*x*x+b*x+c
    ECN_RT =[]
    y_pred =[]
    y_true =[]
    for i in range(len(ECN)):
        ECN_RT.append([ECN[i][0],RT[i][0]])
        y_true.append(RT[i])
        y_pred.append(func(ECN[i][0]))
    r_square = R_square1(ECN_RT,func)
    return  func,k_optimal,error_min,r_square



def test_FA():
    CND = [[14, 0], [15, 0], [16, 1],[16, 1], [16, 0], [16, 0], [18, 4], [18, 3], [18, 3], [18, 3], [18, 2], [18, 2], [18, 1], [18, 1], [18, 0], [
        19, 0], [20, 5], [20, 4], [20, 3], [20, 2], [20, 1], [20, 0], [21, 0], [22, 6], [22, 5], [22, 4], [22, 1], [22, 0], [24, 1]]
    RT = [[6.52], [6.72], [6.59], [6.66], [7.01], [7.3], [6.28], [6.44], [6.47], [6.5], [6.68], [6.8], [7.09], [7.19], [
        7.57], [7.84], [6.4], [6.62], [6.79], [7.2], [7.6], [8.24], [8.49], [6.54], [6.66], [7], [8.24], [8.75], [8.74]]
    func,k,error,r_square = quad_regression_with_k(CND,RT)
    ECN =[]
    ecn_min = 1000000
    ecn_max = 0
    for item in CND:
        ecn = item[0]-k*item[1]
        ecn_min = min(ecn,ecn_min)
        ecn_max = max(ecn,ecn_max)
        ECN.append([ecn])
    pyplot.scatter(ECN,RT)
    x_test = []
    y_test = []
    for x in arange(ecn_min-1,ecn_max+1,0.1):
        x_test.append([x])
        y_test.append(func(x))
    pyplot.plot(x_test,y_test,label="k={:.3f},e={:.3f},r_square={:.3f}".format(k,error,r_square))
    return k,error

def test_CL_1():
    CND = [[56,0],[68,2],[64,4],[56,4],[72,4],       [64,0],[72,8],[57,4],[61,1]]
    RT  = [[47.44],[48.6 ],[47.62],[44.35],[48.6 ],        [48.6 ],[48.06],[44.82],[48.48]]
    func,k,error,r_square  = quad_regression_with_k(CND,RT)
    ECN =[]
    ecn_min = 1000000
    ecn_max = 0
    for item in CND:
        ecn = item[0]-k*item[1]
        ecn_min = min(ecn,ecn_min)
        ecn_max = max(ecn,ecn_max)
        ECN.append([ecn])
    pyplot.scatter(ECN,RT)
    x_test = []
    y_test = []
    for x in arange(ecn_min-1,ecn_max+1,0.1):
        x_test.append([x])
        y_test.append(func(x))
    pyplot.plot(x_test,y_test,label="k={:.3f},e={:.2f},r_square={:.2f}".format(k,error,r_square))
    return k,error

def test_CL_2():
    CND =[[56,0],[68,2],[64,4],[56,4],[72,4],[72,0],[64,0],[72,8],[57,4],[61,1]]
    RT =[[67.68],[68.59],[67.85],[64.83],[68.59],[68.69],[68.59],[68.27],[65.25],[68.5 ]]
    func,k,error,r_square  = quad_regression_with_k(CND,RT)
    ECN =[]
    ecn_min = 1000000
    ecn_max = 0
    for item in CND:
        ecn = item[0]-k*item[1]
        ecn_min = min(ecn,ecn_min)
        ecn_max = max(ecn,ecn_max)
        ECN.append([ecn])
    pyplot.scatter(ECN,RT)
    x_test = []
    y_test = []
    for x in arange(ecn_min-1,ecn_max+1,0.1):
        x_test.append([x])
        y_test.append(func(x))
    pyplot.plot(x_test,y_test,label="k={:.3f},e={:.2f},r_square={:.2f}".format(k,error,r_square))
    return k,error

def test_CL_3():
    CND=[[56,0],[68,2],[64,4],[56,4],[72,4],[72,0],[64,0],[72,8],[57,4],[61,1]]
    RT =[[80.9 ],[81.85],[80.95],[79.84],[81.85],[82.55],[81.85],[81.1 ],[79.98],[81.29]]
    func,k,error,r_square  = quad_regression_with_k(CND,RT)
    ECN =[]
    ecn_min = 1000000
    ecn_max = 0
    for item in CND:
        ecn = item[0]-k*item[1]
        ecn_min = min(ecn,ecn_min)
        ecn_max = max(ecn,ecn_max)
        ECN.append([ecn])
    pyplot.scatter(ECN,RT)
    x_test = []
    y_test = []
    for x in arange(ecn_min-1,ecn_max+1,0.1):
        x_test.append([x])
        y_test.append(func(x))
    pyplot.plot(x_test,y_test,label="k={:.3f},e={:.2f},r_square={:.2f}".format(k,error,r_square))
    return k,error



if __name__ == "__main__":
    
    fig_1=pyplot.figure()
    k,error=test_FA()
    fig_1.legend()

    # fig_2=pyplot.figure()

    # test_CL_1()
    # test_CL_2()
    # test_CL_3()
    # fig_2.legend()


    pyplot.show()