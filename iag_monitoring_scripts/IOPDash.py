#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import datetime as dt
from datetime import date
import glob
import numpy as np
import os
from io import StringIO
from pathlib import Path

import plotly.express as px
from dash import dash_table
from dash import Dash, dcc, html
#import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from dashy import *


#q = Queue(connection=conn)

#os.getcwd()
#os.chdir('C:/Users/dcox/E2E')


#combinedACK = q.enqueue(processACK)
#combinedICTX = q.enqueue(processICTX)
#combinedICTXAway = q.enqueue(processICTXAway)
#combinedICRX = q.enqueue(processICRX)
#combinedICRXAway = q.enqueue(processICRXAway)

#time.sleep(2)

#transactionBrowserRowCount = 150000
Port = 3020
today = date.today()
todaysDate = today.strftime("%m.%d")

#todaysDate = today.strftime("10.04")

load_figure_template("darkly")
"""
combinedACK = processACK()
combinedICTX = processICTX(combinedACK)
combinedICTXAway = processICTXAway(combinedACK)
combinedICRX = processICRX(combinedACK)
combinedICRXAway = processICRXAway(combinedACK) 

ICLPFileList = processICLP(combinedACK)
ICLPFileListAway = processICLPAway(combinedACK)
ITAGFileList = processITAG(combinedACK)
ITAGFileListAway = processITAGAway(combinedACK)

flterMissingICRX, ICTXtoICRX, homeTransactionTable = joinFiles(combinedICTX, combinedICRXAway, transactionBrowserRowCount)
flterMissingICRX.to_csv('missingResponse ' + date +'.csv', index=False)
ICTXtoICRX.to_csv('mergedFiles ' + date +'.csv', index=False)
homeTransactionTable.to_csv('homeTransactionTable ' + date +'.csv', index=False)
flterMissingICRXAway, ICTXtoICRXAway, awayTransactionTable = joinFiles(combinedICTXAway, combinedICRX, transactionBrowserRowCount)
flterMissingICRXAway.to_csv('missingResponseAway ' + date +'.csv', index=False)
ICTXtoICRXAway.to_csv('mergedFilesAway ' + date +'.csv', index=False)
awayTransactionTable.to_csv('awayTransactionTable ' + date +'.csv', index=False)
"""

ICLPFileList = pd.read_csv('ICLPFileList ' + todaysDate + '.csv')
ICLPFileListAway = pd.read_csv('ICLPFileListAway ' + todaysDate + '.csv')
ITAGFileList = pd.read_csv('ITAGFileList ' + todaysDate + '.csv')
ITAGFileListAway = pd.read_csv('ITAGFileListAway ' + todaysDate + '.csv')

flterMissingICRX = pd.read_csv('missingResponse ' + todaysDate + '.csv')
ICTXtoICRX = pd.read_csv('mergedFiles ' + todaysDate + '.csv')
homeTransactionTable = pd.read_csv('homeTransactionTable ' + todaysDate + '.csv')

flterMissingICRXAway = pd.read_csv('missingResponseAway ' + todaysDate + '.csv')
ICTXtoICRXAway = pd.read_csv('mergedFilesAway ' + todaysDate + '.csv')
awayTransactionTable = pd.read_csv('awayTransactionTable ' + todaysDate + '.csv')

flterMissingIRXCAway = pd.read_csv('missingCorrectionAway ' + todaysDate + '.csv')
ITXCtoIRXCAway = pd.read_csv('mergedCorrectionFilesAway ' + todaysDate + '.csv')
awayCorrectionTable = pd.read_csv('awayCorrectionTable ' + todaysDate + '.csv')

try:
    flterMissingIRXC = pd.read_csv('missingCorrection ' + todaysDate + '.csv')
except:
    print("no missing correction")
    flterMissingIRXC = flterMissingIRXCAway
    #flterMissingIRXC = flterMissingIRXC.drop(index=flterMissingIRXC.index, inplace=True)
    
try:
    ITXCtoIRXC = pd.read_csv('mergedCorrectionFiles ' + todaysDate + '.csv')
except:
    print("no home correction files")
    ITXCtoIRXC = ITXCtoIRXCAway
    #ITXCtoIRXC = ITXCtoIRXC.drop(index=ITXCtoIRXC.index, inplace=True)
    
try:
    homeCorrectionTable = pd.read_csv('homeCorrectionTable ' + todaysDate + '.csv')
except:
    print("no home correction table")
    homeCorrectionTable = awayCorrectionTable
    #homeCorrectionTable = homeCorrectionTable.drop(index=homeCorrectionTable.index, inplace=True)



