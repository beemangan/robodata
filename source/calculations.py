import pandas as pd
import scipy as sp
import scipy.sparse as sps


def OPR(data): # Returns an OPR dataframe for any given season, region, or event match dataframe

    data = data[data['round'] == 2] # Qualifcation matches only

    team1 = pd.concat([data.red1,data.blue1],axis=0).sort_index().reset_index(drop=True) # Single column of red1 and blue1 teams sorted by the dropped match index
    team2 = pd.concat([data.red2,data.blue2],axis=0).sort_index().reset_index(drop=True) # same as above for red2 and blue2...
    score = pd.concat([data.redscore,data.bluescore],axis=0).sort_index().reset_index(drop=True) # ...and for redscore and bluescore

    # with OPR you are solving red1 + red2 = redscore and blue1 + blue2 = bluescore
    # OPR measures how much a team contributes to their alliance's score (calculated contribution) and is a measure of offensive power

    teams = pd.get_dummies(team1).add(pd.get_dummies(team2),fill_value=0) # Sparse matrix with rows as matches and columns as teams (should be two 1s per row)

    calcOPR = sp.linalg.lstsq(teams,score.astype(int)) # Least squares regression to find OPR
    OPR = pd.DataFrame(calcOPR[0],index=teams.columns,columns=['OPR']).sort_values('OPR',ascending=False).round(decimals=2) # Convert to dataframe and sort by OPR
    return OPR # If you need a dictionary call OPR(data).to_dict(). Call values from dataframe with OPR(data).at['team#','OPR']

def DPR(data): # Returns a DPR dataframe for any given season, region, or event match dataframe

    data = data[data['round'] == 2] # Qualifcation matches only

    team1 = pd.concat([data.red1,data.blue1],axis=0).sort_index().reset_index(drop=True) # Single column of red1 and blue1 teams sorted by the dropped match index
    team2 = pd.concat([data.red2,data.blue2],axis=0).sort_index().reset_index(drop=True) # same as above for red2 and blue2...
    score = pd.concat([data.bluescore,data.redscore],axis=0).sort_index().reset_index(drop=True) # ... switch order of the alliance scores

    # with DPR you are solving red1 + red2 = bluescore and blue1 + blue2 = redscore
    # DPR measures how much a team detracts from the score of the opposing alliance and is a measure of defensive power

    teams = pd.get_dummies(team1).add(pd.get_dummies(team2),fill_value=0) # Sparse matrix with rows as matches and columns as teams (should be two 1s per row)

    calcDPR = sp.linalg.lstsq(teams,score.astype(int)) # Least squares regression to find DPR
    DPR = pd.DataFrame(calcDPR[0],index=teams.columns,columns=['DPR']).sort_values('DPR',ascending=False).round(decimals=2) # Convert to dataframe and sort by DPR
    return DPR # If you need a dictionary call DPR(data).to_dict(). Call values from dataframe with DPR(data).at['team#','DPR']


# test = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\vrc.parquet',engine='pyarrow') # vrc.parquet is every season
# test.dropna(0,subset=['id','red1','red2','region','blue1','blue2'],inplace=True) # Remove data with null regions or teams
# data = test[(test['region'] == 'North Carolina') & (test['season'] == 125)] # Filter to a specific event
# for e in data['sku'].unique():
#     try:
#         print(OPR(data[data['sku'] == e])) #
#     except KeyError:
#         pass
# print(OPR(data))

stats = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\stats.parquet',engine='pyarrow') # vrc.parquet is every season

print(stats[stats['team'] == '5139C']) # grab specific team # - seems like worlds data is wrong