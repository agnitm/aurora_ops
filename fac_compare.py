#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fac_compare.py
--------------

This module reads in netCDF files from AMPERE Satellite constellation and
converts them into regular data matrices to compare with SWMF-RIM.

Created on Thu Oct  1 01:37:51 2020

@author: Agnit Mukhopadhyay
         Climate and Space Sciences and Engineering
         University of Michigan, Ann Arbor
"""

import ampere_read # AMPERE File Reader
import swmf_read # SWMF IE File Reader
import ifacs # Integrated FACs Calculator
import numpy as np # Numerical Python
import matplotlib.pyplot as plt # Mathematical Plotting Library
import netCDF4 as ncdf # Library to read in netCDF files
import datetime as dt # Library to work with dates and times
from matplotlib.colors import LinearSegmentedColormap as lsc # Better Contour colormap
from spacepy.pybats import rim # To read in SWMF files
import matplotlib.colors as colors # Module required to use Normalize function
from matplotlib.ticker import MaxNLocator # Ticks Operations


#====================== AMPERE FILE INFORMATION ==============================

# AMPERE time start - This should be fixed in future renditions of this code!
tstart = dt.datetime(2011, 9, 26, 10, 0, 0) # Convert the numbers into a datetime
t = tstart.timetuple() # Stripped the numbers into a timetuple

northfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
              '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.north.grd.ncdf')
             .format(t[0], t[1], t[2], t[3]))

southfile = (('./AMPERE/Sept2011_Event_CUSIA/' + 
              '{0:4d}{1:0=2d}{2:0=2d}.{3:0=2d}00.86400.120.south.grd.ncdf')
             .format(t[0], t[1], t[2], t[3]))

# Path to Plots Folder
fpath = './Plots/Sept2011_Event_CUSIA/'

#=============================================================================
#=============================================================================
#=============================================================================

def fac_plot(nAMPERE_file, sAMPERE_file, SWMF_fname, sat_point, time, 
             lines=False, debug=False, max_colat = 40.):
    """

    Parameters
    ----------
    n_AMPERE : Dictionary
        Contains values from the AMPERE Northern Hemipshere.
    s_AMPERE : Dictionary
        Contains values from the AMPERE Southern Hemipshere.
    SWMF : Dictionary
        Contains values from the SWMF IE File.
    sat_point : float
        Contains saturation point value.

    Returns
    -------
    None. Saves Plot...

    """
    
    # Read in files and store data onto dictionaries
    n_AMPERE = ampere_read.ampere_read(nAMPERE_file, t_date)#, debug=True)
    s_AMPERE = ampere_read.ampere_read(sAMPERE_file, t_date)#, debug=True)
    SWMF = swmf_read.swmf_read(swmf_fname)#, debug=True)
    
    
    
    fig = plt.figure(figsize=(12,9))
    ax1 = plt.subplot(221, projection = 'polar') # Polar Plot
    ax2 = plt.subplot(222, projection = 'polar') # Polar Plot
    ax3 = plt.subplot(223, projection = 'polar') # Polar Plot
    ax4 = plt.subplot(224, projection = 'polar') # Polar Plot
    axes = [ax1, ax2, ax3, ax4] # Required for colorbar later...
    
    # Saturate Plots
    for J_r in (n_AMPERE['Jr'], s_AMPERE['Jr'], SWMF['n_Jr'], SWMF['s_Jr']):
        loc = J_r > sat_point
        J_r[loc] = sat_point

        loc = J_r < (-1 * sat_point)
        J_r[loc] = -1 * sat_point
    
    if debug: print(np.max(SWMF['n_Jr']))
    
    # Contour levels
    n = 20
    max_jr = np.max([np.max(n_AMPERE['Jr']), np.max(s_AMPERE['Jr']), 
                     np.max(SWMF['n_Jr']), np.max(SWMF['s_Jr']), sat_point])
    min_jr = np.min([np.min(n_AMPERE['Jr']), np.min(s_AMPERE['Jr']), 
                     np.min(SWMF['n_Jr']), np.min(SWMF['s_Jr']), -1. * sat_point])
    lev = np.linspace(min_jr, max_jr, n)
    
    if debug: print(max_jr, min_jr)
    
    font = {
            'color' : 'k'
            }
    label_color = 'k'
    
    
    
    # Filled Contour Plot with Geometry
    amp_north = ax1.contourf(n_AMPERE['MLT'], n_AMPERE['Lat'], n_AMPERE['Jr'], 
                             lev, cmap='bwr', norm=colors.Normalize(
                                 vmin = min_jr, vmax = max_jr))
    amp_south = ax3.contourf(s_AMPERE['MLT'], s_AMPERE['Lat'], s_AMPERE['Jr'], 
                             lev, cmap='bwr', norm=colors.Normalize(
                                 vmin = min_jr, vmax = max_jr)) 
    
    swm_north = ax2.contourf(SWMF['n_MLT'], SWMF['n_Lat'], SWMF['n_Jr'], 
                             lev, cmap='bwr', norm=colors.Normalize(
                                 vmin = min_jr, vmax = max_jr)) 
    swm_south = ax4.contourf(SWMF['s_MLT'], SWMF['s_Lat'], SWMF['s_Jr'], 
                             lev, cmap='bwr', norm=colors.Normalize(
                                 vmin = min_jr, vmax = max_jr)) 
            
    # Normal Contour Plot for lines
    if lines:
        ax1.contour(n_AMPERE['MLT'], n_AMPERE['Lat'], n_AMPERE['Jr'], lev,
                    linewidths = 0.75, colors = 'k')
        ax2.contour(s_AMPERE['MLT'], s_AMPERE['Lat'], s_AMPERE['Jr'], lev,
                    linewidths = 0.75, colors = 'k')
        ax3.contour(SWMF['n_MLT'], SWMF['n_Lat'], SWMF['n_Jr'], lev,
                    linewidths = 0.75, colors = 'k')
        ax4.contour(SWMF['s_MLT'], SWMF['s_Lat'], SWMF['s_Jr'], lev,
                    linewidths = 0.75, colors = 'k')

            
    # Common Colour Bar
    cbarticks = MaxNLocator(8)
    cb = fig.colorbar(amp_north, ticks = cbarticks, shrink=0.85, pad=0.08, 
                      ax = axes)
    cb.set_label('FAC ($\mu A/m^2$)', fontsize=25, fontdict = font)
    cb.ax.tick_params(labelsize=18, colors = label_color)
    
    # Latitudinal Limit
    for ax in axes:
        ax.set_ylim(0., max_colat)
    
    # ========================
    # MLT + Latitudinal Labels
    
    xticks = [0, 45.*np.pi/180., np.pi/2, 135.*np.pi/180., np.pi, 
              225.*np.pi/180., 3*np.pi/2, 315.*np.pi/180.]
    # ax1
    mlt_labels = ['06', '', '', '', '', '', '00 MLT', '']
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(mlt_labels)
    
    # ax2
    mlt_labels = ['06', '', '', '', '18', '', '00 MLT', '']
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(mlt_labels)
    
    # ax3
    mlt_labels = ['06', '', '12', '', '', '', '00 MLT', '']
    ax3.set_xticks(xticks)
    ax3.set_xticklabels(mlt_labels)
    
    # ax4
    mlt_labels = ['06', '', '12', '', '18', '', '00 MLT', '']
    ax4.set_xticks(xticks)
    ax4.set_xticklabels(mlt_labels)
    
    # Limiting the Latitude
    lat_labels = ['$N$', '', r'70$^0$', '', r'50$^0$']
    #yticks = np.linspace(0, 30., 16)
    yticks = [0, 10, 20, 30, 40]
    
    for ax in axes:
        ax.tick_params(labelsize=15)#, colors = 'white')
        ax.set_yticks(yticks)
        ax.set_yticklabels(lat_labels)
        
    # Set Titles
    ax1.set_ylabel('Northern', fontsize = 25)
    ax3.set_ylabel('Southern', fontsize = 25)
    ax1.set_title('AMPERE', fontsize = 25)
    ax2.set_title('SWMF-MAGNIT', fontsize = 25)
    
    t_label = ('Time: {0}-{1:0=2d}-{2:0=2d} ' + 
               '{3:0=2d}:{4:0=2d}:{5:0=2d} UT').format(t[0], t[1], t[2], t[3], 
                                                      t[4], t[5])
    plt.xlabel(t_label, fontsize=20, labelpad = 15)
    
    # Integrated FAC printing
    
    ifac = 10.23456
    # ax1
    plt.text(0.8, 0.075, 'iFAC (Total)', fontsize=15, transform=ax1.transAxes,
             verticalalignment='top')
    plt.text(0.8, 0.00, 'N/A', fontsize=15, 
             transform=ax1.transAxes, verticalalignment='top')
    
    # ax2
    plt.text(0.8, 0.075, 'iFAC (Total)', fontsize=15, transform=ax3.transAxes,
             verticalalignment='top')
    plt.text(0.8, 0.00, 'N/A', fontsize=15, 
             transform=ax3.transAxes, verticalalignment='top')
    
    
    # SWMF iFACs
    n_swmf_ifac, s_swmf_ifac = ifacs.calc_I_swmf(SWMF_fname)
    
    # ax3
    plt.text(0.8, 0.075, 'iFAC (Total)', fontsize=15, transform=ax2.transAxes,
             verticalalignment='top')
    plt.text(0.8, 0.00, '{:.2f} MA'.format(n_swmf_ifac), fontsize=15, 
             transform=ax2.transAxes, verticalalignment='top')
    
    # ax4
    plt.text(0.8, 0.075, 'iFAC (Total)', fontsize=15, transform=ax4.transAxes,
        verticalalignment='top')
    plt.text(0.8, 0.00, '{:.2f} MA'.format(s_swmf_ifac), fontsize=15, 
             transform=ax4.transAxes, verticalalignment='top')

    savefile = (fpath + '{0}{1:0=2d}{2:0=2d}_' + 
               '{3:0=2d}{4:0=2d}{5:0=2d}_000').format(t[0], t[1], t[2], t[3], 
                                                      t[4], t[5])            
    plt.savefig(savefile, dpi = 300)#, transparent = True)
    plt.show(); plt.close()

#=============================================================================
#=============================================================================
#=============================================================================
#=============================================================================

# MAIN FUNCTION:

# The Great Loop of our times....

# We loop around a start time and end_time
t_start = dt.datetime(2011, 9, 26, 14, 8, 0)
t_end = dt.datetime(2011, 9, 26, 14, 12, 0) #dt.datetime(2011, 9, 27, 9, 58, 0)

t_date = t_start

while(t_date <= t_end):
    t = t_date.timetuple() # Stripped the numbers into a timetuple
    swmf_fname = (('./SWMF-MAGNIT/Sept2011_Event_CUSIA/' +
                   'it{0}{1:0=2d}{2:0=2d}_{3:0=2d}{4:0=2d}{5:0=2d}_000.idl')
                  .format(str(t[0])[2:4], t[1], t[2], t[3], t[4], t[5]))
    
    fac_plot(northfile, southfile, swmf_fname, 1.5, t)#, lines=True)
    t_date = t_date + dt.timedelta(minutes=2)