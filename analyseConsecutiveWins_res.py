# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:06:28 2024

@author: 20195511
"""

#import nba_api
import pandas as pd
import time

from nba_api.stats.endpoints import LeagueStandings
from nba_api.stats.endpoints import TeamGameLog

#LUT

years = []

final_df = pd.DataFrame(columns = ['TeamID', 'TeamName', 'WinPCT', 'Record', 'Season'])

for i in range(54):
    if 71+i < 100:
        years.append(str(1970+i) + '-' + str(71+i))
    elif 71+i<110:
        years.append(str(1970+i) + '-0' + str(71+i-100))
    else:
        years.append(str(1970+i) + '-' + str(71+i-100))
    
for seasonVar in years:
#for i in range(1):
    # print(season)
    data = LeagueStandings(league_id='00',season=seasonVar,season_type='Regular Season')
    time.sleep(1)
    df = data.get_data_frames()[0]
    
    df = df.loc[df['WinPCT'] >= 0.73]
    df['Season'] = seasonVar
    final_df=pd.concat([final_df,df],join='inner')
    
final_consecutive = []
    
for index, row in final_df.iterrows():
     #print(row['Season'], row['TeamID'])
     data = TeamGameLog(season=row['Season'], season_type_all_star='Regular Season', team_id=row['TeamID'])
     df = data.get_data_frames()[0]
     count_df = df.copy()
     count_df = count_df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum())

     count_df = (count_df.assign(streak=(count_df['WL'] != count_df['WL'].shift()).cumsum()).groupby('streak').filter(lambda g:(g['WL'].iloc[0] == 'L') & (len(g) > 1)).drop_duplicates('streak'))
     final_consecutive.append({'Team':row['TeamName'],
          'Season':row['Season'],
          'Record': row['Record'],
          'Consecutive Ls': len(count_df)}) 
     
df_final_consecutive = pd.DataFrame(final_consecutive)
df_final_consecutive.to_csv('lossStreaks.csv')



         
    