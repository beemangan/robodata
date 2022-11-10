import pandas as pd
import pandas.io.parquet as pq
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table, Input, Output

seasons = pd.io.parquet.read_parquet(r'/home/brendan/Documents/Programming/robodata/source/parquet/seasons.parquet',engine='pyarrow')
sdict = dict(zip(seasons.id,seasons.name)) ## Season Dictionary {id:name}

events = pd.io.parquet.read_parquet(r'/home/brendan/Documents/Programming/robodata/source/parquet/events.parquet',engine='pyarrow')
edict = dict(zip(events.sku,events.name)) ## Event Dictionary {sku:name}
max = {
    "173" : "250",
    "154" : "350",
    "139" : "75", # Look into this - need to deal with the LRT events (scoring changes?) there are several sets of scores 100+
    "130" : "140", #max 202
    "125" : "45", #max 45
    "119" : "170", # max 262
    "115" : "92", # max 92
    "110" : "500", # max 490
    "102" : "110",
    "92" : "110",   
} 
matches = pq.read_parquet(r'/home/brendan/Documents/Programming/robodata/source/parquet/vrc.parquet',engine='pyarrow')
stats = pq.read_parquet(r'/home/brendan/Documents/Programming/robodata/source/parquet/stats.parquet',engine='pyarrow')
matches = matches.sort_values('region')
matches = matches.sort_values('season',ascending=False)
matches.dropna(0,subset=['red1','red2','region','blue1','blue2'],inplace=True)

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.Div([
                dcc.Dropdown( # Season Dropdown
                    id="season-dropdown", placeholder="Select a Season",
                    value = 173, # default is spin up
                    options=[{"label": sdict[season], "value": int(season)} for season in matches.season.unique()])],
                style={'width': '60%', 'display': 'inline-block', 'margin':'auto', 'border' : '1px solid black'}),
        html.Div([        
                dcc.Dropdown( # Region Dropdown
                    id="region-dropdown",
                    placeholder="Select a Region")],
                style={'width': '40%', 'display': 'inline-block', 'margin':'auto', 'border' : '1px solid black'}),
        html.Div([
                dcc.Dropdown( # Event Dropdown
                    id="event-dropdown",
                    placeholder="Select an Event")],
                style={'width': '100%', 'display': 'inline-block', 'margin':'auto', 'border' : '1px solid black'}),
    ],style={'display':'flex','flex-direction':'row','width':'50%','margin-bottom':'10px','margin-above':'10px','align-items':'center','justify-content':'center'}),
        html.Div([
                dcc.Tabs(id="tabs", value='matches', children=[
                    dcc.Tab(label='Matches', value='matches'),
                    dcc.Tab(label='Statistics', value='stats'),]),
                html.Div(id='tabs-content')],
                style={'width': '50%', 'display': 'flex', 'justify-content':'center','align-items':'stretch','flex-direction':'column', 'border' : '2px solid black'}),
],style={'display':'flex','justify-content':'center','align-items':'center','flex-direction':'column'})

# Setting up callbacks to populate the dropdown options to be dependent on each other 
# I.e selecting a season populates region with all regions that have events for that season
# and selecting a region populates the event dropdown with all events for that region for that season
# Also set visibility of each dropdown (region becomes visible once season is selected etc)

@app.callback(
    Output('region-dropdown', 'options'),
    Input('season-dropdown', 'value')
)
def set_region_options(season): #Setting region dropdown options
        return [{"label": region, "value": region} for region in matches[matches.season == season].region.unique()]

@app.callback(
    Output('event-dropdown', 'options'),
    Input('region-dropdown', 'value'),
    Input('season-dropdown', 'value')
)
def set_event_options(region,season): #Setting event dropdown options
    return [{"label": edict[str(event)], "value": event} for event in matches[(matches.region == region) & (matches.season == season)].sku.unique()]

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input("season-dropdown", "value"),
    Input("region-dropdown", "value"),
    Input("event-dropdown", "value")
)
def render_content(tab,season,region,event):

    filtered_matches = matches[matches.season == season]
    fstats = stats[stats.season == str(season)]
    fstats = fstats.drop(columns=['season'])

    if region:
        filtered_matches = filtered_matches[filtered_matches.region == region]
        fstats = fstats[fstats.region == region]
        fstats = fstats.drop(columns=['region'])

    if event:
        filtered_matches = filtered_matches[filtered_matches.sku == event]
        fstats = fstats[fstats.sku == event]
        fstats = fstats.drop(columns=['sku'])

    fstats = fstats.sort_values('rank',ascending=True)
    c = dict(zip([str(i) for i in fstats.columns],["Team","Region","Event", "Rank","W","L","T","WP","AP","SP","OPR","DPR","High","Avg","Total"]))
    if tab == 'matches':
        return html.Div([
            dcc.Graph(
                figure = px.scatter(
                    filtered_matches,
                    x="redscore",
                    y="bluescore",
                    range_x=(-5,int(max[str(season)])),
                    range_y=(-5,int(max[str(season)])),
                    color="sku",
                    hover_data=["red1","red2","blue1","blue2"],
                    title="Match Scores",
                    render_mode="webgl",
                    width=850,
                    height=850).update_layout(
                        title={
                            'text': "Match Scores",
                            'y':.95,
                            'x':.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        font=dict(
                            family = "Courier New, monospace",
                            size = 15,
                            color = "black"),
                        showlegend=False,
                        xaxis={"title": ""},
                        yaxis={"title": ""})
            )
        ],style={'display':'flex','flex-direction':'row','width':'100%','margin-bottom':'5px','margin-above':'5px','align-items':'center','justify-content':'center'})
    elif tab == 'stats':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name":c[i], "id": i} for i in fstats.columns],
                data=fstats.to_dict('records'),
                sort_action='native',
                style_cell={'textAlign': 'left'},
                virtualization=True,
            )
        ])
if __name__ == '__main__':
    app.run_server(debug=True)


# goals for main figure: 
# 1. Match score data by red and blue scores, colored by region 
# 2. Violin plots of red and blue scores by region (shows distribution of match scores for region comparison
# #. Hover data for each point - Team names, team scores, winner, event, region
# 4 On click for each data point pull up expanded data element for the match (team's W/L/R at the tournament, team's OPR for that event (EPR?), teams final rankings, other various stats

# "Zoom" levels - season, region, event
# Possible graphs for these ( average match score, average OPR/DPR/CCWM/whatever, top teams, (bottom teams?), highest avg event stats

