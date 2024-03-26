# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:49:40 2024

@author: 20195511
"""

import pandas as pd
import time
from nba_api.stats.endpoints import TeamGameLog
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
    myList = []
    data = TeamGameLog(season=row['YEAR'], season_type_all_star='Regular Season', team_id=row['TEAM_ID'])
    time.sleep(1)
    df = data.get_data_frames()[0]
    
    if row['YEAR'] in yearsUntil73:
        if row['PO_WINS'] < 4 and row['PO_LOSSES'] > 0:
            PO_elim = 'CSF Exit'
        elif row['PO_WINS'] < 8 and row['PO_WINS'] >= 4:
            PO_elim = 'CF Exit'
        elif row['PO_WINS'] < 12 and row['PO_WINS'] >= 8:
            PO_elim = 'Runner Up'
        elif row['PO_WINS'] == 12:
            PO_elim = 'Champ'
        else:
            PO_elim = 'Not Qualified'
    elif row['YEAR'] in yearsUntil75:
        if row['PO_WINS'] < 4 and row['PO_LOSSES'] > 0:
            PO_elim = 'CSF Exit'
        elif row['PO_WINS'] < 8 and row['PO_WINS'] >= 4:
            PO_elim = 'CF Exit'
        elif row['PO_WINS'] < 12 and row['PO_WINS'] >= 8:
            PO_elim = 'Runner Up'
        elif row['PO_WINS'] == 12:
            PO_elim = 'Champ'
        else:
            PO_elim = 'Not Qualified'
    elif row['YEAR'] in yearsUntil77:
        if row['CONF_RANK'] in [4,5]:
            if row['PO_WINS'] < 2 and row['PO_LOSSES'] > 0:
                PO_elim = 'FR Exit'
            elif row['PO_WINS'] >= 2 and row['PO_WINS'] < 6 and row['PO_LOSSES'] > 0:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 10 and row['PO_WINS'] >= 6:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 14 and row['PO_WINS'] >= 10:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 14:
                PO_elim = 'Champ'
        elif row['CONF_RANK'] <4:
            if row['PO_WINS'] < 4 and row['PO_LOSSES'] > 0:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 8 and row['PO_WINS'] >= 4:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 12 and row['PO_WINS'] >= 8:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 12:
                PO_elim = 'Champ' 
        else:
            PO_elim = 'Not Qualified' 
    elif row['YEAR'] in yearsUntil84:
        if row['CONF_RANK'] in [3,4,5,6]:
            if row['PO_WINS'] < 2 and row['PO_LOSSES'] > 0:
                PO_elim = 'FR Exit'
            elif row['PO_WINS'] >= 2 and row['PO_WINS'] < 6 and row['PO_LOSSES'] > 0:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 10 and row['PO_WINS'] >= 6:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 14 and row['PO_WINS'] >= 10:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 14:
                PO_elim = 'Champ'
        elif row['CONF_RANK'] <3:
            if row['PO_WINS'] < 4 and row['PO_LOSSES'] > 0:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 8 and row['PO_WINS'] >= 4:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 12 and row['PO_WINS'] >= 8:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 12:
                PO_elim = 'Champ' 
        else:
            PO_elim = 'Not Qualified' 
    elif row['YEAR'] in yearsUntil03:
            if row['PO_WINS'] < 3 and row['PO_LOSSES'] > 0:
                PO_elim = 'FR Exit'
            elif row['PO_WINS'] < 7 and row['PO_WINS'] >= 3:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 11 and row['PO_WINS'] >= 7:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 15 and row['PO_WINS'] >= 11:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 15:
                PO_elim = 'Champ' 
            else:
                PO_elim = 'Not Qualified' 
    else:
            if row['PO_WINS'] < 4 and row['PO_LOSSES'] > 0:
                PO_elim = 'FR Exit'
            elif row['PO_WINS'] < 8 and row['PO_WINS'] >= 4:
                PO_elim = 'CSF Exit'
            elif row['PO_WINS'] < 12 and row['PO_WINS'] >= 8:
                PO_elim = 'CF Exit'
            elif row['PO_WINS'] < 16 and row['PO_WINS'] >= 12:
                PO_elim = 'Runner Up'
            elif row['PO_WINS'] == 16:
                PO_elim = 'Champ' 
            else:
                PO_elim = 'Not Qualified' 
    
    
    if len(df) < 59:
        # print('teste1')
        df_my_count = df.copy()
        my_count = df_my_count.value_counts('WL')
        if my_count.filter(items=['W'])[0] >= math.floor(len(df_my_count)*0.67):
            myList.append(True)
        else:
            myList.append(False)
            
        if any(myList):
            PJ_stats = True
        else:
            PJ_stats = False
     
    else:
        # print('teste2')

        for i in range(0, len(df)-59):
            df_my_count = df.copy()
            df_my_count = df_my_count.iloc[0+i:59+i]
            my_count = df_my_count.value_counts('WL')
            if my_count.filter(items=['W'])[0] >= 40:
                myList.append(True)
            else:
                myList.append(False)
                
        if any(myList):
            PJ_stats = True
        else:
            PJ_stats = False

    df = df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum())
    df= (df.assign(streak=(df['WL'] != df['WL'].shift()).cumsum()).groupby('streak').filter(lambda g:(g['WL'].iloc[0] == 'L') & (len(g) > 1)).drop_duplicates('streak'))
    
    export_data.append({
         'Team':row['TEAM_NAME'],
         'Season':row['YEAR'],
         'Record':str(row['WINS']) + '-' + str(row['LOSSES']),
         'Loss Streaks in season':len(df),
         'Finals Stats':PO_elim,
         'Phil Jackson Achieved': PJ_stats
         })


df_export_data = pd.DataFrame(export_data)
df_export_data.to_markdown('../data/historical_Phil_Jackson_adapt_and_loss_Streaks.md')