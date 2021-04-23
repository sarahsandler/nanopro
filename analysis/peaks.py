# Peak Finder
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

def peak_finder(event_data,height,threshold,distance,prominence):
    file=event_data
    group_keys_ln=[]
    group_key = list(file.keys()) 
    for j in group_key:
        noise = file[j].attrs["rms_nA"]<0.025
        if noise == True:
            group_keys_ln.append(j)
    group_key=group_keys_ln #group keys for low noise events only    
    columns=['event','mag1','mag2','mag3','mag4','mag5','mag6','mag7','mag8','mag9']
    peak_data_all_mag=pd.DataFrame(columns=columns)
    for i in group_key:
        current = file[i]['current_nA'][...]
        y= -1*current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence)
        ############ mag
        if len(peaks)<10:
            event_df=pd.DataFrame([i])
            peak_data_mag=pd.DataFrame.from_dict(properties['peak_heights'])
            frames=(event_df,peak_data_mag)
            peak_data_mag=pd.concat(frames,join='outer')
            peak_data_mag=peak_data_mag.T
            size=len(peak_data_mag.columns)
            while (size<10):
                peak_data_mag['mag'+str(size)]=0
                size += 1
            peak_data_mag.columns=['event','mag1','mag2','mag3','mag4','mag5','mag6','mag7','mag8','mag9']
            frames=peak_data_all_mag,peak_data_mag
            peak_data_all_mag=pd.concat(frames)
            group_key=peak_data_all_mag.event
            columns=['event','pos1','pos2','pos3','pos4','pos5','pos6','pos7','pos8','pos9']
            peak_data_all_pos=pd.DataFrame(columns=columns)
    for i in group_key:
        current = file[i]['current_nA'][...]
        y= -1*current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence)
        ############ pos
        if len(peaks)<10:
            event_df=pd.DataFrame([i])
            peak_data_pos=pd.DataFrame.from_dict(peaks)
            frames=(event_df,peak_data_pos)
            peak_data_pos=pd.concat(frames,join='outer')
            peak_data_pos=peak_data_pos.T
            size=len(peak_data_pos.columns)
            while (size<10):
                peak_data_pos['pos'+str(size)]=0
                size += 1
            peak_data_pos.columns=['event','pos1','pos2','pos3','pos4','pos5','pos6','pos7','pos8','pos9']
            frames=peak_data_all_pos,peak_data_pos
            peak_data_all_pos=pd.concat(frames)
            store='good'
        else: 
            store='error'
    peak_data_all=pd.merge(peak_data_all_pos, peak_data_all_mag, left_on='event', right_on='event')
    #peak_data_all
    return peak_data_all
