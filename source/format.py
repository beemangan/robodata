import pandas as pd
import pandas.io.parquet as pario
import sys, os
import time
import plotly.express as px

data = pario.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\vrc.parquet',engine='pyarrow')

sns = pario.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\seasons.parquet',engine='pyarrow')

dict = {
    '173': 'SpinUp',
    '154' : 'TippingPoint',
    '139' : 'ChangeUp',
    '130' : 'TowerTakeover',
    '125' : 'TurningPoint',
    '119' : 'InTheZone',
    '115' : 'Starstruck',
    '110' : 'NothingButNet', 
    '102' : 'Skyrise',
    '92' : 'TossUp',
    '85' : 'SackAttack', 
    '73' : 'Gateway', 
    '7' : 'RoundUp', 
    '1' : 'CleanSweep'
    }
dict2 = {
    '173': 'Spin Up',
    '154' : 'Tipping Point',
    '139' : 'Change Up',
    '130' : 'Tower Takeover',
    '125' : 'Turning Point',
    '119' : 'In The Zone',
    '115' : 'Starstruck',
    '110' : 'Nothing But Net', 
    '102' : 'Skyrise',
    '92' : 'Toss Up',
    '85' : 'Sack Attack', 
    '73' : 'Gateway', 
    '7' : 'Round Up', 
    '1' : 'Clean Sweep'
    }
seasons = data.season.unique().tolist()
for season in seasons:
    season_data = data[data.season == season]
    print(season_data)
    # season_data.dropna(0,subset=['red1','red2','region','blue1','blue2'],inplace=True)
    # season_data = data.sort_values('region')
    # fig = px.scatter(season_data, x="redscore", y="bluescore", color="region", title= dict2[str(season)], hover_data=['red1','red2','blue1','blue2'],render_mode='webgl')

    # fig.write_html(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\webpage\output.html',default_width='100%',default_height='100%')
    # time.sleep(4)
    # os.rename(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\webpage\output.html',dict[str(season)]+'.html')