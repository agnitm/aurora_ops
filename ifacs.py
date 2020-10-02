#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:24:04 2020

@author: agnitm
"""

import numpy as np # Numerical Python
from spacepy.pybats import rim # To read in SWMF files
import ampere_read as amprd
import datetime as dt

def calc_I_swmf(fname):
    """
        See string for calc_I in SpacePy's pybats.rim
    """
   
    # Read the IE data file
    data = rim.Iono(fname)
    data['time'] = data.attrs['time']
   
    # Compute dLon and dLat
    data.dlon = data['n_psi'  ][0,3] - data['n_psi'  ][0,2]
    data.dlat = data['n_theta'][3,0] - data['n_theta'][2,0]
   
    # Calculate some physically meaningful values/units
    units = 1E-6*1E-6  # micro amps to amps, amps to MegaAmps
    R = (6371.0+110.0)*1000.0 # Radius of Earth + iono altitude
    dTheta = np.pi*data.dlat/180.
    dPhi   = np.pi*data.dlon/180.
   
    # -----NORTHERN HEMISPHERE-----
    # Get relevant values:
    colat     = data['n_theta']*np.pi/180.
    integrand = data['n_jr']*np.sin(colat)*dTheta*dPhi
    # Get locations of "up" and "down"
    loc_up = data['n_jr']>0
    loc_do = data['n_jr']<0
    data['n_I']     = units*R**2 * np.sum(integrand)
    data['n_Iup']   = units*R**2 * np.sum(integrand[loc_up])
    data['n_Idown'] = units*R**2 * np.sum(integrand[loc_do])
    data['n_Itotal']= units*R**2 * np.sum(np.abs(integrand)) * 0.5
   
    # -----SOUTHERN HEMISPHERE-----
    # Get relevant values:
    colat     = data['s_theta']*np.pi/180.
    integrand = data['s_jr']*np.sin(colat)*dTheta*dPhi
    # Get locations of "up" and "down"
    loc_up = data['s_jr']>0
    loc_do = data['s_jr']<0
    data['s_I']     = units*R**2 * np.sum(integrand)
    data['s_Iup']   = units*R**2 * np.sum(integrand[loc_up])
    data['s_Idown'] = units*R**2 * np.sum(integrand[loc_do])
    data['s_Itotal']= units*R**2 * np.sum(np.abs(integrand)) * 0.5

    return data['n_Itotal'], data['s_Itotal']

def calc_I_ampere(fname, time):
    """
        See string for calc_I in SpacePy's pybats.rim
    """
   
    # Read the IE data file
    data = amprd.ampere_read(fname, time)
    data['time'] = time
   
    # Compute dLon and dLat
    dlon = data['MLT'  ][0,3] - data['MLT'  ][0,2]
    dlat = data['Lat'][3,0] - data['Lat'][2,0]
   
    # Calculate some physically meaningful values/units
    units = 1E-6*1E-6  # micro amps to amps, amps to MegaAmps
    R = (6371.0+110.0)*1000.0 # Radius of Earth + iono altitude
    dTheta = np.pi*dlat/180.
    dPhi   = np.pi*dlon/180.
   
    # -----NORTHERN HEMISPHERE-----
    # Get relevant values:
    colat     = data['Lat']*np.pi/180.
    integrand = data['Jr']*np.sin(colat)*dTheta*dPhi
    # Get locations of "up" and "down"
    loc_up = data['Jr']>0
    loc_do = data['Jr']<0
    data['I']     = units*R**2 * np.sum(integrand)
    data['Iup']   = units*R**2 * np.sum(integrand[loc_up])
    data['Idown'] = units*R**2 * np.sum(integrand[loc_do])
    
    print(data['Iup'])
    
    return data

# # AMPERE time start - This should be fixed in future renditions of this code!
# tstart = dt.datetime(2011, 9, 26, 10, 0, 0) # Convert the numbers into a datetime
# t = tstart.timetuple() # Stripped the numbers into a timetuple

# northfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
#               '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.north.grd.ncdf')
#              .format(t[0], t[1], t[2], t[3]))

# southfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
#               '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.south.grd.ncdf')
#              .format(t[0], t[1], t[2], t[3]))

# time = dt.datetime(2011, 9, 27, 0, 30, 0)
# data = calc_I_ampere(northfile, time)