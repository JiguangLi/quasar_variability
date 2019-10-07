#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 10:10:37 2017

@author: jiguangli
"""
import pandas as pd
from astropy.io import fits

#build the two CSV files for radio_loud and radio_quiet
def build_two_csv(input_dict,df_all,lookup_dict):
    
    df_quiet=pd.DataFrame(columns=df_all.columns)
    df_loud=pd.DataFrame(columns=df_all.columns)
    count_quiet=0
    count_loud=0
    patience=0
    
    for k,v in input_dict.items():   
        print(patience)
        patience+=1
        if_loud=v
        if(if_loud==-1):
            continue 
        elif(k in lookup_dict.keys()):
            id_name=lookup_dict[k]
            file_name=str(id_name)+'.dat'
            if(file_name in df_all.index):
                series_to_append=df_all.loc[file_name]
                if(if_loud==0):
                    df_quiet.loc[count_quiet]=series_to_append
                    count_quiet+=1
                elif(if_loud==1):
                    df_loud.loc[count_loud]=series_to_append
                    count_loud+=1
                  
    df_quiet.to_csv('radio_quiet_stats',sep=',')
    df_loud.to_csv('radio_loud_stats',sep=',')
                    
                
                

#convert the original type 1 quasar file into a dictionary
#Key: SDSS_NAME   Values: 0(no-radio),1(radio-loud),-1(uncertain)
input_file = fits.open('DR12Q(type1).fits')
tbdata = input_file[1].data 
all_name=tbdata.field('SDSS_NAME') #The array of SDSS name
if_loud=tbdata.field('FIRST_MATCHED')#The array of First-matched
name_loud_dict=dict(zip(all_name,if_loud))


#Obtain the dataframe from whose series will be appended to radio_loud
#and radio_quiet dataframes
df_all = pd.read_csv('type1_all_stats.csv')
df_all= df_all.set_index('file_name')


#covert the lookup table to a dictionary
#key: SDSS_NAME   Value: id
df_lookup=pd.read_csv('radio_match.csv')
df_lookup=df_lookup.set_index('SDSS_NAME')
SDSS_list=df_lookup.index.tolist()
id_list=df_lookup['id'].tolist()
lookup_dict=dict(zip(SDSS_list,id_list))


#input parameter types: dict, dataframe, dict
build_two_csv(name_loud_dict,df_all,lookup_dict)








