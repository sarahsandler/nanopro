
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

def dpeak_finder(event_data,height,threshold,distance,prominence,width,wlen):
    file=event_data # hdf5 file events
    group_keys_ln=[] # creating empty place to store filtered files
    group_key = list(file.keys()) #reading in events numbers
    ###########################################
    ############# noise filtering #############
    ###########################################
    for j in group_key:
        noise = file[j].attrs["rms_nA"]<0.04 #filtering out noisy events
        if noise == True:
            group_keys_ln.append(j)
    group_key=group_keys_ln #group keys for low noise events only    
    ###########################################
    ############# magnitudes #############
    ###########################################
    columns=['event','mag1','mag2','mag3','mag4','mag5','mag6','mag7','mag8','mag9'] # creating columns
    peak_data_all_mag=pd.DataFrame(columns=columns) #creating df with columns
    for i in group_key:
        current = file[i]['current_nA'][...] #current
        y= -1*current #inversing the current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence,width,wlen) #peak finder
        ############ mag
        if len(peaks)<11:  #storing 9 peak magnitudes
            event_df=pd.DataFrame([i])
            peak_data_mag=pd.DataFrame.from_dict(properties['peak_heights'])
            frames=(event_df,peak_data_mag)
            peak_data_mag=pd.concat(frames,join='outer')
            peak_data_mag=peak_data_mag.T
            size=len(peak_data_mag.columns)
            while (size<11):
                peak_data_mag['mag'+str(size)]=0
                size += 1
            peak_data_mag.columns=['event','mag1','mag2','mag3','mag4','mag5','mag6','mag7','mag8','mag9','mag10']
            frames=peak_data_all_mag,peak_data_mag
            peak_data_all_mag=pd.concat(frames)
            group_key=peak_data_all_mag.event
            columns=['event','pos1','pos2','pos3','pos4','pos5','pos6','pos7','pos8','pos9','pos10'] #creating columns for poisiton
            peak_data_all_pos=pd.DataFrame(columns=columns)
            
    ###########################################
    ############# positions #############
    ###########################################
    for i in group_key:
        current = file[i]['current_nA'][...]
        y= -1*current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence,width,wlen)
        ############ pos
        if len(peaks)<11:
            event_df=pd.DataFrame([i])
            peak_data_pos=pd.DataFrame.from_dict(peaks)
            frames=(event_df,peak_data_pos)
            peak_data_pos=pd.concat(frames,join='outer')
            peak_data_pos=peak_data_pos.T
            size=len(peak_data_pos.columns)
            while (size<11):
                peak_data_pos['pos'+str(size)]=0
                size += 1
            peak_data_pos.columns=['event','pos1','pos2','pos3','pos4','pos5','pos6','pos7','pos8','pos9','pos10']
            frames=peak_data_all_pos,peak_data_pos
            peak_data_all_pos=pd.concat(frames)
            store='good'
        else: 
            store='error'
    peak_data_all=pd.merge(peak_data_all_pos, peak_data_all_mag, left_on='event', right_on='event') #combining magnitude and position
    
    
   ###########################################
    ############# widths #############
    ###########################################
    columns=['event','wid1','wid2','wid3','wid4','wid5','wid6','wid7','wid8','wid9'] # creating columns
    peak_data_all_widths=pd.DataFrame(columns=columns) 
    for i in group_key:
        current = file[i]['current_nA'][...]
        y= -1*current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence,width,wlen)
            ############ pos
        if len(peaks)<10:
            event_df=pd.DataFrame([i])
            peak_data_widths=peak_data_widths=pd.DataFrame.from_dict(properties['widths'])
            frames=(event_df,peak_data_widths)
            peak_data_widths=pd.concat(frames,join='outer')            
            peak_data_widths=peak_data_widths.T
            size=len(peak_data_widths.columns)
            while (size<10):
                peak_data_widths['wid'+str(size)]=0
                size += 1
            peak_data_widths.columns=['event','wid1','wid2','wid3','wid4','wid5','wid6','wid7','wid8','wid9']
            frames=peak_data_all_widths,peak_data_widths
            peak_data_all_widths=pd.concat(frames)
            store='good'
        else: 
            store='error'
    peak_data_all=pd.merge(peak_data_all, peak_data_all_widths, left_on='event', right_on='event') #combining magnitude and position
    
    
    ###########################################
    ############# wls #############
    ###########################################
    columns=['event','wh1','wh2','wh3','wh4','wh5','wh6','wh7','wh8','wh9'] # creating columns
    peak_data_all_wh=pd.DataFrame(columns=columns) 
    for i in group_key:
        current = file[i]['current_nA'][...]
        y= -1*current
        peaks, properties = find_peaks(y, height, threshold, distance, prominence,width,wlen)
            ############ pos
        if len(peaks)<10:
            event_df=pd.DataFrame([i])
            peak_data_wh=pd.DataFrame.from_dict(properties["width_heights"])
            frames=(event_df,peak_data_wh)
            peak_data_wh=pd.concat(frames,join='outer')            
            peak_data_wh=peak_data_wh.T
            size=len(peak_data_wh.columns)
            while (size<10):
                peak_data_wh['wh'+str(size)]=0
                size += 1
            peak_data_wh.columns=['event','wh1','wh2','wh3','wh4','wh5','wh6','wh7','wh8','wh9']
            frames=peak_data_all_wh,peak_data_wh
            peak_data_all_wh=pd.concat(frames)
            store='good'
        else: 
            store='error'
    peak_data_all=pd.merge(peak_data_all, peak_data_all_wh, left_on='event', right_on='event') #combining magnitude and position
    
    
    ###########################################
    ############# durations #############
    ###########################################
    duration_peaks=[]
    group_key = list(file.keys())
    for i in group_key:
        duration = file[i].attrs["duration_ms"]
        duration_peaks.append(duration)
        dur_df=pd.DataFrame(duration_peaks)
        dur_df.columns=['duration']
    dur_df['event']=list(file.keys()) #creating duration df from list
    peak_data_all=pd.merge(peak_data_all, dur_df, left_on='event', right_on='event')
 
    ###########################################
    ############# areas #############
    ###########################################  
    a_peaks=[]
    group_key = list(file.keys())
    for i in group_key:
        area = file[i].attrs["area_fC"]
        a_peaks.append(area)
        a_df=pd.DataFrame(a_peaks)
        a_df.columns=['area']
    a_df['event']=list(file.keys())#creating area df from list
    peak_data_all=pd.merge(peak_data_all, a_df, left_on='event', right_on='event')
    
    #peak_data_all
    return peak_data_all
