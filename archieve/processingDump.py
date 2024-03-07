# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:00:29 2024

@author: 20195511
"""

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