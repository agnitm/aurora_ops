#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ampere_read.py
--------------

This module reads in netCDF files from AMPERE Satellite constellation and
converts them into regular data matrices to compare with SWMF-RIM.

Created on Tue Jun  5 15:35:01 2018
Last Update on Wed Sep 23 16:52:40 2020

@author: Agnit Mukhopadhyay
         Climate and Space Sciences and Engineering
         University of Michigan, Ann Arbor
"""

import numpy as np # Numerical Python
import matplotlib.pyplot as plt # Mathematical Plotting Library
import netCDF4 as ncdf # Library to read in netCDF files
import datetime as dt # Library to work with dates and times
import matplotlib.colors as colors # Module required to use Normalize function


# For Both Hemispheres
def ampere_read(fname, t_date, debug=False):
    """
    This function reads in a netCDF file and plots the AMPERE data to screen on
    a polar plot based on Latitude and magnetic local time (MLT) data.
    For reference, AMPERE data for Northern and Southern hemispheres are 
    accessible separately.
    
    Input:
    ------
        fname     AMPERE event filename for a given hemisphere
        t_date    Time (in YYYY-MM-DD HH:MM:SS UT format)
    
    Output:
    -------
        dict    Dictionary containing latitude, longitude and FACs for North
                and North Hemispheres.
            
    """
    
    # Identify if data is of Northern Hemisphere or Southern Hemisphere
    fchar = []; fchar[:] = fname.split("/")[-1]
    if (fchar[-14:-9] == ['n', 'o', 'r', 't', 'h']):
        hemi = 'north'
    else:
        hemi = 'south'
        
    if debug: print(hemi)
    
    # Retrieve data for given Hemisphere!!!
    data = ncdf.Dataset(fname)
    
    # Set Size of Matrices
    nLat = data.variables['nlat'][0] # Total Number of Latitudes
    nMLT = data.variables['nlon'][0] # total Number of MLTs
    nTime = len(data.variables['start_yr']) # Total Number of Minutes
    
    if debug: print(nLat, nMLT, nTime)
    
    if debug: print(data.variables.keys())
    
    # Make 2-D Matrix Map of the Latitude, Longitude and the Field Aligned Current
    Lat = np.zeros((nLat, nMLT + 1)) # 2D Matrix containing the Latitudes
    MLT = np.zeros((nLat, nMLT + 1)) # 2D Matrix containing the MLTs
    J_r = np.zeros((nLat, nMLT + 1)) # 2D Matrix containing the Jr
    # The + 1 is for the ghost cell on the end of the matrix
    
    Time = [] # Time Array
    # Assign values into Time Array
    for t in range(len(data.variables['start_yr'])):
        year = data.variables['start_yr'][t]
        month = data.variables['start_mo'][t]
        day = data.variables['start_dy'][t]
        hour = data.variables['start_hr'][t]
        minute = data.variables['start_mt'][t]
        Time.append(dt.datetime(year, month, day, hour, minute, 0))
    
    #print(Time[Time.index(t_date)], Time.index(t_date)) # DEBUG
    t_ind = Time.index(t_date) # Assign index of time you want to see here...
    
    if hour >= 0.: # Just a precautionary measure...
        # Write the data into 2D Matrix Variables
        for j in range(0, nMLT): # for all MLTs
            for i in range(0, nLat): # for all Latitudes
                index = i + j * nLat # Converting a 2D index into 1D
                
                # Save the data into the coefficient matrices
                mlat = 91. - data.variables['colat'][t_ind][index]
                mlon = data.variables['mlt'][t_ind][index]
                jr = data.variables['Jr'][t_ind][index]
                
                Lat[i][j] = mlat
                MLT[i][j] = mlon
                J_r[i][j] = jr
        # Return of the Ghost Cell
        for i in range(0, nLat): # for all Latitudes
            Lat[i][-1] = Lat[i][0]
            MLT[i][-1] = MLT[i][0] + nMLT
            J_r[i][-1] = J_r[i][0]
    
    # DEBUG: Print Data to screen
    if debug:
        print(Lat)
        print(MLT)
        print(J_r)
    
    # Convert MLT, Latitude and Jr data into directly plottable values
    if hemi == 'north':
        MLT_plot = MLT * np.pi/12. - np.pi/2.
        Lat_plot = 90. - Lat
        J_r_plot = J_r
    else:
        MLT_plot = MLT * np.pi/12. - np.pi/2.
        Lat_plot = 90. + Lat
        J_r_plot = J_r
    
    # DEBUG: Polar Plot
    if debug:
        ax1 = plt.subplot(111, projection = 'polar') # Polar Plot
        ax1.contourf(MLT_plot, Lat_plot, J_r_plot, cmap='bwr',
                     norm=colors.Normalize(vmin = -1.5, vmax = 1.5))
        plt.show()


    # Save everything in a dictionary
    ampere_data = {}
    ampere_data['MLT'] = MLT_plot
    ampere_data['Lat'] = Lat_plot
    ampere_data['Jr'] = J_r_plot

    return ampere_data # Return plottable data to user...


#=============================================================================

# MAIN FUNCTION:

# # AMPERE time start - This should be fixed in future renditions of this code!
# tstart = dt.datetime(2011, 9, 26, 10, 0, 0) # Convert the numbers into a datetime
# t = tstart.timetuple() # Stripped the numbers into a timetuple

# northfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
#               '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.north.grd.ncdf')
#              .format(t[0], t[1], t[2], t[3]))

# southfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
#               '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.south.grd.ncdf')
#              .format(t[0], t[1], t[2], t[3]))

# t_date = dt.datetime(2011, 9, 27, 0, 0, 0)
# AMPERE_Data = ampere_read(northfile, t_date)#, debug=True)


# # Test Plot for AMPERE
# ax1 = plt.subplot(111, projection = 'polar') # Polar Plot
# ax1.contourf(AMPERE_Data['MLT'], AMPERE_Data['Lat'], AMPERE_Data['Jr'], 
#              cmap='bwr')
# plt.show()
