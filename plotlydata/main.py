import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# PLOTLY DOCUMENTATION IS AWFUL - USE API REFERENCE IF POSSIBLE AND NOTE DIFFERENCES BETWEEN PLOTLY EXPRESS AND PLOTLY GRAPH OBJECTS
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


sns = pd.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\seasons.parquet',engine='pyarrow')
data = pd.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\TurningPoint.parquet',engine='pyarrow')
data.dropna(0,subset=['red1','red2','region','blue1','blue2'],inplace=True)
data = data.sort_values('region')
fig = px.scatter(data, x="redscore", y="bluescore", marginal_x="violin", marginal_y="violin", color="region", title= "Turning Point", hover_data=['sku','red1','red2','blue1','blue2'],render_mode="webgl")
fig.write_html(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\webpage\TurningPoint.html',default_width='100%',default_height='100%')

#Plotly figures are represented of trees where the root node has 3 top layer attributes: data, layout, and frames.

SeasonGraphic = go.Figure([ScatterTrace,ViolinTrace])

# goals for main figure: 
# 1. Match score data by red and blue scores, colored by region 
# 2. Violin plots of red and blue scores by region (shows distribution of match scores for region comparison
# #. Hover data for each point - Team names, team scores, winner, event, region
# 4 On click for each data point pull up expanded data element for the match (team's W/L/R at the tournament, team's OPR for that event (EPR?), teams final rankings, other various stats

# "Zoom" levels - season, region, event
# Possible graphs for these ( average match score, average OPR/DPR/CCWM/whatever, top teams, (bottom teams?), highest avg event stats

