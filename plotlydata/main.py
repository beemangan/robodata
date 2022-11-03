import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# PLOTLY DOCUMENTATION IS AWFUL - USE API REFERENCE IF POSSIBLE AND NOTE DIFFERENCES BETWEEN PLOTLY EXPRESS AND PLOTLY GRAPH OBJECTS

sns = pd.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\seasons.parquet',engine='pyarrow')
data = pd.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\vrc.parquet',engine='pyarrow')
data.dropna(0,subset=['red1','red2','region','blue1','blue2'],inplace=True)
# dict = {}
# for i in data.season.unique().tolist():
#     dict[str(i)] = str(i)

# fig = px.scatter(data, x=data.redscore, y=data.bluescore,color=data.region, animation_frame=data.season, title="Match Data",hover_data=[data.red1,data.red2,data.blue1,data.blue2])

# fig["layout"].pop("updatemenus")

# fig.show()


seasons = sns.name.unique().tolist()
sid = sns.id.unique().tolist()

sd = dict(zip(seasons,sid))

# make list of continents
regions = []
for region in data.region:
    if region not in regions:
        regions.append(region)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["xaxis"] = {"autorange" : True , "title": "Red Alliance Score"}
fig_dict["layout"]["yaxis"] = {"autorange" : True , "title": "Blue Alliance Score"}
fig_dict["layout"]["hovermode"] = "closest"

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
season = 'VRC 2022-2023: Spin Up'
for region in regions:
    data_by_season = data[data.season == season]
    data_by_season_and_region = data_by_season[
        data_by_season.region == region]

    data_dict = {
        "x": data_by_season_and_region.redscore,
        "y": data_by_season_and_region.bluescore,
        "mode": "markers",
        "text": data_by_season_and_region.region,
        "marker": {
            "sizemode": "area",
            "sizeref": 200000,
            "size" : 6,
        },
        "name": region
    }
    fig_dict["data"].append(data_dict)

# make frames
for season in seasons:
    frame = {"data": [], "name": str(season)}
    for region in regions:
        data_by_season = data[data["season"] == sd[season]]
        data_by_season_and_region = data_by_season[
            data_by_season["region"] == region]

        data_dict = {
            "x": list(data_by_season_and_region["redscore"]),
            "y": list(data_by_season_and_region["bluescore"]),
            "mode": "markers",
            "text": list(data_by_season_and_region["region"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size" : 6
            },
            "name": region
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [season],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": season,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)
fig.update_layout(width=1300,height=1000)
fig.show()