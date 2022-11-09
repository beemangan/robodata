import pandas as pd

seasons = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\seasons.parquet',engine='pyarrow')
sdict = dict(zip(seasons.id,seasons.name)) ## Season Dictionary {id:name}

teams = pd.io.parquet.read_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\teams.parquet',engine='pyarrow')
tdict = dict(zip(teams.id,teams.number)) ## Team Dictionary {id:number}