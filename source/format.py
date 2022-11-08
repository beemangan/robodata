import pandas as pd
import scipy as sp
import scipy.sparse as sps

vrc = pd.io.parquet.read_parquet('/home/brendan/Documents/Programming/robodata/source/parquet/vrc.parquet',engine='pyarrow') # vrc.parquet is every season
vrc.dropna(0,subset=['id','red1','red2','region','blue1','blue2'],inplace=True) # Remove data with null regions or teams

event = vrc[vrc['region'] == 'North Carolina'] # Filter to California
event = event[event['season'] == 110]
event = event[event['round'] == 2] # Filter to qualification matches only

data = event[['red1','red2','blue1','blue2','redscore','bluescore']]

team1 = pd.concat([data.red1,data.blue1],axis=0)
team1.sort_index(inplace=True)
team1.reset_index(drop=True,inplace=True)

team2 = pd.concat([data.red2,data.blue2],axis=0)
team2.sort_index(inplace=True)
team2.reset_index(drop=True,inplace=True)

score = pd.concat([data.redscore,data.bluescore],axis=0)
score.sort_index(inplace=True)
score.reset_index(drop=True,inplace=True)

teams = pd.get_dummies(team1).add(pd.get_dummies(team2),fill_value=0)


calcOPR = sp.linalg.lstsq(teams,score.astype(int),lapack_driver='gelsy')
OPR = pd.DataFrame(calcOPR[0],index=teams.columns,columns=['OPR'])
OPR.sort_values('OPR',ascending=False,inplace=True)
print(OPR)