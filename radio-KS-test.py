#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:40:38 2017

@author: jiguangli
"""

from scipy.stats import ks_2samp
import pandas as pd

#read radio-loud and radio-quiet data, drop all the Nah values
quiet_all=pd.read_csv('radio_quiet_stats.csv')
loud_all=pd.read_csv('radio_loud_stats.csv')
df_quiet=quiet_all.dropna()
df_loud=loud_all.dropna()


var_indices=['Chi-square','WSTD','MAD','IQR','ROMS','NEV','P2PV',
                     'L1AC','CSSD','Excursion','VNR','S_B']

var_p_dict=dict()

for var_index in var_indices:

    quiet_stats=df_quiet[var_index].tolist()
    loud_stats= df_loud[var_index].tolist()
    result=ks_2samp(quiet_stats,loud_stats)
    var_p_dict[var_index]=result[1]

print(var_p_dict)
    