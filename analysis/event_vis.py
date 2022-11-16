# Event Visualization
# Sarah [ses98]
# 22 April 2021
import numpy as np   
import matplotlib
import matplotlib.pyplot as plt
import pylab as plt
import pandas as pd
from scipy.signal import find_peaks 

font = {'family' : 'Calibri',
        'weight' : 'normal',
        'size'   : 10}


def event_vis(event_set):
    file=event_set
    group_key = list(file.keys())
    for i in group_key:
        samplefreq_Hz = file[i].attrs["samplefreq_Hz"]
        current = file[i]['current_nA'][...]
        x = np.arange(current.size) / samplefreq_Hz * 1000
        plt.figure(dpi=200, figsize=(2,1))
        plt.style.use('default')
        matplotlib.rc('font', **font)
        plt.plot(x, current, color='black',linewidth=0.5)
        plt.title("Event: " + str([i]))
        plt.xlabel('Time [ms]')
        plt.ylabel('Current Drop[nA]')
        #plt.ylim(-0.50,0.05)
        #plt.xlim(-0.05,4)
        #plt.axis('off')
        show= plt.show()
    return show

def defined_event_vis(event_set,events):
    file=event_set
    group_key = events
    for i in group_key:
        samplefreq_Hz = file[i].attrs["samplefreq_Hz"]
        current = file[i]['current_nA'][...]
        x = np.arange(current.size) / samplefreq_Hz * 1000
        plt.figure(dpi=200, figsize=(2,1))
        plt.style.use('default')
        matplotlib.rc('font', **font)
        plt.plot(x, current, color='black',linewidth=0.5)
        plt.title("Event: " + str([i]))
        plt.xlabel('Time [ms]')
        plt.ylabel('Current Drop[nA]')
        show= plt.show()
    return show

def peak_event_vis(event_set,h,t,d,p,w):
    file=event_set
    group_key = list(file.keys())
    for i in group_key:
        current = file[i]['current_nA'][...]
        x= -1*current
        peaks, properties = find_peaks(x, height=h, threshold=t, distance=d, prominence=p,width=w)
        plt.figure(dpi=200, figsize=(3,1))
        plt.style.use('default')
        matplotlib.rc('font', **font)
        plt.plot(y, color='black')
        plt.plot(peaks, y[peaks], "x", color='red')
        plt.vlines(x=peaks, ymin=x[peaks] - properties["prominences"], ymax = x[peaks], color = "C1")
        plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"], xmax=properties["right_ips"], color = "C1")
        #plt.plot(np.zeros_like(y), "--", color="gray")
        plt.title("Event: " + str([i]))
        show= plt.show()
    return show

def defined_peak_event_vis(event_set,events,h,t,d,p,w,wl):
    file=event_set
    group_key = events
    for i in group_key:
        current = file[i]['current_nA'][...]
        x= -1*current
        peaks, properties = find_peaks(x, height=h, threshold=t, distance=d, prominence=p,width=w,wlen=wl)
        plt.figure(dpi=200, figsize=(2,1))
        plt.style.use('default')
        matplotlib.rc('font', **font)
        plt.plot(x, color='black')
        plt.plot(peaks, x[peaks], "x", color='red')
        #plt.vlines(x=peaks, ymin=x[peaks] - properties["prominences"], ymax = x[peaks], color = "C1")
        #plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"], xmax=properties["right_ips"], color = "C1")
        #plt.plot(np.zeros_like(y), "--", color="gray")
        plt.title("Event: " + str([i]))
        show= plt.show()
    return show
