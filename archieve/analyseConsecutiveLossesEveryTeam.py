# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:02:50 2024

@author: 20195511
"""
import pandas as pd
import time
from nba_api.stats.endpoints import LeagueStandings
from nba_api.stats.endpoints import TeamGameLog
from nba_api.stats.endpoints import TeamYearByYearStats
import matplotlib.pyplot as plt
import numpy as np
import math


#LUT

years = []

yearsUntil73 = []

yearsUntil75 = []

yearsUntil77 = []

yearsUntil84 = []

yearsUntil03=[]

yearsAfter03 = []

teamAndYears_df = pd.DataFrame(columns = ['TeamID', 'TeamName', 'Season'])

for i in range(53):
    if 71+i < 100:
        years.append(str(1970+i) + '-' + str(71+i))
        if i < 2:
            yearsUntil73.append(str(1970+i) + '-' + str(71+i))
        elif i >= 2 and i < 4:
            yearsUntil75.append(str(1970+i) + '-' + str(71+i))
        elif i >= 4 and i < 6:
            yearsUntil77.append(str(1970+i) + '-' + str(71+i))
        elif i >= 6 and i < 13:
            yearsUntil84.append(str(1970+i) + '-' + str(71+i))           
        else:
            yearsUntil03.append(str(1970+i) + '-' + str(71+i))           
    elif 71+i<110:
        years.append(str(1970+i) + '-0' + str(71+i-100))
        if 71+i < 103:
            yearsUntil03.append(str(1970+i) + '-0' + str(71+i-100))           
        else:
            yearsAfter03.append(str(1970+i) + '-0' + str(71+i-100))
    else:
        years.append(str(1970+i) + '-' + str(71+i-100))
        yearsAfter03.append(str(1970+i) + '-' + str(71+i-100))
        

df_processing_av = pd.read_json('../data/json/Processed data no gamelogs.json')

export_data = []

for index, row in df_processing_av.iterrows():
    data = TeamGameLog(season=row['YEAR'], season_type_all_star='Regular Season', team_id=row['TEAM_ID'])
    time.sleep(1)

    df = data.get_data_frames()[0]
    df = df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum())
    df= (df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum()).groupby('streak').filter(lambda g:(g['WL'].iloc[0] == 'L') & (len(g) > 1)).drop_duplicates('streak'))
    
    export_data.append({
         'Team':row['TEAM_NAME'],
         'Season':row['YEAR'],
         'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
         'Loss Streaks in season':len(df),
         'Finals Stats':row['NBA_FINALS_APPEARANCE']
         })
    
df_export_data = pd.DataFrame(export_data)
df_export_data.to_csv('../data/csv/lossStreaksAllTime.csv')
    