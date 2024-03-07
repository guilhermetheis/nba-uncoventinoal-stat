# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 09:43:55 2024

@author: 20195511
"""

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

## load csv

df_pj =  pd.read_csv('../data/csv/PJ Teams.csv')

# Separate PJ True

df_pj_true = df_pj.copy()
df_pj_true = df_pj_true.loc[df_pj_true['PJ Positive'] == True]

# PJ False
df_pj_false = df_pj.copy()
df_pj_false = df_pj_false.loc[df_pj_false['PJ Positive'] == False]

# Histograms

df_pj_true['Playoffs Results'].value_counts().plot(kind='bar', title='Playoff Results of PJ-Positive Teams')
plt.savefig('../figs/PJ_positive.png', dpi='figure',bbox_inches='tight')
df_pj_false['Playoffs Results'].value_counts().plot(kind='bar', title='Playoff Results of PJ-Negative Teams')
plt.savefig('../figs/PJ_negative.png', dpi='figure',bbox_inches='tight')