import pandas as pd
import pandas.io.parquet as pario
import numpy as np
import scipy as sp
import scipy.sparse as sps
import dictionaries as d
import sys
vrc = pario.read_parquet('/home/brendan/Documents/Programming/robodata/source/parquet/vrc.parquet',engine='pyarrow') # vrc.parquet is every season



vrc.dropna(0,subset=['id','red1','red2','region','blue1','blue2'],inplace=True) # Remove data with null regions or teams
event = vrc[vrc.sku == "RE-VRC-18-6700"]
data = event[['red1','red2','blue1','blue2','redscore','bluescore']]
team1 = pd.concat([data.red1,data.blue1],axis=0)
team1.sort_index(inplace=True)
team1.reset_index(drop=True,inplace=True)
team2 = pd.concat([data.red2,data.blue2],axis=0)
team2.sort_index(inplace=True)
team2.reset_index(drop=True,inplace=True)
teams = pd.DataFrame()
teams['team1'] = team1
teams['team2'] = team2
score = pd.concat([data.redscore,data.bluescore],axis=0)
score.sort_index(inplace=True)
score.reset_index(drop=True,inplace=True)
t1 = pd.get_dummies(teams.team1)
t2 = pd.get_dummies(teams.team2)
t1 = t1.add(t2,fill_value=0)
qr = sp.linalg.qr(t1,mode='economic')
print(qr)
calcOPR = sp.linalg.lstsq(sp.linalg.qr(t1),score.astype(int),lapack_driver='gelsy')
OPR = pd.DataFrame(calcOPR[0],index=t1.columns,columns=['OPR'])
OPR.sort_values('OPR',ascending=False,inplace=True)
print(OPR)