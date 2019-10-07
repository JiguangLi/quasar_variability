#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 14:11:49 2017

@author: jiguangli
"""
from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.cosmology import FlatLambdaCDM


def compute_luminosity(sdss_name,sdss_magz_dict,cosmo):
    z=sdss_magz_dict[sdss_name][1]
    radio_l_watt=sdss_magz_dict[sdss_name][0]*(10**(-29))
    l_distance=cosmo.luminosity_distance(z)  
    l_distance_meters=l_distance.value*3.085677758*(10**22)
    l=4*np.pi*radio_l_watt*(l_distance_meters**2)
    return l

#Store SDSS names of two populations into two lists
loud_stats=pd.read_csv('better_rl_stats.csv')
#quiet_stats=pd.read_csv('normalized_large_quiet_stats.csv')
#upper_limit=np.percentile(quiet_stats['Chi-square'],90)
#quiet_stats=quiet_stats[quiet_stats['Chi-square']<upper_limit]

#==============================================================================
# loud_id=loud_stats['Unnamed: 0'].tolist()
# loud_id=[x[:-4] for x in loud_id]
# quiet_id=quiet_stats['Unnamed: 0'].tolist()
# quiet_id=[y[:-4] for y in quiet_id]
# 
# look_up=pd.read_csv('lightcurve_lookup.csv')
# #loud_table=look_up[look_up['id'].isin(loud_id)]
# #loud_sdss_names=loud_table['SDSS_NAME'].tolist()
# ids=look_up['id'].tolist()
# sdss_names=look_up['SDSS_NAME'].tolist()
# id_sdss_dict=dict(zip(ids,sdss_names))
# loud_sdss_names=[id_sdss_dict[int(hehe)] for hehe in loud_id]
# loud_stats['SDSS_NAME']=pd.Series(loud_sdss_names)
# quiet_sdss_names=[id_sdss_dict[int(hinhin)] for hinhin in quiet_id]
# quiet_stats['SDSS_NAME']=pd.Series(quiet_sdss_names)
# 
# quiet_table=look_up[look_up['id'].isin(quiet_id)]
# quiet_sdss_names=quiet_table['SDSS_NAME'].tolist()
# 
# 
# #build a dictionary:
# #key: SDSS_name   Values: (I magnitude,Z)
# input_file = fits.open('DR12Q(type1).fits')
# tbdata = input_file[1].data 
# mag_arrays=tbdata.field('FIRST_FLUX') 
# SDSS_names=tbdata.field('SDSS_NAME')
# red_shifts=tbdata.field('Z_VI')
# mag_z_tuple=zip(mag_arrays,red_shifts)
# sdss_magz_dict=dict(zip(SDSS_names,mag_z_tuple))
# 
# #compute luminosity
# cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
#==============================================================================
#==============================================================================
# quiet_l_values=[compute_luminosity(x,sdss_magz_dict,cosmo) 
# for x in quiet_sdss_names]
#==============================================================================
# #==============================================================================
# loud_l_values=[compute_luminosity(y,sdss_magz_dict,cosmo) 
# for y in loud_sdss_names]
# loud_stats['Luminosity']=pd.Series(loud_l_values)
# #quiet_z_values=np.array([sdss_magz_dict[zq][1] for zq in quiet_sdss_names ])
# loud_z_values=np.array([sdss_magz_dict[zl][1] for zl in loud_sdss_names ])
# loud_stats['Z']=pd.Series(loud_z_values)
#==============================================================================


#==============================================================================
# quiet_z_values=np.array([sdss_magz_dict[zl][1] for zl in quiet_sdss_names ])
# quiet_stats['Z']=pd.Series(quiet_z_values)
#==============================================================================
loud_z_values=loud_stats['Z'].tolist()
loud_l_values=loud_stats['Luminosity'].tolist()
#plot Z-l
fig=plt.figure()
plt.xlabel('Z')
plt.ylabel('Luminosity (W)')
#plt.scatter(quiet_z_values,quiet_l_values,s=50, c='blue',label='radio-quiet')
plt.scatter(loud_z_values,loud_l_values,s=21, c='red',marker='o',label='radio-loud')
#ax=fig.gca()
#ax.set_ylim(10**4, 10**8)
plt.yscale('log')
plt.legend()





