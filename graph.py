# imports required libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy import odr
import sys

#retieves input from gui, to not use gui comment out the below and decomment the other code that sets the variables
file=sys.argv[1]
sheet=sys.argv[2]
xhead=sys.argv[3]
yhead=sys.argv[4]
xerrhead=sys.argv[5]
yerrhead=sys.argv[6]
functype=sys.argv[7]


'''
#allows the user to input required variables via the console
file=input("File Name: ")
sheet=input("Sheet Name: ")
xhead=input("x header: ")
yhead=input("y header: ")
xerrhead=input("x error header: ")
yerrhead=input("y error header: ")
functype=input("Function fit type(linear or ): ")
'''

#checks for file type and opens with pandas
if file[-4:]=="xlsx":
    data=pd.read_excel(file,sheet_name=sheet)
elif file[-4:]==".csv":
    data=pd.read_csv(file)
#if it is not a supported file type raises exception
else:
    raise Exception("Unsupported file type")

#gets the x and y data from  the file using the user given names of the headings
xdata=data[xhead]
ydata=data[yhead]

#creates a matplotlib figure
fig=plt.figure()


#for checks for any error columns and for the existing columns adds error bars to the figures as well as plotting all points
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




#adds label to the axes
plt.xlabel(xhead)
plt.ylabel(yhead)

#has ticks on all 4 sides go inwards (preference feel free to change)
plt.tick_params(direction='in', top=True, right=True)


#checks if user selected a linear fit
if functype=="Linear":
    #defines linear equation
    def func(x, a, b):
        return a*x+b
    #checks if error in both axes
    if xerrhead!="" and yerrhead!="":
        #due to x errors, requires different funchtion do defines it
        def funcodr(B,x):
            return B[0]*x+B[1]
        #uses funcodr to find best fit
        odrModel = odr.Model(funcodr)
        data = odr.RealData(xdata, ydata, sx=xerr, sy=yerr)
        podr = odr.ODR(data,odrModel, beta0=[1.0,0.0])
        out = podr.run()
        #outputs optimisation data to console
        out.pprint()
        #plots best fit
        plt.plot(xdata,func(xdata, *out.beta))
        
    elif xerrhead!="":
        #due to x errors, requires different funchtion do defines it
        def funcodr(B,x):
            return B[0]*x+B[1]
        #uses funcodr to find best fit
        odrModel = odr.Model(funcodr)
        data = odr.RealData(xdata, ydata, sx=xerr, sy=yerr)
        podr = odr.ODR(data,odrModel, beta0=[1.0,0.0])
        out = podr.run()
        #outputs optimisation data to console
        out.pprint()
        #plots best fit
        plt.plot(xdata,func(xdata, *out.beta))
        
    elif yerrhead!="":
        #uses opt.curve_fit to find the best fit
        p_opt, p_cov = opt.curve_fit(func, xdata, ydata, sigma=yerr, absolute_sigma=True)
        #plots best fit
        plt.plot(xdata,func(xdata, *p_opt))
        uncertainties = np.sqrt(np.diag(p_cov))
        #outputs optimisation data to console
        print(p_opt, uncertainties)
        
    else:
        #uses opt.curve_fit to find the best fit
        p_opt, p_cov = opt.curve_fit(func, xdata, ydata)
        #plots best fit
        plt.plot(xdata,func(xdata, *p_opt))
        uncertainties = np.sqrt(np.diag(p_cov))
        #outputs optimisation data to console
        print(p_opt, uncertainties)
        
    #adds legend (wip)
    plt.legend()

#displays plot
plt.show()





