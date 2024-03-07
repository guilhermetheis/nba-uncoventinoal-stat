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
    
for seasonVar in years: #getting all the data from all the teams in all the seasons
    # print(season)
    data = LeagueStandings(league_id='00',season=seasonVar,season_type='Regular Season')
    time.sleep(1)
    df = data.get_data_frames()[0]
    df['Season'] = seasonVar
    teamAndYears_df=pd.concat([teamAndYears_df,df],join='inner')
    
df_allTeams_data = pd.DataFrame(columns = ['TEAM_ID','TEAM_NAME', 'YEAR', 'WINS', 'LOSSES', 'CONF_RANK','PO_WINS','PO_LOSSES', 'NBA_FINALS_APPEARANCE'])


for index, row in teamAndYears_df.iterrows():
    data2 = TeamYearByYearStats(team_id=row['TeamID'],league_id='00',per_mode_simple='PerGame',season_type_all_star='Regular Season')
    time.sleep(1)
    df2 = data2.get_data_frames()[0]
    df_allTeams_data = pd.concat([df_allTeams_data,df2],join='inner')


# Drop all the duplicates

df_processing = df_allTeams_data.copy()
df_processing = df_processing.drop_duplicates()
df_processing = df_processing.sort_values('YEAR')

#Get data based on available gamelog data

df_processing_av = df_processing.copy()
df_processing_av = df_processing_av[df_processing_av['YEAR'].isin(years)]
df_processing_av.reset_index(drop=True, inplace=True)
df_processing_av.to_json('../data/Processed data no gamelogs.json')
