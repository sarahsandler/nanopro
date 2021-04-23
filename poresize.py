# Pore Sizer
# Sarah [ses98]
# 22 April 2021

import h5py     
import numpy as np   
import matplotlib.pyplot as plt
import pylab as plt
import pandas as pd 
from scipy.signal import find_peaks 
from scipy import stats
import ipywidgets as widgets
from IPython import display
from scipy.interpolate import interp1d
import pkg_resources
from shutil import copyfile
from sympy import symbols, solve
from sympy.solvers import solve
from sympy import Symbol, real_root
import os

def poresize(data_folder,sample_conc):
#reading in 
    path= 'C:/Users/ses98/Desktop/EVENTS/' + data_folder
    os.getcwd()
    os.chdir(path)

    #copying IV noise
    copyfile('IV curve and noise.dat', 'IV curve and noise.txt')
    IV = pd.read_csv('IV curve and noise.txt', delimiter="\t",skiprows=[0],names=['Voltage','Current', 'Noise'])

    #calculating resistance
    current=IV.Current
    voltage=IV.Voltage
    coeff = np.polyfit(voltage, current, 1) # fitting the IV curve
    col = '--m'
    resohm = 1/(coeff[0]*1E-6)

    # reading in LiCl curve
    filepath = "/Users/ses98/OneDrive - University of Cambridge/PhD/Analysis Scripts/"
    os.getcwd()
    os.chdir(filepath)
    licl=pd.read_csv('conductivity.csv',skiprows=[1], header=0, names=['c','cond'])

    # conductivity of lithium chloride
    conc=licl.c
    cond=licl.cond
    f = interp1d(conc, cond, kind='cubic')
    xnew = np.arange(1, 5, 1)
    ynew = f(xnew)   # use interpolation function returned by `interp1d`
    col_names=['cond']
    licl_df=pd.DataFrame(ynew,xnew,columns=col_names)
    ##############################
    #sample_conc=2 ### user input!
    ##############################
    val=sample_conc-1
    cond=licl_df.iloc[val][0] 

    # calculating pore size
    psi1=0.092
    psi2=0.046
    L=(100E-9)
    res=resohm
    d = Symbol('d')
    poresize=solve(((4*L/(cond*np.pi*d*(d+2*L*np.tan(psi1))))+(2/(cond*np.pi*np.tan(psi2)*(d+2*L*np.tan(psi1))))+(1/(2*cond*d)))-res, d)
    poresize=poresize[1]*1E9
    return (poresize)

