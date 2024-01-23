# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 18:23:07 2022

@author: dcox
"""
import pandas as pd
import datetime as dt
import glob
import numpy as np
import os
from io import StringIO
from pathlib import Path

import plotly.express as px
from dash import dash_table
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

def processACK(sentPath, processedPath):
    read_ACK = sorted(Path(sentPath).glob('*.ACK'))

    ACKList = []

    for file in read_ACK:
        ackDF = pd.read_csv(file, header=None) # additional arguments up to your needs
        ackDF['ACK File Name'] = file.name
        ackDF.rename(columns={list(ackDF)[0]:'ACK Entry'}, inplace=True)
        ACKList.append(ackDF)

    combinedACK_1 = pd.concat(ACKList)
    
    read_ACK2 = sorted(Path(processedPath).glob('*.ACK'))

    ACKList2 = []

    for file in read_ACK2:
        ackDF2 = pd.read_csv(file, header=None) # additional arguments up to your needs
        ackDF2['ACK File Name'] = file.name
        ackDF2.rename(columns={list(ackDF2)[0]:'ACK Entry'}, inplace=True)
        ACKList2.append(ackDF2)

    combinedACK_2 = pd.concat(ACKList2)
    
    combinedACK = pd.concat([combinedACK_1, combinedACK_2])

    combinedACK.to_csv('ack_sample.csv', index=False)

    #Process ACK

    combinedACK['File Name'] = combinedACK['ACK Entry'].str.slice(10,38)
    combinedACK['File Name'] = combinedACK['File Name'].str.strip()
    combinedACK['ACK Code'] = combinedACK['ACK Entry'].str.slice(74,77)
    combinedACK['ACK Datetime'] = combinedACK['ACK Entry'].str.slice(60,74)
    combinedACK['ACK Datetime'] = pd.to_datetime(combinedACK['ACK Datetime'])
    combinedACK.to_csv('ack_sample.csv', index=False)

    return combinedACK

# Uncomment the following import statements:
from dash import dash_table
import dash_bootstrap_components as dbc

# Remove the following code block:
#combinedACK = pd.DataFrame()
#combinedICTX = pd.DataFrame()
#combinedICTXAway = pd.DataFrame()
#combinedICRX = pd.DataFrame()
#combinedICRXAway = pd.DataFrame()

# Update the line 'combinedACK.to_csv('ack sample.csv', index=False)' to 'combinedACK.to_csv('ack_sample.csv', index=False)' to change the output file name.

# Update the line 'ICTXtoICRX.to_csv('tester.csv', index=False)' to 'ICTXtoICRX.to_csv('ICTXtoICRX.csv', index=False)' to change the output file name.

# Update the line 'ITXCtoIRXC.to_csv('tester.csv', index=False)' to 'ITXCtoIRXC.to_csv('ITXCtoIRXC.csv', index=False)' to change the output file name.
