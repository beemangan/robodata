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


# Plotly graph object implementation attempts will be documented below this.
ScatterTrace = go.Scatter()
ViolinTrace = go.Violin()
#Plotly figures are represented of trees where the root node has 3 top layer attributes: data, layout, and frames.

SeasonGraphic = go.Figure([ScatterTrace,ViolinTrace])