custom_dict = {'POST': 0, 'PPST': 1,'RJPL': 2,'TAGB': 3,'RJDP': 4,'INSU': 5,'ACCB': 6,'RINV': 7,'NPST': 8,'OLD1': 9}
homeTransactionTableDT = homeTransactionTable
homeTransactionTableDT['Reconciliation Code Date'] = pd.to_datetime(homeTransactionTableDT['ICRX Creation Date']).dt.date
reconGrpHome = homeTransactionTableDT.groupby(['Reconciliation Code','Reconciliation Code Date'], as_index=False).count()
reconGrpHome = reconGrpHome.sort_values(by=['Reconciliation Code'], key=lambda x: x.map(custom_dict))
fig = px.pie(reconGrpHome,values='ICRX Entry', names='Reconciliation Code', title='150k Transaction Breakdown',color_discrete_sequence = px.colors.qualitative.G10)
#fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
fig5 = px.histogram(reconGrpHome, x='Reconciliation Code Date',y='ICRX Entry', title = 'Reconciliation Code Trend', 
              color = 'Reconciliation Code', barnorm='percent', color_discrete_sequence = px.colors.qualitative.G10)  
              
#color_discrete_sequence=px.colors.qualitative.Dark24)
awayTransactionTableDT = awayTransactionTable
awayTransactionTableDT['Reconciliation Code Date'] = pd.to_datetime(awayTransactionTableDT['ICRX Creation Date']).dt.date
reconGrpAway = awayTransactionTableDT.groupby(['Reconciliation Code','Reconciliation Code Date'], as_index=False).count()
reconGrpAway = reconGrpAway.sort_values(by=['Reconciliation Code'], key=lambda x: x.map(custom_dict))
fig2 = px.pie(reconGrpAway,values='ICRX Entry', names='Reconciliation Code', title='150k Transaction Breakdown',color_discrete_sequence = px.colors.qualitative.G10)
#fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0))
fig6 = px.histogram(reconGrpAway, x='Reconciliation Code Date',y='ICRX Entry', title = 'Reconciliation Code Trend', 
              color = 'Reconciliation Code', barnorm='percent', color_discrete_sequence = px.colors.qualitative.G10)  


ICLPFileListGraph = ICLPFileList.drop_duplicates(subset=['Creation Date'], keep='first')
fig3 = px.line(ICLPFileListGraph, x='Creation Date',y='Record Count', title = 'ICLP Record Count Trend')

ITAGFileListGraph = ITAGFileList.drop_duplicates(subset=['Creation Date'], keep='first')
fig4 = px.line(ITAGFileListGraph, x='Creation Date',y='Record Count', title = 'ITAG Record Count Trend')


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.DARKLY]

#app = Dash(__name__, external_stylesheets=external_stylesheets)
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
#app.layout = dash_table.DataTable(data=flterMissingICRX.to_dict('records'), 
#                                 columns=[{"name": i, "id": i} for i in flterMissingICRX.columns])

server = app.server

