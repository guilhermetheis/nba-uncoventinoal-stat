# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 10:23:36 2024

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

teamAndYears_df = pd.DataFrame(columns = ['TeamID', 'TeamName', 'Season'])

for i in range(53):
    if 71+i < 100:
        years.append(str(1970+i) + '-' + str(71+i))
    elif 71+i<110:
        years.append(str(1970+i) + '-0' + str(71+i-100))
    else:
        years.append(str(1970+i) + '-' + str(71+i-100))
    
    
for seasonVar in years: #getting all the data from all the teams in all the seasons
    # print(season)
    data = LeagueStandings(league_id='00',season=seasonVar,season_type='Regular Season')
    time.sleep(1)
    df = data.get_data_frames()[0]
    df['Season'] = seasonVar
    teamAndYears_df=pd.concat([teamAndYears_df,df],join='inner')
    
df_allTeams_data = pd.DataFrame(columns = ['TEAM_ID','TEAM_NAME', 'YEAR', 'WINS', 'LOSSES', 'NBA_FINALS_APPEARANCE'])


for index, row in teamAndYears_df.iterrows():
    data2 = TeamYearByYearStats(team_id=row['TeamID'],league_id='00',per_mode_simple='PerGame',season_type_all_star='Regular Season')
    time.sleep(1)
    df2 = data2.get_data_frames()[0]
    df2 = df2.loc[df2['NBA_FINALS_APPEARANCE'] == 'LEAGUE CHAMPION']
    df_allTeams_data = pd.concat([df_allTeams_data,df2],join='inner')


# Drop all the duplicates

df_processing = df_allTeams_data.copy()
df_processing = df_processing.drop_duplicates()
df_processing = df_processing.sort_values('YEAR')

#Get data based on available gamelog data

df_processing_av = df_processing.copy()
df_processing_av = df_processing_av[df_processing_av['YEAR'].isin(years)]

export_data = []

for index, row in df_processing_av.iterrows():
    data = TeamGameLog(season=row['YEAR'], season_type_all_star='Regular Season', team_id=row['TEAM_ID'])
    time.sleep(1)
    df = data.get_data_frames()[0]
    
    myList = []
    if len(df) < 59:
        df_my_count = df.copy()
        my_count = df_my_count.value_counts('WL')
        if my_count[0] >= math.floor(len(df)*0.67):
            myList.append(True)
        else:
            myList.append(False)
            
        if any(myList):
            export_data.append({
                 'Team':row['TEAM_NAME'],
                 'Season':row['YEAR'],
                 'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
                 'PJ Positive': True
                 })
        else:
            export_data.append({
                 'Team':row['TEAM_NAME'],
                 'Season':row['YEAR'],
                 'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
                 'PJ Positive': False
                 })
            
     
    else:

        for i in range(0, len(df)-59):
            df_my_count = df.iloc[0+i:59+i]
            my_count = df_my_count.value_counts('WL')
            if my_count[0] >= 40:
                myList.append(True)
            else:
                myList.append(False)
                
        if any(myList):
            export_data.append({
                 'Team':row['TEAM_NAME'],
                 'Season':row['YEAR'],
                 'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
                 'PJ Positive': True
                 })
        else:
            export_data.append({
                 'Team':row['TEAM_NAME'],
                 'Season':row['YEAR'],
                 'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
                 'PJ Positive': False
                 })
            
df_export_data = pd.DataFrame(export_data)
df_export_data.to_csv('PJ Teams.csv')

