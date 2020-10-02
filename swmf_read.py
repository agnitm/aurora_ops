#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
swmf_read.py
------------

This module reads in IDL files from SWMF Ionospheric Electrodynamics (IE) 
module and converts them into regular data matrices to compare with AMPERE 
data.

Created on Tue Jun  5 15:35:01 2018
Last Update on Thu Oct  1 00:25:36 2020

@author: Agnit Mukhopadhyay
         Climate and Space Sciences and Engineering
         University of Michigan, Ann Arbor
"""

import numpy as np # Numerical Python
import matplotlib.pyplot as plt # Mathematical Plotting Library
from spacepy.pybats import rim # To read in SWMF files

# For either hemisphere
def swmf_read(fname, debug=False):
    """
    This function reads in an IDL file to help plot SWMF data on a polar plot 
    based on Latitude and magnetic local time (MLT) data.
    For further information, please refer to the SWMF Manual and/or 
    spacepy.pybats.rim manual for data structures.
    
    Input:
    ------
        fname     SWMF event filename for a given time
    
    Output:
    -------
        dict    Dictionary containing latitude, longitude and FACs for North
                and North Hemispheres.
            
    """
    
    # Retrieve data from file !!!
    data = rim.Iono(fname)
    
    # Get size of array, and elements in dictionary
    if debug: 
        print(data.attrs['ntheta'], data.attrs['nphi'])
        print(data.keys())

    # Store everything in a separate dictionary
    swmf_data = {}
    swmf_data['n_MLT'] = data['n_psi']*np.pi/180.0+np.pi/2.
    swmf_data['n_Lat'] = data['n_theta']
    swmf_data['n_Jr'] = np.array(data['n_jr'])
    swmf_data['s_MLT'] = data['s_psi']*np.pi/180.0+np.pi/2.
    swmf_data['s_Lat'] = 180. - data['s_theta']
    swmf_data['s_Jr'] = np.array(data['s_jr'])
    
    if debug:
        # Test Plot for SWMF
        ax1 = plt.subplot(121, projection = 'polar') # Polar Plot
        ax2 = plt.subplot(122, projection = 'polar') # Polar Plot
        ax1.contourf(swmf_data['n_MLT'], swmf_data['n_Lat'], swmf_data['n_Jr'], 
                     cmap='bwr')
        ax2.contourf(swmf_data['s_MLT'], swmf_data['s_Lat'], swmf_data['s_Jr'], 
                     cmap='bwr')
        plt.show()

    return swmf_data # Return plottable data to user...

#=============================================================================

# MAIN FUNCTION:

# t_date = dt.datetime(2011, 9, 26, 15, 0, 0)
# t = t_date.timetuple() # Stripped the numbers into a timetuple

# t_end = dt.datetime(2011, 9, 26, 15, 4, 0)

# # The year formatting is done differently because SWMF IE files start with the 
# # last two digits of the year

# while(t_date < t_end):
#     t = t_date.timetuple() # Stripped the numbers into a timetuple
#     filename = (('./SWMF-MAGNIT/Sept2011_Event_CUSIA/' +
#                   'it{0}{1:0=2d}{2:0=2d}_{3:0=2d}{4:0=2d}{5:0=2d}_000.idl')
#                 .format(str(t[0])[2:4], t[1], t[2], t[3], t[4], t[5]))
    
#     print(filename)
#     SWMF_Data = swmf_read(filename)#, debug=True)
#     t_date = t_date + dt.timedelta(minutes = 2)


#     # Test Plot for SWMF
#     ax1 = plt.subplot(121, projection = 'polar') # Polar Plot
#     ax2 = plt.subplot(122, projection = 'polar') # Polar Plot
#     ax1.contourf(SWMF_Data['n_MLT'], SWMF_Data['n_Lat'], SWMF_Data['n_Jr'], 
#                   cmap='bwr')
#     ax2.contourf(SWMF_Data['s_MLT'], SWMF_Data['s_Lat'], SWMF_Data['s_Jr'], 
#                   cmap='bwr')
#     plt.show()