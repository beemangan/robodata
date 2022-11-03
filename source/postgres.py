import psycopg2 as sql
import pandas as pd
import pandas.io.sql as sqlio
import pandas.io.parquet as pario
import sys, os

conn = sql.connect("host=127.0.0.1 dbname=data user=robodata password=12345") # Connecting to localhost database created by scraper 
cur = conn.cursor()

#"SELECT id, name FROM seasons"
#"SELECT events.season, events.location->>'region' as region, events.sku, matches.round,matches.id, red1, red2, red3, redscore, bluescore, blue3, blue2, blue1 FROM events, matches RIGHT JOIN (SELECT red.match_id,red1, red2, red3, redscore, bluescore, blue3, blue2, blue1 FROM red, blue WHERE red.match_id = blue.match_id) beans ON matches.id = beans.match_id WHERE matches.event_id = events.id ORDER BY id ASC"

data = sqlio.read_sql_query(sys.argv[1],conn)
data = data.convert_dtypes() # Force conversion of datatypes, mainly alliance_color

data.to_parquet(r'C:\Users\Brendan\Documents\Programming\Python Testing\robodata\source\output.parquet',engine='pyarrow')

os.rename('output.parquet',str(sys.argv[2]))
