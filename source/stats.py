import pandas as pd
import numpy as np
import calculations as calc
import traceback
# This file will be used for testing and for the creation of the stats dataframe.

rankings = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\rankings.parquet',engine='pyarrow')
vrc = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\vrc.parquet',engine='pyarrow')

stats = pd.DataFrame(columns=['team','season','region','sku','rank','wins','losses','ties','wp','ap','sp','opr','dpr','highscore','avgscore','totalpts'])
errors = pd.DataFrame(columns=['team','sku','error','traceback'])
eventcount = 0
errorcount = 0
for sku in vrc['sku'].unique(): # For every event,
    eventcount += 1
    season = vrc[vrc['sku'] == sku]['season'].unique()[0] # Get the season
    region = vrc[vrc['sku'] == sku]['region'].unique()[0] # Get the region
    eventmatches = vrc[vrc['sku'] == sku] # Get all matches for that event
    eventrankings = rankings[rankings['sku'] == sku] # Get all rankings for that event
    opr = calc.OPR(eventmatches) # Get OPR dictionary for that event
    dpr = calc.DPR(eventmatches) # Get DPR dictionary for that event
    for team in eventrankings['number'].unique(): # For every team in that event,
        rank = eventrankings[eventrankings['number'] == team] # Get the team's ranking
        try:
            stats.loc[len(stats.index)] = [ # Attempt to insert a new row
                str(team),
                str(season),
                str(region),
                str(sku),
                int(rank['rank']),
                int(rank['wins']),
                int(rank['losses']),
                int(rank['ties']),
                float(rank['wp']),
                float(rank['ap']),
                float(rank['sp']),
                float(opr.at[str(team),'OPR']),
                float(dpr.at[str(team),'DPR']),
                int(rank['high_score']),
                int(rank['average_points']),
                int(rank['total_points'])]
        except Exception as e:
            errors.loc[len(errors.index)] = [str(team),str(sku),str(e),str(traceback.format_exc())] # Error handling
            errorcount += 1
            continue
    print(f'Event {eventcount} of {len(vrc["sku"].unique())} complete. {errorcount} errors logged so far.')


            
print(stats)
stats.to_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\stats.parquet',engine='pyarrow')
print(errors)
errors.to_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\errors.parquet',engine='pyarrow')