app.layout = html.Div([
    html.H1('IOP Monitoring Dash'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='ICTX/ICRX Monitoring', value='tab-1-example-graph'),
        dcc.Tab(label='ITXC/IRXC Monitoring', value='tab-2-example-graph'),
        dcc.Tab(label='ICLP Monitoring', value='tab-3-example-graph'),
        dcc.Tab(label='ITAG Monitoring', value='tab-4-example-graph'),
        dcc.Tab(label='Transaction Browser', value='tab-5-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
], className="dbc")



@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H6('Monitor inbound and outbound ICTX and their age.'),
             dcc.Tabs([
                 dcc.Tab(label='Unmatched Outbound ICTX Aging', children=[
                    dash_table.DataTable(data=flterMissingICRX.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in flterMissingICRX.columns],
                                sort_action='native',
                                editable=True,
                                page_size=10,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'filter_query': '{File Age (Days)} > 2',
                                            'column_id': 'File Age (Days)'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Codee',
                                            'filter_query': '{ICTX ACK Code = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Unmatched Inbound ICTX Aging', children=[
                    dash_table.DataTable(data=flterMissingICRXAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in flterMissingICRXAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=10,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'filter_query': '{File Age (Days)} > 2',
                                            'column_id': 'File Age (Days)'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Oubound ICTX -> ICRX', children=[
                    dash_table.DataTable(data=ICTXtoICRX.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ICTXtoICRX.columns],
                                sort_action='native',
                                editable=True,
                                page_size=15,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} = "2"'
                                        },
                                        'backgroundColor': 'gold',
                                        'color': 'black'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} > 2'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Inbound ICTX -> ICRX', children=[
                    dash_table.DataTable(data=ICTXtoICRXAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ICTXtoICRXAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=15,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} = "2"'
                                        },
                                        'backgroundColor': 'gold',
                                        'color': 'black'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} > 2'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ])
            ])
            
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H6('Monitor inbound and outbound ICTX and their age.'),
             dcc.Tabs([
                 dcc.Tab(label='Unmatched Outbound ICTX Aging', children=[
                    dash_table.DataTable(data=flterMissingIRXC.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in flterMissingIRXC.columns],
                                sort_action='native',
                                editable=True,
                                page_size=10,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'filter_query': '{File Age (Days)} > 2',
                                            'column_id': 'File Age (Days)'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'IRXC ACK Code',
                                            'filter_query': '{IRXC ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'IRXC ACK Codee',
                                            'filter_query': '{IRXC ACK Code = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'IRXC ACK Code',
                                            'filter_query': '{IRXC ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'IRXC ACK Code',
                                            'filter_query': '{IRXC ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Unmatched Inbound ICTX Aging', children=[
                    dash_table.DataTable(data=flterMissingIRXCAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in flterMissingIRXCAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=10,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'filter_query': '{File Age (Days)} > 2',
                                            'column_id': 'File Age (Days)'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ICTX ACK Code',
                                            'filter_query': '{ICTX ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Oubound ICTX -> ICRX', children=[
                    dash_table.DataTable(data=ITXCtoIRXC.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ITXCtoIRXC.columns],
                                sort_action='native',
                                editable=True,
                                page_size=15,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} = "2"'
                                        },
                                        'backgroundColor': 'gold',
                                        'color': 'black'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} > 2'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ]),
                dcc.Tab(label='Inbound ICTX -> ICRX', children=[
                    dash_table.DataTable(data=ITXCtoIRXCAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ITXCtoIRXCAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=15,
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "07"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "04"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "05"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} = "2"'
                                        },
                                        'backgroundColor': 'gold',
                                        'color': 'black'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'Turnaround Time (Days)',
                                            'filter_query': '{Turnaround Time (Days)} > 2'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                                ])
                ])
            ])
            
        ])
    elif tab == 'tab-3-example-graph':
        return html.Div([
            html.H6('Monitor inbound and outbound ICLP files and their ACK statuses.'),
            dcc.Tabs([
                 dcc.Tab(label='Outbound ICLP', children=[
                    dash_table.DataTable(data=ICLPFileList.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ICLPFileList.columns],
                                sort_action='native',
                                editable=True,
                                page_size=5,
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "02"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                        ]),
                    dcc.Graph(figure = fig3)
                ]),
                dcc.Tab(label='Inbound ICLP', children=[
                    dash_table.DataTable(data=ICLPFileListAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ICLPFileListAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=5,
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "02"'
                                        },
                                        'backgroundColor': 'gold',
                                        'color': 'black'
                                    }
                        ])
                ]),
            ])
        ])
    elif tab == 'tab-4-example-graph':
        return html.Div([
            html.H6('Monitor inbound and outbound ITAG files and their ACK statuses.'),
            dcc.Tabs([
                 dcc.Tab(label='Outbound ITAG', children=[
                    dash_table.DataTable(data=ITAGFileList.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ITAGFileList.columns],
                                sort_action='native',
                                editable=True,
                                page_size=5,
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "02"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                        ]),
                    dcc.Graph(figure = fig4)
                ]),
                dcc.Tab(label='Inbound ITAG', children=[
                    dash_table.DataTable(data=ITAGFileListAway.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in ITAGFileListAway.columns],
                                sort_action='native',
                                editable=True,
                                page_size=5,
                                style_data_conditional=[
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "no ACK"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },
                                    {
                                        'if':{
                                            'column_id': 'ACK Code',
                                            'filter_query': '{ACK Code} = "02"'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    }
                        ])
                ]),
            ])
        ])
    elif tab == 'tab-5-example-graph':
        return html.Div([
            html.H6('Browse transactions'),
            dcc.Tabs([
                 dcc.Tab(label='Outbound Transactions', children=[
                    dash_table.DataTable(data=homeTransactionTable.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in homeTransactionTable.columns],
                                sort_action='native',
                                editable=True,
                                page_size=20,
                                filter_action='native'
                                ),
                    dcc.Graph(figure = fig5),
                    dcc.Graph(figure = fig)
                ]),
                dcc.Tab(label='Inbound Transactions', children=[
                    dash_table.DataTable(data=awayTransactionTable.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in awayTransactionTable.columns],
                                sort_action='native',
                                editable=True,
                                page_size=20,
                                filter_action='native'
                                ),
                    dcc.Graph(figure = fig6),
                    dcc.Graph(figure = fig2)
                ]),
                
            ])
        ])

if __name__ == '__main__':
    app.run_server(debug=True, port=Port)





