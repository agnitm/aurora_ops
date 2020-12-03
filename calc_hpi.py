#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_hpi.py
===========
Compute the auroral hemispheric power from an SWMF IDL file.

Created on Wed Dec  2 03:45:37 2020

@author: Agnit Mukhopadhyay
         University of Michigan
         Ann Arbor, MI
"""

import numpy as np
from spacepy.pybats import rim

def calc_hpi(a, debug=False):
        '''
        Integrate auroral energy and number fluxes to get the following 
        values:
        tot_numflux:   The total number flux over one hemisphere.
        tot_aur_hpi:   The total energy flux over one hemisphere (in GW).

        Values are stored in the object with the prefix 'n_' or 's_', 
        to indicate the hemisphere for four different sources of precipitation: 
            'diff': Electron Diffuse
            'idif': Ion Diffuse
            'mono': Monoenergetic
            'bbnd': Broadband
        and may be accessed via self['n_diff']['tot_aur_hpi'], etc.

        Parameters
        ==========
        dict

        Returns
        =======
        obj


        Examples
        ========
        >>> a = rim.Iono('spacepy/tests/data/pybats_test/it000321_104510_000.idl.gz')
        >>> a.calc_I()
        >>> print(a['n_diff']['tot_numflux'])
        
        '''

        # Calculate some physically meaningful values/units
        units_eflux = 1E-9 # Watts to GigaWatts
        units_numflux = 1E+04 # cm^-2 to m^-2
        R = (6371.0+110.0)*1000.0 # Radius of Earth + iono altitude
        dTheta = np.pi * a.dlat/180.
        dPhi   = np.pi * a.dlon/180.
        
        hemi = ['n', 's']
        
        for h in hemi:
            # Get relevant values:
            colat     = a[h+'_theta']*np.pi/180.
            
            # -----DIFFUSE PRECIP-----
            a[h+'_diff'] = {}
            # Number Flux
            t = a[h+'_diff_ave-e'] * 1E03 * 11604
            diff_numflux = a[h+'_rt rho'] * t**0.5 * 1553.5632/1.66E-21
            integrand = (diff_numflux * np.sin(colat) * dTheta*dPhi)
            a[h+'_diff']['tot_numflux'] = units_numflux*R**2 * np.sum(integrand)
            # Energy Flux
            integrand = (a[h+'_diff_e-flux'] * np.sin(colat) * dTheta*dPhi)
            a[h+'_diff']['tot_aur_hpi'] = units_eflux*R**2 * np.sum(integrand)
            
            if debug:
                print((h+'-Diffuse:   ' +
                   'Total Number Flux = {:4.3E}   ' + 
                   'Auroral HPI = {:.3f}').format(a[h+'_diff']['tot_numflux'], 
                                                  a[h+'_diff']['tot_aur_hpi']))
                                                  
            # -----ION DIFF PRECIP-----
            a[h+'_idif'] = {}
            # Number Flux
            t = a[h+'_idif_ave-e'] * 1E03 * 11604 * 5
            idif_numflux = a[h+'_rt rho'] * t**0.5 * 36.26531/1.66E-21
            integrand = (idif_numflux * np.sin(colat) * dTheta*dPhi)
            a[h+'_idif']['tot_numflux'] = units_numflux*R**2 * np.sum(integrand)
            # Energy Flux
            integrand = (a[h+'_idif_e-flux'] * np.sin(colat) * dTheta*dPhi)
            a[h+'_idif']['tot_aur_hpi'] = units_eflux*R**2 * np.sum(integrand)
            
            if debug:
                print((h+'-IonDiff:   ' +
                   'Total Number Flux = {:4.3E}   ' + 
                   'Auroral HPI = {:.3f}').format(a[h+'_idif']['tot_numflux'], 
                                                  a[h+'_idif']['tot_aur_hpi']))

            # -----MONOENERGETIC PRECIP-----
            a[h+'_mono'] = {}
            # Number Flux
            loc_up = a[h+'_jr']>0 # Upward FAC signify downward electrons
            integrand = a[h+'_jr']*np.sin(colat)*dTheta*dPhi/1.6e-19
            a[h+'_mono']['tot_numflux'] = 1E-06*R**2 * np.sum(integrand[loc_up])
            # Energy Flux
            integrand = (a[h+'_mono_e-flux'] * np.sin(colat) * dTheta*dPhi)
            a[h+'_mono']['tot_aur_hpi'] = units_eflux*R**2 * np.sum(integrand)
        
            if debug:
                print((h+'-Mono:      ' +
                   'Total Number Flux = {:4.3E}   ' + 
                   'Auroral HPI = {:.3f}').format(a[h+'_mono']['tot_numflux'], 
                                                  a[h+'_mono']['tot_aur_hpi']))

            # -----BROADBAND PRECIP-----
            a[h+'_bbnd'] = {}
            # Number Flux
            integrand = (a[h+'_bbnd_n-flux'] * np.sin(colat) * 
                         dTheta*dPhi)
            a[h+'_bbnd']['tot_numflux'] = units_numflux*R**2 * np.sum(integrand)
            # Energy Flux
            integrand = (a[h+'_bbnd_e-flux'] * np.sin(colat) * dTheta*dPhi)
            a[h+'_bbnd']['tot_aur_hpi'] = units_eflux*R**2 * np.sum(integrand)
            
            if debug:
                print((h+'-Broadband: ' +
                   'Total Number Flux = {:4.3E}   ' + 
                   'Auroral HPI = {:.3f}').format(a[h+'_bbnd']['tot_numflux'], 
                                                  a[h+'_bbnd']['tot_aur_hpi']))

        return a