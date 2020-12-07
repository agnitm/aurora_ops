#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 01:52:44 2020

@author: agnitm
"""

import numpy as np
import spacepy.pybats as pb
import spacepy.pybats.kyoto as kyoto
import matplotlib.pyplot as plt
import datetime as dt

time1 = dt.datetime(2010, 4, 4, 22, 0)
time2 = dt.datetime(2010, 4, 5, 10, 45)
dt = dt.timedelta(minutes=1)

kyoto_ae = kyoto.fetch('ae', time1, time2)

t = time1
aur_data = {}
aur_data['time'] = []
aur_data['AU'] = []
aur_data['AL'] = []

while(t <= time2):
    fname = ('AurIndex_superhi/MagGrid_superhires/mag_grid_e{:}{:0=2d}{:0=2d}' + 
             '-{:0=2d}{:0=2d}{:0=2d}.out').format(t.year, t.month, t.day, 
                                                  t.hour, t.minute, 
                                                  t.second)
    print(fname)
    if fname != 'AurIndex_superhi/MagGrid_superhires/mag_grid_e20100405-083000.out':                                            
        data = open(fname, 'r')
    
        for i in range(4):
            data.readline()
            # print(data.readline())
            
        net_data = data.readlines()
            
        dBn = np.zeros(len(net_data))
        for i in range(len(net_data)):
            line = net_data[i].split()
            dBn[i] = float(line[2])   
            
        print(np.max(dBn), np.min(dBn))
        aur_data['time'].append(t)
        aur_data['AU'].append(np.max(dBn))
        aur_data['AL'].append(np.min(dBn))
    t += dt

t = time1
aur_data1 = {}
aur_data1['time'] = []
aur_data1['AU'] = []
aur_data1['AL'] = []

while(t <= time2):
    fname = ('AurIndex_lores/mag_grid_e{:}{:0=2d}{:0=2d}' + 
              '-{:0=2d}{:0=2d}{:0=2d}.out').format(t.year, t.month, t.day, 
                                                  t.hour, t.minute, 
                                                  t.second)
    data = open(fname, 'r')
    
    for i in range(4):
        data.readline()
        # print(data.readline())
        
    net_data = data.readlines()
            
    dBn = np.zeros(len(net_data))
    for i in range(len(net_data)):
        line = net_data[i].split()
        dBn[i] = float(line[2])   
        
    # print(np.max(dBn), np.min(dBn))
    aur_data1['time'].append(t)
    aur_data1['AU'].append(np.max(dBn))
    aur_data1['AL'].append(np.min(dBn))
    t += dt
    
t = time1
aur_data2 = {}
aur_data2['time'] = []
aur_data2['AU'] = []
aur_data2['AL'] = []

while(t <= time2):
    fname = ('AurIndex_hires/mag_grid_e{:}{:0=2d}{:0=2d}' + 
              '-{:0=2d}{:0=2d}{:0=2d}.out').format(t.year, t.month, t.day, 
                                                  t.hour, t.minute, 
                                                  t.second)
    data = open(fname, 'r')
    
    for i in range(4):
        data.readline()
        # print(data.readline())
        
    net_data = data.readlines()
            
    dBn = np.zeros(len(net_data))
    for i in range(len(net_data)):
        line = net_data[i].split()
        dBn[i] = float(line[2])   
        
    # print(np.max(dBn), np.min(dBn))
    aur_data2['time'].append(t)
    aur_data2['AU'].append(np.max(dBn))
    aur_data2['AL'].append(np.min(dBn))
    t += dt

#=============================================================================
plt.figure(figsize=(12,3))
plt.plot(kyoto_ae['time'], kyoto_ae['al'], 'k', alpha = 0.35, lw=5, 
         label = 'Kyoto')    
plt.plot(aur_data1['time'], aur_data1['AL'], 'orangered', label = 'MAGNIT 1/4 $R_E$', 
         lw=2.5)
plt.plot(aur_data2['time'], aur_data2['AL'], 'magenta', label = 'MAGNIT 1/8 $R_E$', 
          lw=2.5)
plt.plot(aur_data['time'], aur_data['AL'], 'r', label = 'MAGNIT 1/16 $R_E$', 
         lw=2.5)

rlm_values = pb.LogFile('geoindex_e20100404-190000_RLMhires.log', 
                           starttime=time1)
plt.plot(rlm_values['time'], rlm_values['AL'], '--b', label = 'RLM')

plt.xlim(kyoto_ae['time'][0], kyoto_ae['time'][-1])
plt.ylabel('AL')
plt.legend(ncol=2)
plt.savefig('AL_all.png', dpi=200)
plt.show(); plt.close()

#=============================================================================
plt.figure(figsize=(12,3))
plt.plot(kyoto_ae['time'], kyoto_ae['au'], 'k', alpha = 0.35, lw=5,
         label = 'Kyoto')    
plt.plot(aur_data1['time'], aur_data1['AU'], 'orangered', label = 'MAGNIT 1/4 $R_E$', 
         lw=2.5)
plt.plot(aur_data2['time'], aur_data2['AU'], 'magenta', label = 'MAGNIT 1/8 $R_E$', 
         lw=2.5)
plt.plot(aur_data['time'], aur_data['AU'], 'r', label = 'MAGNIT 1/16 $R_E$',
         lw=2.5)
plt.plot(rlm_values['time'], rlm_values['AU'], '--b', label = 'RLM')

plt.xlim(kyoto_ae['time'][0], kyoto_ae['time'][-1])
plt.ylabel('AU')
plt.legend(ncol=2)
plt.savefig('AU_all.png', dpi=200)
plt.show(); plt.close()

#=============================================================================
plt.figure(figsize=(12,3))
plt.plot(kyoto_ae['time'], kyoto_ae['ae'], 'k', alpha = 0.35, lw = 5,
         label = 'Kyoto')  
plt.plot(aur_data1['time'], aur_data1['AU'] + np.abs(aur_data1['AL']), 
         'orangered', label = 'MAGNIT 1/4 $R_E$', lw=2.5)  
plt.plot(aur_data2['time'], aur_data2['AU'] + np.abs(aur_data2['AL']), 
         'magenta', label = 'MAGNIT 1/8 $R_E$', lw=2.5)
plt.plot(aur_data['time'], aur_data['AU'] + np.abs(aur_data['AL']), 
         'r', label = 'MAGNIT 1/16 $R_E$', lw=2.5)
plt.plot(rlm_values['time'], rlm_values['AE'], '--b', label = 'RLM')

plt.xlim(kyoto_ae['time'][0], kyoto_ae['time'][-1])
plt.ylabel('AE')
plt.legend(ncol=2)
plt.savefig('AE_all.png', dpi=200)
plt.show(); plt.close()

# #=============================================================================
# plt.figure(figsize=(8,4))
# plt.plot(kyoto_ae['time'], kyoto_ae['ao'], 'k', alpha = 0.35, lw = 5,
#          label = 'Kyoto')  
# plt.plot(aur_data1['time'], (aur_data1['AU'] + aur_data1['AL'])*0.5, 
#          'orangered', label = 'MAGNIT 1/4 $R_E$', lw=3.5)  
# plt.plot(aur_data2['time'], (aur_data2['AU'] + aur_data2['AL'])*0.5, 
#          'magenta', label = 'MAGNIT 1/8 $R_E$', lw=3.5)
# plt.plot(aur_data['time'], (aur_data['AU'] + aur_data['AL'])*0.5, 
#          'r', label = 'MAGNIT 1/16 $R_E$', lw=3.5)
# plt.plot(rlm_values['time'], rlm_values['AO'], '--b', label = 'RLM')

# plt.xlim(kyoto_ae['time'][0], kyoto_ae['time'][-1])
# plt.ylabel('AO')
# plt.legend(ncol=2)
# plt.show(); plt.close()