import numpy as np
import varfeat
import os
import pandas as pd

directory= os.fsencode('/Users/jiguangli/quasar_stats/lcs')
count=0
indices=['file_name','Chi-square','WSTD','MAD','IQR','ROMS',
                 'NEV','P2PV','L1AC','CSSD','Excursion','VNR','S_B']
df=pd.DataFrame(columns=indices)

for file in os.listdir(directory):
       file_name=str(file)[2:-1]
       path='/Users/jiguangli/quasar_stats/lcs/'+file_name
       arr=np.loadtxt(path)
       #print('Input array is :')
       #print(arr)
            
       #Compute chi-square
       chi=varfeat.chisq(arr)
       #print('Chi-square:',chi)
            
       #Compute weighted standard deviation
       wstd=varfeat.wstd(arr)
       #print('WSTD:',wstd)
            
       #Compute Median absolute deviation
       mad=varfeat.mad(arr)
       #print('MAD:',mad)
            
       #Compute Interquatile range
       ir=varfeat.iqr(arr)
       #print('IQR:',ir)
            
       #Compute Robust median statistic
       rm=varfeat.roms(arr)
       #print('ROMS:',rm)
            
       #Compute Normalized excess variance
       nev=varfeat.nev(arr)
       #print('NEV:',nev)
            
       #Compute Peak-to-peak variability
       p2p=varfeat.p2pvar(arr)
       #print('P2PV:',p2p)
            
       #Compute Lag-1 autocorrelation
       lag1=varfeat.chisq(arr)
       #print('L1AC:',lag1)
            
       #Compute Consecutive same-sign deviations from the mean magnitude
       cssd=varfeat.cssd(arr)
       #print('CSSD:',cssd)
            
       #Compute Excursions
       e=varfeat.ex(arr)
       #print('Excursions:',e)
            
            
       #Compute Von Neumann ratio
       von=varfeat.neumann(arr)
       #print('VNR:',von)
            
       #Compute S_B variability statistics
       sb= varfeat.sb(arr)
       #print('SB:',sb)
            
       results=[file_name,chi,wstd,mad,ir,rm,nev,p2p,lag1,cssd,e
                     ,von,sb]
            
       temp=pd.Series(results)
       df.loc[count]=results
       count=count+1
       print(count)
          
  

df.to_csv('temp',sep=',')
    
    
    

