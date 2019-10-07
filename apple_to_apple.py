#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 09:05:46 2017

@author: jiguangli
"""


from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.stats import ks_2samp
from scipy.stats import anderson_ksamp
import matplotlib.gridspec as gridspec

#return the qualified SDSS names in a list
#param: mag_ran, z_ran, represent the range of query
#mag_dict, z_dict: dictionaries 
def findSdssNames(mag_ran,z_ran,mag_dict,z_dict):
    mag_set=[mag_sdss for mag_sdss in mag_dict.keys() if
             mag_dict[mag_sdss]>mag_ran[0] and mag_dict[mag_sdss]<mag_ran[1]]
    z_set=[z_sdss for z_sdss in z_dict.keys() if
             z_dict[z_sdss]>z_ran[0] and z_dict[z_sdss]<z_ran[1]]
    return list(set(mag_set)&set(z_set))
 

#open variability indices stats for two populations
loud_stats=pd.read_csv('better_rl_stats.csv')
quiet_stats=pd.read_csv('better_rq_stats.csv')
upper_limit=np.percentile(quiet_stats['Chi-square'],90)
quiet_stats=quiet_stats[quiet_stats['Chi-square']<upper_limit]
    
#build: SDSS-Mag, SDSS-Z dictionary    
input_file = fits.open('DR12Q(type1).fits')
tbdata = input_file[1].data 
SDSS_names=tbdata.field('SDSS_NAME')
mag_info=tbdata.field('MI')
z_info=tbdata.field('Z_VI')
sdss_mag_dict=dict(zip(SDSS_names,mag_info))
sdss_z_dict=dict(zip(SDSS_names,z_info))

#return a list of qualified SDSS names
sdss_set=findSdssNames((-27,-25),(2.2,2.8),sdss_mag_dict,sdss_z_dict)


#find the subset of two dataframes for plotting
loud_stats=loud_stats[loud_stats['SDSS_NAME'].isin(sdss_set)]
quiet_stats=quiet_stats[quiet_stats['SDSS_NAME'].isin(sdss_set)]

#draw 1000 samples from each population
random.seed(1221)
draw_loud= random.sample(range(0,len(loud_stats)-1),1000)
draw_quiet= random.sample(range(0,len(quiet_stats)-1),1000)

#MI-Z distributions in the sample selected
#Gather MI-Z information
loud_sdss_set=loud_stats['SDSS_NAME'].tolist()
loud_sdss_chosen=[loud_sdss_set[i] for i in draw_loud]
loud_Mi_set=[sdss_mag_dict[j] for j in loud_sdss_chosen]
loud_z_set=[sdss_z_dict[k] for k in loud_sdss_chosen]

quiet_sdss_set=quiet_stats['SDSS_NAME'].tolist()
quiet_sdss_chosen=[quiet_sdss_set[l] for l in draw_quiet]
quiet_Mi_set=[sdss_mag_dict[m] for m in quiet_sdss_chosen]
quiet_z_set=[sdss_z_dict[n] for n in quiet_sdss_chosen]

all_Mi_set=loud_Mi_set+quiet_Mi_set
all_z_set=loud_z_set+quiet_z_set

#ready to make MI-Z plot
plt.figure()
gspec = gridspec.GridSpec(3, 3)
Mi_histogram = plt.subplot(gspec[0, 0:2])
Z_histogram = plt.subplot(gspec[1:, 2])
main_plot = plt.subplot(gspec[1:, 0:2])
legend_place=plt.subplot(gspec[0,2])

main_plot.scatter(loud_Mi_set,loud_z_set,c='blue',s=5,label='radio-loud')
main_plot.scatter(quiet_Mi_set,quiet_z_set,c='red',s=5,label='radio-quiet')
main_plot.set_xlabel('Absoulte magnitude')
main_plot.set_ylabel('Z')

h,l=main_plot.get_legend_handles_labels()
legend_place.legend(h,l)
legend_place.set_yticklabels([])
legend_place.set_xticklabels([])
legend_place.get_xaxis().set_visible(False)
legend_place.get_yaxis().set_visible(False)

Mi_histogram.hist(all_Mi_set,bins=10,normed=True)
Mi_histogram.set_xticklabels([])


Z_histogram.hist(all_z_set, bins=18, normed=True,orientation='horizontal')
Z_histogram.set_yticklabels([])

var_indices=['Chi-square','WSTD','MAD','IQR','ROMS','NEV','P2PV',
                     'L1AC','Excursion','VNR','S_B']

#plot distributions of variability indices
#==============================================================================
# for var_index in var_indices:
#     
#     #Convert the data to list
#     quiet_var=quiet_stats[var_index].tolist()
#     quiet_var=[quiet_var[i] for i in draw_quiet]    
#     loud_var=loud_stats[var_index].tolist()
#     loud_var=[loud_var[i] for i in draw_loud]  
#     
#     #Determine the boundary to plot
#     first_quartile=min(np.percentile(quiet_var,25),
#                            np.percentile(loud_var,25))
#     third_quartile=max(np.percentile(quiet_var,75),
#                            np.percentile(loud_var,75))
#     max_value=max(np.max(quiet_var),np.max(loud_var))
#     min_value=min(np.min(quiet_var),np.min(loud_var))
#     print('Max_value of {} : {}'.format(var_index,max_value))
#     print('Min_value of {} : {}'.format(var_index,min_value))
#     IQR=third_quartile-first_quartile
#     upper_bound=min(third_quartile+3*IQR,max_value)
#     lower_bound=max(first_quartile-3*IQR,min_value)
#         
#     pyplot.figure(var_index)
#     bins = np.linspace(lower_bound, upper_bound, 20)
#     pyplot.hist(quiet_var, bins, alpha=0.5, label='radio-quiet',normed=True)
#     pyplot.hist(loud_var, bins, alpha=0.5, label='radio-loud',normed=True)
#     pyplot.legend(loc='upper right')
#     pyplot.title('{}: 2.2<Z<2.8 & -27<MI<-25'.format(var_index))
#     pyplot.show()
#         
#==============================================================================

#==============================================================================
# 
# #KS test
# ks_p_dict=dict()
# for var_index in var_indices:
#     quiet_var=quiet_stats[var_index].tolist()
#     quiet_var=[quiet_var[i] for i in draw_quiet]    
#     loud_var=loud_stats[var_index].tolist()
#     loud_var=[loud_var[i] for i in draw_loud]  
#     result=ks_2samp(quiet_var,loud_var)
#     ks_p_dict[var_index]=result[1]
#     
# print(ks_p_dict)
# 
# #Anderson-Darling
# ad_p_dict=dict()
# for var_index in var_indices:
#     quiet_var=quiet_stats[var_index].tolist()
#     quiet_var=[quiet_var[i] for i in draw_quiet]    
#     loud_var=loud_stats[var_index].tolist()
#     loud_var=[loud_var[i] for i in draw_loud]  
#     result=anderson_ksamp([quiet_var,loud_var])
#     ad_p_dict[var_index]=result[2]
#     #print('{}:{}'.format(var_index,result))
# print(ad_p_dict)
# 
#==============================================================================






