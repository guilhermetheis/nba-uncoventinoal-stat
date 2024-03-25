# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:25:36 2024

@author: 20195511
"""


import pandas as pd
import time

from nba_api.stats.endpoints import BoxScoreScoringV2

data = BoxScoreScoringV2(game_id='0022301027').data_sets