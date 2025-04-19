import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy import odr

file=input("File Name: ")
sheet=input("Sheet Name: ")
xhead=input("x header: ")
yhead=input("y header: ")
xerrhead=input("x error header: ")
yerrhead=input("y error header: ")
functype=input("Function fit type(linear or ): ")

if file[-4:]=="xlsx":
    data=pd.read_excel(file,sheet_name=sheet)
elif file[:-4]==".csv":
    data=pd.read_csv(file)
else:
    print("Unsupported file type")

xdata=data[xhead]
ydata=data[yhead]

fig=plt.figure()


if xerrhead!="" and yerrhead!="":
    xerr=data[xerrhead]
    yerr=data[yerrhead]
    plt.errorbar(xdata,ydata,xerr=xerr,yerr=yerr,fmt='.k', capsize=3, ecolor="Red")
elif xerrhead!="":
    xerr=data[xerrhead]
    plt.errorbar(xdata,ydata,xerr=xerr,fmt='.k', capsize=3, ecolor="Red")
elif yerrhead!="":
    yerr=data[yerrhead]
    plt.errorbar(xdata,ydata,yerr=yerr,fmt='.k', capsize=3, ecolor="Red")
else:
    plt.scatter(xdata,ydata,color='black',marker=".")





plt.xlabel(xhead)
plt.ylabel(yhead)


if functype=="":
    plt.show()

elif functype=="linear":
    def func(x, a, b):
        return a*x+b
    if yerrhead!="":
        p_opt, p_cov = opt.curve_fit(func, xdata, ydata, sigma=yerr, absolute_sigma=True)
    else:
        p_opt, p_cov = opt.curve_fit(func, xdata, ydata, absolute_sigma=True)
    
    plt.plot(xdata,func(xdata, *p_opt))
    uncertainties = np.sqrt(np.diag(p_cov))
    print(p_opt, uncertainties)
    plt.show()






