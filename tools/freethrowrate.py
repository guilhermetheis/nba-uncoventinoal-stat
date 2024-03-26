# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:25:36 2024

@author: 20195511
"""


import pandas as pd
import time
from nba_api.stats.endpoints.leaguedashplayerstats import LeagueDashPlayerStats

years = []

for i in range(29,54):
    if 71+i<110:
        years.append(str(1970+i) + '-0' + str(71+i-100))
    else:
        years.append(str(1970+i) + '-' + str(71+i-100))

# Initialize an empty DataFrame
result_df = pd.DataFrame()
        
for seasons in years:
        
    res = LeagueDashPlayerStats(measure_type_detailed_defense='Scoring', season=seasons)
    data = res.get_data_frames()[0]
    df = data.copy()
    df = df.loc[(df['GP'] > 25)]
    df = df[['PLAYER_NAME', 'GP', 'PCT_PTS_FT']]
    df = df.sort_values(by=['PCT_PTS_FT'], ascending=False)
    # Get the top 10 rows
    df = df.head(10)
    df=df.reset_index()
    # Create a new column with the season name
    col_name = seasons.replace('-', '_')  # Convert season string to a valid column name
    result_df[col_name] = df['PLAYER_NAME'] + ' ' + df['PCT_PTS_FT'].astype(str)

result_df.to_csv('../data/csv/PointsPCTFT.csv')
result_df.to_csv('../data/csv/PointsPCTFT.csv')
