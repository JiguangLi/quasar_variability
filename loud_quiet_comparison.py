#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:01:30 2017

@author: jiguangli
"""

import pandas as pd
import numpy
from matplotlib import pyplot


#read radio-loud and radio-quiet data, drop all the Nah values
quiet_all=pd.read_csv('radio_quiet_stats.csv')
loud_all=pd.read_csv('radio_loud_stats.csv')
df_quiet=quiet_all.dropna()
df_loud=loud_all.dropna()

#get the basic information of radio-loud and radio-quiet data, such as
#max and min.
quiet_summary=quiet_all.describe()
loud_summary=loud_all.describe()

#build a pandas series to iterate all the variability indices
var_indices=['Chi-square','WSTD','MAD','IQR','ROMS','NEV','P2PV',
                     'L1AC','CSSD','Excursion','VNR','S_B']


#Compare histograms
for var_index in range(12):
        quiet_stats=df_quiet[var_indices[var_index]].tolist()
        loud_stats=df_loud[var_indices[var_index]].tolist()
        
        
        #Determine the boundary to plot
        first_quartile=min(quiet_summary.at['25%',var_indices[var_index]],
                           loud_summary.at['25%',var_indices[var_index]])
        third_quartile=min(loud_summary.at['75%',var_indices[var_index]],
                           loud_summary.at['75%',var_indices[var_index]])
        max_value=max(quiet_summary.at['max',var_indices[var_index]],
                      loud_summary.at['max',var_indices[var_index]])
        min_value=min(quiet_summary.at['min',var_indices[var_index]],
                      loud_summary.at['min',var_indices[var_index]])
        IQR=third_quartile-first_quartile
        upper_bound=min(third_quartile+3*IQR,max_value)
        lower_bound=max(first_quartile-3*IQR,min_value)
        
        pyplot.figure(var_index)
        bins = numpy.linspace(lower_bound, upper_bound, 20)
        pyplot.hist(quiet_stats, bins, alpha=0.5, label='radio-quiet',normed=True)
        pyplot.hist(loud_stats, bins, alpha=0.5, label='radio-loud',normed=True)
        pyplot.legend(loc='upper right')
        pyplot.title(var_indices[var_index])
        pyplot.show()
        












