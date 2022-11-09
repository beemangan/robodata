import pandas as pd
import pandas.io.parquet as pq
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table

seasons = pd.io.parquet.read_parquet(r'/home/brendan/Documents/Programming/robodata/source/parquet/seasons.parquet',engine='pyarrow')
sdict = dict(zip(seasons.id,seasons.name)) ## Season Dictionary {id:name}

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
    html.H1("VRC Match Data"),
    html.Div([
                dcc.Dropdown(
                    id="season-dropdown", placeholder="Select a Season",
                    value = 173, # default is spin up
                    options=[{"label": sdict[season], "value": int(season)} for season in matches.season.unique()]),
                
                dcc.Dropdown(
                    id="region-dropdown",
                    placeholder="Select a Region",
                    options=[{"label": region, "value": region} for region in matches.region.unique()]),

                ],
            style={"width": "15%", "display": "inline-block"},
        ),
    dcc.Tabs(id="tabs", value='matches', children=[
        dcc.Tab(label='Matches', value='matches'),
        dcc.Tab(label='Statistics', value='stats'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    dash.Output('tabs-content', 'children'),
    dash.Input('tabs', 'value'),
    dash.Input("season-dropdown", "value"),
    dash.Input("region-dropdown", "value"),
)
def render_content(tab,s,region):
    filtered_matches = matches[matches.season == s]
    filtered_stats = stats[stats.season == str(s)]
    if region:
        filtered_matches = filtered_matches[filtered_matches.region == region]
        filtered_stats = filtered_stats[filtered_stats.region == region]
    filtered_stats.sort_values('opr',inplace=True,ascending=False)
    if tab == 'matches':
        return html.Div([
            dcc.Graph(
                figure = px.scatter(
                    filtered_matches,
                    x="redscore",
                    y="bluescore",
                    color="sku",
                    hover_data=["red1","red2","blue1","blue2"],
                    title="Match Scores",
                    render_mode="webgl",
                    width=900,
                    height=898).update_layout(showlegend=False)
            )
        ])
    elif tab == 'stats':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in filtered_stats.columns],
                data=filtered_stats.to_dict('records'),
                style_cell={'textAlign': 'left'},
            )
        ])





# app.layout = html.Div(
#     [   
#         html.H1("VRC Match Data"),
#         # Dropdown to filter season
#         html.Div(
#             [
#                 dcc.Dropdown(
#                     id="season-dropdown",
#                     placeholder="Select a Season",
#                     value = 173, # default is spin up
#                     options=[{"label": sdict[season], "value": season} for season in matches.season.unique()], # Create available options from the dataset
#                 ),
#             ],
#             style={"width": "15%", "display": "inline-block"},
#         ),
#         html.Div(
#             [
#                 dcc.Dropdown(
#                     id="region-dropdown",
#                     placeholder="Select a Region",
#                     value = 'All', # default is spin up
#                     options=[{"label": region, "value": region} for region in matches.region.unique()], # Create available options from the dataset
#                 ),
#             ],
#             style={"width": "15%", "display": "inline-block"},
#         ),
#         html.Div(
#             [
#                 dcc.Tabs(
#                     id="tabs",
#                     value="match-scores",
#                     children=[
#                         dcc.Tab(label='Match Scores', value="match-scores",children=[dcc.Graph(id='match-scores',className ="chart")]),
#                         dcc.Tab(label='Statistics', value='stats',children=[dcc.Graph(id='stats')]),
#                     ]
#                 ),
#             ],
#             style={"width": "15%", "display": "inline-block"},
#         ),
#         html.Div(id="tab-content"),
        
#     ]
# )

# @app.callback(
#     dash.Output("match-scores", "figure"),
#     dash.Input("season-dropdown", "value"),
#     dash.Input("region-dropdown", "value"),
# )
# def update_figure(selected_season,selected_region):
#     filtered_matches = matches[matches.season == selected_season]
#     if selected_region:
#         filtered_matches = filtered_matches[filtered_matches.region == selected_region]
#     fig = px.scatter(
#         filtered_matches, 
#         x="redscore",
#         y="bluescore",
#         labels={"region": "Region"},
#         hover_data=["red1","red2","blue1","blue2",'sku'],
#         range_x=[-5,int(max[str(selected_season)])],
#         range_y=[-5,int(max[str(selected_season)])],
#         height=800,
#         width=898,
#         render_mode="webgl")
#     return fig

# @app.callback(
#     dash.Output('tab-content', 'children'),
#     dash.Input('tabs', 'value'))
# def render_content(tab):
#     if tab == 'match-scores':
#         return html.Div([
#             dcc.Graph(
#                 id='match-scores'
#             )
#         ])
#     elif tab == 'stats':
#         return html.Div([
#             dcc.Graph(
#                 id='stats',
#                 figure = go.Figure(
#                     header = dict(
#                         values = stats.columns,
#                         align = "left"
#                     ),
#                     cells = dict(
#                         values = stats.values,
#                         align = "left"
#                     )
#                 )

#             )
#         ])


if __name__ == '__main__':
    app.run_server(debug=True)


# goals for main figure: 
# 1. Match score data by red and blue scores, colored by region 
# 2. Violin plots of red and blue scores by region (shows distribution of match scores for region comparison
# #. Hover data for each point - Team names, team scores, winner, event, region
# 4 On click for each data point pull up expanded data element for the match (team's W/L/R at the tournament, team's OPR for that event (EPR?), teams final rankings, other various stats

# "Zoom" levels - season, region, event
# Possible graphs for these ( average match score, average OPR/DPR/CCWM/whatever, top teams, (bottom teams?), highest avg event stats

