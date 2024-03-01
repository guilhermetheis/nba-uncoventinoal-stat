# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:37:00 2024

@author: 20195511
"""

import nba_api
import pandas as pd

from nba_api.stats.endpoints import TeamGameLog

# LUT

teamsID = {'Atlanta Hawks': 1610612737,
 'Boston Celtics': 1610612738,
 'Cleveland Cavaliers': 1610612739,
 'New Orleans Pelicans': 1610612740,
 'Chicago Bulls': 1610612741,
 'Dallas Mavericks': 1610612742,
 'Denver Nuggets': 1610612743,
 'Golden State Warriors': 1610612744,
 'Houston Rockets': 1610612745,
 'Los Angeles Clippers': 1610612746,
 'Los Angeles Lakers': 1610612747,
 'Miami Heat': 1610612748,
 'Milwaukee Bucks': 1610612749,
 'Minnesota Timberwolves': 1610612750,
 'Brooklyn Nets': 1610612751,
 'New York Knicks': 1610612752,
 'Orlando Magic': 1610612753,
 'Indiana Pacers': 1610612754,
 'Philadelphia 76ers': 1610612755,
 'Phoenix Suns': 1610612756,
 'Portland Trail Blazers': 1610612757,
 'Sacramento Kings': 1610612758,
 'San Antonio Spurs': 1610612759,
 'Oklahoma City Thunder': 1610612760,
 'Toronto Raptors': 1610612761,
 'Utah Jazz': 1610612762,
 'Memphis Grizzlies': 1610612763,
 'Washington Wizards': 1610612764,
 'Detroit Pistons': 1610612765,
 'Charlotte Hornets': 1610612766}

seasonTypes = ['Pre Season', 'All Star', 'Regular Season', 'Playoffs']

seasonID = '2023-24' ## Current season

# Code
teamRecords_3PPCT = pd.DataFrame(columns=('Team', 'W-L Elite','W-L Very Good','W-L Above Average','W-L Below Average','W-L Bad','W-L Poor','W% Elite','W% Very Good','W% Above Average','W% Below Average','W% Bad', 'W% Poor'))

# for x in teamsID: ## X gives you name, teamsID[x] gives you the ID
#     print(teamsID[x])
for teamName in teamsID:
    
    data = TeamGameLog(season=seasonID, season_type_all_star='Regular Season', team_id=teamsID[teamName])
    df = data.get_data_frames()[0]
    
    df_el = df.copy()
    
    df_el = df_el.loc[df_el['FG3_PCT'] >= 0.42]
    df_el_W = df_el['WL'].str.contains('W').sum()
    df_el_L = df_el['WL'].str.contains('L').sum()
      
    df_vg = df.copy()
    df_vg = df_vg.loc[(df_vg['FG3_PCT'] < 0.42) & (df_vg['FG3_PCT'] >= 0.39)]
    df_vg_W = df_vg['WL'].str.contains('W').sum()
    df_vg_L = df_vg['WL'].str.contains('L').sum()
    
    df_aAVG = df.copy()
    df_aAVG = df_aAVG.loc[(df_aAVG['FG3_PCT'] < 0.39) & (df_aAVG['FG3_PCT'] >= 0.367)]
    df_aAVG_W = df_aAVG['WL'].str.contains('W').sum()
    df_aAVG_L = df_aAVG['WL'].str.contains('L').sum()
    
    df_bAVG = df.copy()
    df_bAVG = df_bAVG.loc[(df_bAVG['FG3_PCT'] < 0.367) & (df_bAVG['FG3_PCT'] >= 0.333)]
    df_bAVG_W = df_bAVG['WL'].str.contains('W').sum()
    df_bAVG_L = df_bAVG['WL'].str.contains('L').sum()
      
    df_bad = df.copy()
    df_bad = df_bad.loc[(df_bad['FG3_PCT'] < 0.333) & (df_bad['FG3_PCT'] >= 0.30)]
    df_bad_W = df_bad['WL'].str.contains('W').sum()
    df_bad_L = df_bad['WL'].str.contains('L').sum()
    
    
    df_below30 = df.copy()
    df_below30 = df_below30.loc[df_below30['FG3_PCT'] < 0.3]
    below30_W = df_below30['WL'].str.contains('W').sum()
    below30_L = df_below30['WL'].str.contains('L').sum()
    
    
    teamRecords_3PPCT = teamRecords_3PPCT.append({
        'Team': teamName,
        
        'W-L Elite': str(df_el_W) + '-' + str(df_el_L),
        
        'W-L Very Good': str(df_vg_W) + '-' + str(df_vg_L),
        
        'W-L Above Average': str(df_aAVG_W) + '-' + str(df_aAVG_L),
        
        'W-L Below Average': str(df_bAVG_W) + '-' + str(df_bAVG_L),
        
        'W-L Bad':str(df_bad_W) + '-' + str(df_bad_L),
        
        'W-L Poor':str(below30_W) + '-' + str(below30_L),
        
        'W% Elite': (df_el_W)/(df_el_W+df_el_L),
        
        'W% Very Good': (df_vg_W)/(df_vg_W+df_vg_L),
        
        'W% Above Average': (df_aAVG_W)/(df_aAVG_W+df_aAVG_L),
        
        'W% Below Average': (df_bAVG_W)/(df_bAVG_W+df_bAVG_L),
        
        'W% Bad': (df_bad_W)/(df_bad_W+df_bad_L),
        
        'W% Poor': (below30_W)/(below30_W+below30_L)
        
        }, ignore_index=True
        )
    
teamRecords_3PPCT.to_csv('../data/csv/allTeams3P.csv')
teamRecords_3PPCT.to_markdown('../data/allTeams3P.md', stralign='left',numalign='center', index=False, floatfmt='.3f')