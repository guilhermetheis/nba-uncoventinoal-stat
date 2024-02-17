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
df_export_data.to_csv('lossStreaks.csv')
    
## Processing some data

plt.figure
bins = np.arange(0,10,1)
plt.hist(df_export_data.loc[(df_export_data['Finals Appereance'] == 'LEAGUE CHAMPION')]['Loss Streaks in season'], bins,edgecolor='black', align='left')
plt.title('NBA Champions and numbers of occurances of loss-streaks in the season')
plt.xlabel('Number of loss streaks during the season')
plt.xticks(bins)
plt.savefig('winners.png')
plt.show()


plt.figure
bins = np.arange(0,10,1)
plt.hist(df_export_data.loc[(df_export_data['Finals Appereance'] == 'FINALS APPEARANCE')]['Loss Streaks in season'], bins,edgecolor='black', align='left')
plt.title('NBA Runner-Ups and numbers of occurances of loss-streaks in the season')
plt.xlabel('Number of loss streaks during the season')
plt.xticks(bins)
plt.savefig('runnerUps.png')
plt.show()



plt.figure
bins = np.arange(0,11,1)
plt.hist(df_export_data.loc[(df_export_data['Finals Appereance'] == 'N/A')]['Loss Streaks in season'], bins,edgecolor='black', align='left')
plt.title('Phil Jackson non-finalists and numbers of occurances of loss-streaks in the season')
plt.xlabel('Number of occurances of loss-streaks during the season')
plt.xticks(bins)
plt.savefig('nonFinalists.png')
plt.show()

## Seeing if there is any trend yearly

fig, ax = plt.subplots(figsize=(15, 8))
#plt.xticks()
ax.plot(np.arange(0,42,1),df_export_data.loc[(df_export_data['Finals Appereance'] == 'LEAGUE CHAMPION')]['Loss Streaks in season'],linewidth=4)
ax.set_xticks(np.arange(0,42,1), labels=df_export_data.loc[(df_export_data['Finals Appereance'] == 'LEAGUE CHAMPION')]['Season'])
ax.tick_params(axis='x', rotation=90)
fig.suptitle('Yearly trends for champions', fontsize=16)
ax.set_xlabel('Seasons', fontsize=16)
ax.set_ylabel('Number of loss-streak occurances during the season', fontsize=13)
fig.savefig('championsTrends.png')
fig.show()

fig, ax = plt.subplots(figsize=(15, 8))
#plt.xticks()
ax.plot(np.arange(0,30,1),df_export_data.loc[(df_export_data['Finals Appereance'] == 'FINALS APPEARANCE')]['Loss Streaks in season'],linewidth=4)
ax.set_xticks(np.arange(0,30,1), labels=df_export_data.loc[(df_export_data['Finals Appereance'] == 'FINALS APPEARANCE')]['Season'])
ax.tick_params(axis='x', rotation=90)
fig.suptitle('Yearly trends for runner-ups', fontsize=16)
ax.set_xlabel('Seasons', fontsize=16)
ax.set_ylabel('Number of loss-streak occurances during the season', fontsize=13)
fig.savefig('runnerUPTrends.png')
fig.show()