# Event Visualization
# Sarah [ses98]
# 22 April 2021
import numpy as np   
import matplotlib.pyplot as plt
import pylab as plt
import pandas as pd 

def event_vis(event_set):
    file=event_set
    group_key = list(file.keys())
    for i in group_key:
        samplefreq_Hz = file[i].attrs["samplefreq_Hz"]
        current = file[i]['current_nA'][...]
        x = np.arange(current.size) / samplefreq_Hz * 1000
        plt.figure()
        plt.style.use('ggplot')
        plt.plot(x, current, color='black')
        plt.title("Event: " + str([i]))
        plt.xlabel('Time [ms]')
        plt.ylabel('Current Drop[nA]')
        show= plt.show()
    return show

def peak_event_vis(event_set,sorted_events):
    file=event_set
    group_key = sorted_events
    for i in group_key:
        samplefreq_Hz = file[i].attrs["samplefreq_Hz"]
        current = file[i]['current_nA'][...]
        x = np.arange(current.size) / samplefreq_Hz * 1000
        plt.figure()
        plt.style.use('ggplot')
        plt.plot(x, current, color='black')
        plt.title("Event: " + str([i]))
        plt.xlabel('Time [ms]')
        plt.ylabel('Current Drop[nA]')
        show= plt.show()
    return show