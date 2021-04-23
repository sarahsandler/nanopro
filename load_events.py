# Load Events
# Sarah [ses98]
# 22 April 2021

import h5py

def load_data(filefolder):
    data_folder = "/Users/ses98/Desktop/EVENTS/"
    filefolder=filefolder
    filepath = data_folder + filefolder + "/"
    events_hdf5 = "events.hdf5"
    e_fp= filepath + events_hdf5 #events file path
    event_data=h5py.File(e_fp, 'r')
    return event_data

