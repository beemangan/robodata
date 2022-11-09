import psycopg2 as sql
import pandas as pd
import pandas.io.sql as sqlio
import pandas.io.parquet as pario
import sys, os

conn = sql.connect("host=127.0.0.1 dbname=data user=robodata password=12345") # Connecting to localhost database created by scraper 
cur = conn.cursor()

seasons = "SELECT id, name FROM seasons"
teams = "SELECT * FROM teams"
events = "SELECT * FROM events"
rankings = "SELECT seasons.id, events.location->>'region' as region, sku, rank, number, wins, losses, ties, wp, ap, sp, high_score, average_points, total_points FROM rankings, teams, events, seasons WHERE rankings.team_id = teams.id AND event_id = events.id AND events.season = seasons.id ORDER BY id asc, sku asc"
skills = "SELECT * FROM skills"
matches = "SELECT events.season, events.location->>'region' as region, events.sku, matches.round,matches.id, red1, red2, red3, redscore, bluescore, blue3, blue2, blue1 FROM events, matches RIGHT JOIN (SELECT red.match_id,red1, red2, red3, redscore, bluescore, blue3, blue2, blue1 FROM red, blue WHERE red.match_id = blue.match_id) beans ON matches.id = beans.match_id WHERE matches.event_id = events.id ORDER BY id ASC"

data = sqlio.read_sql_query(rankings,conn)
data = data.convert_dtypes() # Force conversion of datatypes, mainly alliance_color

data.to_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\parquet\rankings.parquet',engine='pyarrow')