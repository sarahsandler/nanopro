# Mag Scatter
# Sarah [ses98]
# 22 April 2021

import numpy as np   
import matplotlib.pyplot as plt
import pylab as plt
import pandas as pd 

def mag_scatter(file,peaks):
    duration_peaks=[]
    duration=[]
    group_key=peaks.event
    for j in group_key:
            duration = file[j].attrs["duration_ms"]
            duration_peaks.append(duration)
    duration_df=pd.DataFrame([duration_peaks],
                    index=['duration'])
    duration=duration_df.T
    plt.plot(duration,peaks.mag1, 'o', color='red', alpha=0.05)
    plt.plot(duration,peaks.mag2, 'o', color='orange', alpha=0.05)
    plt.plot(duration,peaks.mag3, 'o', color='yellow', alpha=0.05)
    plt.plot(duration,peaks.mag4, 'o', color='green', alpha=0.05)
    plt.plot(duration,peaks.mag5, 'o', color='blue', alpha=0.05)
    plt.plot(duration,peaks.mag6, 'o', color='purple', alpha=0.05)
    show= plt.show()
    return show
