# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:06:28 2024

@author: 20195511
"""

import pandas as pd
import time
from nba_api.stats.endpoints import LeagueStandings
from nba_api.stats.endpoints import TeamGameLog
from nba_api.stats.endpoints import TeamYearByYearStats
import matplotlib.pyplot as plt
import numpy as np



#LUT

years = []

final_df = pd.DataFrame(columns = ['SeasonID','TeamID', 'TeamName', 'WinPCT', 'Record', 'Season'])

for i in range(53):
    if 71+i < 100:
        years.append(str(1970+i) + '-' + str(71+i))
    elif 71+i<110:
        years.append(str(1970+i) + '-0' + str(71+i-100))
    else:
        years.append(str(1970+i) + '-' + str(71+i-100))
    
for seasonVar in years:
    # print(season)
    data = LeagueStandings(league_id='00',season=seasonVar,season_type='Regular Season')
    time.sleep(2)
    df = data.get_data_frames()[0]
    
    df = df.loc[df['WinPCT'] >= 0.67]
    df['Season'] = seasonVar
    final_df = pd.concat([final_df,df],join='inner')
    
export_data = []

for index, row in final_df.iterrows():
    data = TeamGameLog(season=row['Season'], season_type_all_star='Regular Season', team_id=row['TeamID'])
    time.sleep(1)
    df = data.get_data_frames()[0]
    df = df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum())
    df= (df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum()).groupby('streak').filter(lambda g:(g['WL'].iloc[0] == 'L') & (len(g) > 1)).drop_duplicates('streak'))
    data2 = TeamYearByYearStats(team_id=row['TeamID'],league_id='00',per_mode_simple='PerGame',season_type_all_star='Regular Season')
    time.sleep(1)
    df2 = data2.get_data_frames()[0]
    myYear = row['Season']
    export_data.append({
         'Team':row['TeamName'],
         'Season':row['Season'],
         'Record':row['Record'],
         'Loss Streaks in season':len(df),
         'Finals Appereance': df2.query('YEAR==@myYear')['NBA_FINALS_APPEARANCE'].iloc[0]
         })
    
df_export_data = pd.DataFrame(export_data)
df_export_data.to_csv('../data/csv/lossStreaks.csv')