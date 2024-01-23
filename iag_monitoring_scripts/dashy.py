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

#combinedACK = pd.DataFrame()
#combinedICTX = pd.DataFrame()
#combinedICTXAway = pd.DataFrame()
#combinedICRX = pd.DataFrame()
#combinedICRXAway = pd.DataFrame()


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

    combinedACK.to_csv('ack sample.csv', index=False)




    #Process ACK

    combinedACK['File Name'] = combinedACK['ACK Entry'].str.slice(10,38)
    combinedACK['File Name'] = combinedACK['File Name'].str.strip()
    combinedACK['ACK Code'] = combinedACK['ACK Entry'].str.slice(74,77)
    combinedACK['ACK Datetime'] = combinedACK['ACK Entry'].str.slice(60,74)
    combinedACK['ACK Datetime'] = pd.to_datetime(combinedACK['ACK Datetime'])
    combinedACK.to_csv('ack sample.csv', index=False)

    return combinedACK



def processICLP(combinedACK, sentPath):
    #processACK()
    read_ICLP = sorted(Path(sentPath).glob('*.ICLP'))

    ICLPList = []
    ICLPCountList = []

    for file in read_ICLP:
        tempICLP = pd.read_csv(file,header=0)
        ICLPCountList.append(tempICLP.count())
        ICLPList.append(file.name) # additional arguments up to your needs

    ICLPFileList = pd.DataFrame(ICLPList, columns=['File Name'])
    ICLPCountDFSeries = pd.concat(ICLPCountList, ignore_index=True)
    ICLPCountDF =  pd.DataFrame(ICLPCountDFSeries, columns=['Record Count'])
    ICLPFileList = pd.concat([ICLPFileList,ICLPCountDF], axis=1)



    #Process ICLP

    ICLPFileList['Creation Date'] = ICLPFileList['File Name'].str.slice(4,18)
    ICLPFileList['Creation Date'] = pd.to_datetime(ICLPFileList['Creation Date'])
    ICLPFileList = pd.merge(ICLPFileList,combinedACK,how='left',on='File Name')
    ICLPFileList["ACK Code"].fillna("no ACK", inplace = True)
    ICLPFileList = ICLPFileList[['Creation Date', 'File Name', 'Record Count', 'ACK Code', 'ACK Datetime']]
    ICLPFileList = ICLPFileList.sort_values(by='Creation Date', ascending=False)

    ICLPFileList.to_csv('Outbound ICLP List.csv', index=False)

    return ICLPFileList



def processICLPAway(combinedACK, processedPath):
    read_ICLP_Away = sorted(Path(processedPath).glob('*.ICLP'))

    ICLPListAway = []
    #ICLPCountList = []

    for file in read_ICLP_Away:
        #tempICLP = pd.read_csv(file,header=0, on_bad_lines='skip')
        #ICLPCountList.append(tempICLP.count())
        ICLPListAway.append(file.name) # additional arguments up to your needs

    ICLPFileListAway = pd.DataFrame(ICLPListAway, columns=['File Name'])
    #ICLPCountDFSeries = pd.concat(ICLPCountList, ignore_index=True)
    #ICLPCountDF =  pd.DataFrame(ICLPCountDFSeries, columns=['Record Count'])
    #ICLPFileListAway = pd.concat([ICLPFileListAway,ICLPCountDF], axis=1)


    #Process ICLP

    ICLPFileListAway['Creation Date'] = ICLPFileListAway['File Name'].str.slice(4,18)
    ICLPFileListAway['Creation Date'] = pd.to_datetime(ICLPFileListAway['Creation Date'])
    ICLPFileListAway = pd.merge(ICLPFileListAway,combinedACK,how='left',on='File Name')
    ICLPFileListAway["ACK Code"].fillna("no ACK", inplace = True)
    ICLPFileListAway = ICLPFileListAway[['Creation Date', 'File Name', 'ACK Code', 'ACK Datetime']]
    ICLPFileListAway = ICLPFileListAway.sort_values(by='Creation Date', ascending=False)

    ICLPFileListAway.to_csv('Inbound ICLP List.csv', index=False)

    return ICLPFileListAway



def processITAG(combinedACK, sentPath):
    read_ITAG = sorted(Path(sentPath).glob('*.ITAG'))


    ITAGList = []
    ITAGCountList = []
    
    for file in read_ITAG:
        tempITAG = pd.read_csv(file,header=0)
        ITAGCountList.append(tempITAG.count())
        ITAGList.append(file.name) # additional arguments up to your needs
    
    ITAGFileList = pd.DataFrame(ITAGList, columns=['File Name'])
    ITAGCountDFSeries = pd.concat(ITAGCountList, ignore_index=True)
    ITAGCountDF =  pd.DataFrame(ITAGCountDFSeries, columns=['Record Count'])
    ITAGFileList = pd.concat([ITAGFileList,ITAGCountDF], axis=1)


    ITAGFileList['Creation Date'] = ITAGFileList['File Name'].str.slice(4,18)
    ITAGFileList['Creation Date'] = pd.to_datetime(ITAGFileList['Creation Date'])
    ITAGFileList = pd.merge(ITAGFileList,combinedACK,how='left',on='File Name')
    ITAGFileList["ACK Code"].fillna("no ACK", inplace = True)
    ITAGFileList = ITAGFileList[['Creation Date', 'File Name', 'Record Count', 'ACK Code', 'ACK Datetime']]
    ITAGFileList = ITAGFileList.sort_values(by='Creation Date', ascending=False)

    ITAGFileList.to_csv('Outbound ITAG List.csv', index=False)

    return ITAGFileList


def processITAGAway(combinedACK, processedPath):
    read_ITAG_Away = sorted(Path(processedPath).glob('*.ITAG'))

    #ITAGListAway = []

    #for file in read_ITAG_Away:
    #    ITAGListAway.append(file.name) # additional arguments up to your needs

    #ITAGFileListAway = pd.DataFrame(ITAGListAway, columns=['File Name'])

    ITAGListAway = []
    #ITAGCountList = []
    
    for file in read_ITAG_Away:
        #tempITAG = pd.read_csv(file,header=0)
        #ITAGCountList.append(tempITAG.count())
        ITAGListAway.append(file.name) # additional arguments up to your needs
    
    ITAGFileListAway = pd.DataFrame(ITAGListAway, columns=['File Name'])
    #ITAGCountDFSeries = pd.concat(ITAGCountList, ignore_index=True)
    #ITAGCountDF =  pd.DataFrame(ITAGCountDFSeries, columns=['Record Count'])
    #ITAGFileListAway = pd.concat([ITAGFileListAway,ITAGCountDF], axis=1)




    ITAGFileListAway['Creation Date'] = ITAGFileListAway['File Name'].str.slice(4,18)
    ITAGFileListAway['Creation Date'] = pd.to_datetime(ITAGFileListAway['Creation Date'])
    ITAGFileListAway = pd.merge(ITAGFileListAway,combinedACK,how='left',on='File Name')
    ITAGFileListAway["ACK Code"].fillna("no ACK", inplace = True)
    ITAGFileListAway = ITAGFileListAway[['Creation Date', 'File Name', 'ACK Code', 'ACK Datetime']]
    ITAGFileListAway = ITAGFileListAway.sort_values(by='Creation Date', ascending=False)

    ITAGFileListAway.to_csv('Inbound ITAG List.csv', index=False)

    return ITAGFileListAway




def processICTX(combinedACK, sentPath):
    read_ICTX = sorted(Path(sentPath).glob('*.ICTX'))

    ictxfiles = []

    for file in read_ICTX:
        ictxDF = pd.read_csv(file) # additional arguments up to your needs
        ictxDF['ICTX File Name'] = file.name
        ictxDF.rename(columns={list(ictxDF)[0]:'ICTX Entry'}, inplace=True)
        ictxfiles.append(ictxDF)

    combinedICTX = pd.concat(ictxfiles)

    combinedICTX = combinedICTX.rename({'ICTX File Name':'File Name'}, axis=1)
    combinedICTX = pd.merge(combinedICTX,combinedACK,how='left',on='File Name')
    combinedICTX = combinedICTX.rename({'File Name':'ICTX File Name'}, axis=1)
    combinedICTX["ACK Code"].fillna("no ACK", inplace = True)
    combinedICTX = combinedICTX.rename({'ACK Code':'ICTX ACK Code'}, axis=1)
    combinedICTX = combinedICTX.rename({'ACK Datetime':'ICTX ACK Datetime'}, axis=1)
    combinedICTX['Creation Date'] = combinedICTX['ICTX File Name'].str.slice(8,22)
    combinedICTX['Creation Date'] = pd.to_datetime(combinedICTX['Creation Date'])
    combinedICTX['dateTime'] = combinedICTX['ICTX Entry'].str.slice(83,97)
    combinedICTX['dateTime'] = pd.to_datetime(combinedICTX['dateTime'])
    #combinedICTX['Creation Date'] = combinedICTX['Source'].str.slice(8,16)
    #combinedICTX['Creation Date'] = pd.to_datetime(combinedICTX['Creation Date'])
    combinedICTX['Today'] = dt.datetime.now()
    combinedICTX['File Age (Days)'] = combinedICTX['Today'].dt.date - combinedICTX['Creation Date'].dt.date
    combinedICTX['File Age (Days)'] = combinedICTX['File Age (Days)'].dt.total_seconds()/60/60/24
    combinedICTX['File Age (Days)'] = combinedICTX['File Age (Days)'].astype(int)
    combinedICTX = combinedICTX.drop('Today',axis=1)
    combinedICTX['trxID'] = combinedICTX['ICTX Entry'].str[:12]
    combinedICTX.to_csv('combinedICTX.csv', index=False)

    #will use eventually
    #combinedICTX['fileAge'] = combinedICTX['fileAge'].astype(str) + ' days old'
    #combinedICTX['agency'] = combinedICTX['ICTX Entry'].str.slice(44,47)
    #combinedICTX['tagID'] = combinedICTX['ICTX Entry'].str.slice(47,55)
    #combinedICTX['tagID'].loc[(combinedICTX['tagID'] == "********")] = 0
    #combinedICTX['tagID'] = combinedICTX['tagID'].astype(int)
    #combinedICTX['plate'] = combinedICTX['ICTX Entry'].str.slice(64,74)
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "039")] = "LEE"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "036")] = "CFX"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "035")] = "FTE"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "064")] = "FTE"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "033")] = "NCTA"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "037")] = "MDX"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "038")] = "THEA"
    #combinedICTX['agency'].loc[(combinedICTX['agency'] == "034")] = "SRTA"
    #combinedICTX['plate'] = combinedICTX['plate'].str.strip()
    #combinedICTX['plate'].loc[(combinedICTX['plate'] == "**********")] = 0

    return combinedICTX

def processICTXAway(combinedACK, processedPath):
    read_ICTX_Away = sorted(Path(processedPath).glob('*.ICTX'))

    ictxfilesaway = []

    for file in read_ICTX_Away:
        ictxDF = pd.read_csv(file) # additional arguments up to your needs
        ictxDF['ICTX File Name'] = file.name
        ictxDF.rename(columns={list(ictxDF)[0]:'ICTX Entry'}, inplace=True)
        ictxfilesaway.append(ictxDF)

    combinedICTXAway = pd.concat(ictxfilesaway)

    combinedICTXAway = combinedICTXAway.rename({'ICTX File Name':'File Name'}, axis=1)
    combinedICTXAway = pd.merge(combinedICTXAway,combinedACK,how='left',on='File Name')
    combinedICTXAway = combinedICTXAway.rename({'File Name':'ICTX File Name'}, axis=1)
    combinedICTXAway["ACK Code"].fillna("no ACK", inplace = True)
    combinedICTXAway = combinedICTXAway.rename({'ACK Code':'ICTX ACK Code'}, axis=1)
    combinedICTXAway = combinedICTXAway.rename({'ACK Datetime':'ICTX ACK Datetime'}, axis=1)
    combinedICTXAway['Creation Date'] = combinedICTXAway['ICTX File Name'].str.slice(8,22)
    combinedICTXAway['Creation Date'] = pd.to_datetime(combinedICTXAway['Creation Date'])
    combinedICTXAway['dateTime'] = combinedICTXAway['ICTX Entry'].str.slice(83,97)
    combinedICTXAway['dateTime'] = pd.to_datetime(combinedICTXAway['dateTime'])
    #combinedICTXAway['Creation Date'] = combinedICTXAway['Source'].str.slice(8,16)
    #combinedICTXAway['Creation Date'] = pd.to_datetime(combinedICTXAway['Creation Date'])
    combinedICTXAway['Today'] = dt.datetime.now()
    combinedICTXAway['File Age (Days)'] = combinedICTXAway['Today'].dt.date - combinedICTXAway['Creation Date'].dt.date
    combinedICTXAway['File Age (Days)'] = combinedICTXAway['File Age (Days)'].dt.total_seconds()/60/60/24
    combinedICTXAway['File Age (Days)'] = combinedICTXAway['File Age (Days)'].astype(int)
    combinedICTXAway = combinedICTXAway.drop('Today',axis=1)
    combinedICTXAway['trxID'] = combinedICTXAway['ICTX Entry'].str[:12]
    combinedICTXAway.to_csv('combinedICTXAway.csv', index=False)

    return combinedICTXAway

def processITXC(combinedACK, sentPath):
    read_ITXC = sorted(Path(sentPath).glob('*.ITXC'))

    itxcfiles = []

    for file in read_ITXC:
        itxcDF = pd.read_csv(file) # additional arguments up to your needs
        itxcDF['ITXC File Name'] = file.name
        itxcDF.rename(columns={list(itxcDF)[0]:'ITXC Entry'}, inplace=True)
        itxcfiles.append(itxcDF)

    combinedITXC = pd.concat(itxcfiles)

    combinedITXC = combinedITXC.rename({'ITXC File Name':'File Name'}, axis=1)
    combinedITXC = pd.merge(combinedITXC,combinedACK,how='left',on='File Name')
    combinedITXC = combinedITXC.rename({'File Name':'ITXC File Name'}, axis=1)
    combinedITXC["ACK Code"].fillna("no ACK", inplace = True)
    combinedITXC = combinedITXC.rename({'ACK Code':'ITXC ACK Code'}, axis=1)
    combinedITXC = combinedITXC.rename({'ACK Datetime':'ITXC ACK Datetime'}, axis=1)
    combinedITXC['Creation Date'] = combinedITXC['ITXC File Name'].str.slice(8,22)
    combinedITXC['Creation Date'] = pd.to_datetime(combinedITXC['Creation Date'])
    combinedITXC['dateTime'] = combinedITXC['ITXC Entry'].str.slice(83,97)
    combinedITXC['dateTime'] = pd.to_datetime(combinedITXC['dateTime'])
    #combinedITXC['Creation Date'] = combinedITXC['Source'].str.slice(8,16)
    #combinedITXC['Creation Date'] = pd.to_datetime(combinedITXC['Creation Date'])
    combinedITXC['Today'] = dt.datetime.now()
    combinedITXC['File Age (Days)'] = combinedITXC['Today'].dt.date - combinedITXC['Creation Date'].dt.date
    combinedITXC['File Age (Days)'] = combinedITXC['File Age (Days)'].dt.total_seconds()/60/60/24
    combinedITXC['File Age (Days)'] = combinedITXC['File Age (Days)'].astype(int)
    combinedITXC = combinedITXC.drop('Today',axis=1)
    combinedITXC['trxID'] = combinedITXC['ITXC Entry'].str[2:14]
    combinedITXC.to_csv('combinedITXC.csv', index=False)

    #will use eventually
    #combinedITXC['fileAge'] = combinedITXC['fileAge'].astype(str) + ' days old'
    #combinedITXC['agency'] = combinedITXC['ITXC Entry'].str.slice(44,47)
    #combinedITXC['tagID'] = combinedITXC['ITXC Entry'].str.slice(47,55)
    #combinedITXC['tagID'].loc[(combinedITXC['tagID'] == "********")] = 0
    #combinedITXC['tagID'] = combinedITXC['tagID'].astype(int)
    #combinedITXC['plate'] = combinedITXC['ITXC Entry'].str.slice(64,74)
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "039")] = "LEE"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "036")] = "CFX"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "035")] = "FTE"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "064")] = "FTE"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "033")] = "NCTA"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "037")] = "MDX"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "038")] = "THEA"
    #combinedITXC['agency'].loc[(combinedITXC['agency'] == "034")] = "SRTA"
    #combinedITXC['plate'] = combinedITXC['plate'].str.strip()
    #combinedITXC['plate'].loc[(combinedITXC['plate'] == "**********")] = 0

    return combinedITXC

def processITXCAway(combinedACK, processedPath):
    read_ITXC_Away = sorted(Path(processedPath).glob('*.ITXC'))

    itxcfilesaway = []

    for file in read_ITXC_Away:
        itxcDF = pd.read_csv(file) # additional arguments up to your needs
        itxcDF['ITXC File Name'] = file.name
        itxcDF.rename(columns={list(itxcDF)[0]:'ITXC Entry'}, inplace=True)
        itxcfilesaway.append(itxcDF)

    combinedITXCAway = pd.concat(itxcfilesaway)

    combinedITXCAway = combinedITXCAway.rename({'ITXC File Name':'File Name'}, axis=1)
    combinedITXCAway = pd.merge(combinedITXCAway,combinedACK,how='left',on='File Name')
    combinedITXCAway = combinedITXCAway.rename({'File Name':'ITXC File Name'}, axis=1)
    combinedITXCAway["ACK Code"].fillna("no ACK", inplace = True)
    combinedITXCAway = combinedITXCAway.rename({'ACK Code':'ITXC ACK Code'}, axis=1)
    combinedITXCAway = combinedITXCAway.rename({'ACK Datetime':'ITXC ACK Datetime'}, axis=1)
    combinedITXCAway['Creation Date'] = combinedITXCAway['ITXC File Name'].str.slice(8,22)
    combinedITXCAway['Creation Date'] = pd.to_datetime(combinedITXCAway['Creation Date'])
    combinedITXCAway['dateTime'] = combinedITXCAway['ITXC Entry'].str.slice(85,99)
    combinedITXCAway['dateTime'] = pd.to_datetime(combinedITXCAway['dateTime'])
    #combinedITXCAway['Creation Date'] = combinedITXCAway['Source'].str.slice(8,16)
    #combinedITXCAway['Creation Date'] = pd.to_datetime(combinedITXCAway['Creation Date'])
    combinedITXCAway['Today'] = dt.datetime.now()
    combinedITXCAway['File Age (Days)'] = combinedITXCAway['Today'].dt.date - combinedITXCAway['Creation Date'].dt.date
    combinedITXCAway['File Age (Days)'] = combinedITXCAway['File Age (Days)'].dt.total_seconds()/60/60/24
    combinedITXCAway['File Age (Days)'] = combinedITXCAway['File Age (Days)'].astype(int)
    combinedITXCAway = combinedITXCAway.drop('Today',axis=1)
    combinedITXCAway['trxID'] = combinedITXCAway['ITXC Entry'].str[2:14]
    combinedITXCAway.to_csv('combinedITXCAway.csv', index=False)

    return combinedITXCAway

def processICRX(combinedACK, sentPath):
    read_ICRX = sorted(Path(sentPath).glob('*.ICRX'))

    icrxfiles = []

    for file in read_ICRX:
        icrxDF = pd.read_csv(file) # additional arguments up to your needs
        icrxDF['File Name'] = file.name
        icrxDF.rename(columns={list(icrxDF)[0]:'ICRX Entry'}, inplace=True)
        icrxfiles.append(icrxDF)

    combinedICRX = pd.concat(icrxfiles)

    #Process ICRX

    combinedICRX['trxID'] = combinedICRX['ICRX Entry'].str[:12]
    combinedICRX['ICRX Creation Date'] = combinedICRX['File Name'].str.slice(8,22)
    combinedICRX['ICRX Creation Date'] = pd.to_datetime(combinedICRX['ICRX Creation Date'])
    combinedICRX = pd.merge(combinedICRX,combinedACK,how='left',on='File Name')
    combinedICRX = combinedICRX.rename({'File Name':'ICRX File Name'}, axis=1)
    combinedICRX["ACK Code"].fillna("no ACK", inplace = True)
    combinedICRX.to_csv('combinedICRX.csv', index=False)

    #will use eventually
    #combinedICRX['recCode'] = combinedICRX['ICRX Entry'].str.slice(12, 16)
    #combinedICRX['actualValue'] = combinedICRX['ICRX Entry'].str.slice(22,27)
    #combinedICRX['actualValue'] = combinedICRX['actualValue'].astype(int)
    #combinedICRX['actualValue'] = combinedICRX['actualValue']/100

    return combinedICRX

def processICRXAway(combinedACK, processedPath):
    read_ICRX_Away = sorted(Path(processedPath).glob('*.ICRX'))

    icrxfilesaway = []

    for file in read_ICRX_Away:
        icrxDF = pd.read_csv(file) # additional arguments up to your needs
        icrxDF['File Name'] = file.name
        icrxDF.rename(columns={list(icrxDF)[0]:'ICRX Entry'}, inplace=True)
        icrxfilesaway.append(icrxDF)

    combinedICRXAway = pd.concat(icrxfilesaway)

    #Process outbound ICRX

    combinedICRXAway['trxID'] = combinedICRXAway['ICRX Entry'].str[:12]
    combinedICRXAway['ICRX Creation Date'] = combinedICRXAway['File Name'].str.slice(8,22)
    combinedICRXAway['ICRX Creation Date'] = pd.to_datetime(combinedICRXAway['ICRX Creation Date'])
    combinedICRXAway = pd.merge(combinedICRXAway,combinedACK,how='left',on='File Name')
    combinedICRXAway = combinedICRXAway.rename({'File Name':'ICRX File Name'}, axis=1)
    combinedICRXAway["ACK Code"].fillna("no ACK", inplace = True)
    combinedICRXAway.to_csv('combinedICRXAway.csv', index=False)

    return combinedICRXAway

def processIRXC(combinedACK, sentPath):
    read_IRXC = sorted(Path(sentPath).glob('*.IRXC'))

    irxcfiles = []

    for file in read_IRXC:
        irxcDF = pd.read_csv(file) # additional arguments up to your needs
        irxcDF['File Name'] = file.name
        irxcDF.rename(columns={list(irxcDF)[0]:'IRXC Entry'}, inplace=True)
        irxcfiles.append(irxcDF)

    combinedIRXC = pd.concat(irxcfiles)

    #Process IRXC

    combinedIRXC['trxID'] = combinedIRXC['IRXC Entry'].str[:12]
    combinedIRXC['IRXC Creation Date'] = combinedIRXC['File Name'].str.slice(8,22)
    combinedIRXC['IRXC Creation Date'] = pd.to_datetime(combinedIRXC['IRXC Creation Date'])
    combinedIRXC = pd.merge(combinedIRXC,combinedACK,how='left',on='File Name')
    combinedIRXC = combinedIRXC.rename({'File Name':'IRXC File Name'}, axis=1)
    combinedIRXC["ACK Code"].fillna("no ACK", inplace = True)
    combinedIRXC.to_csv('combinedIRXC.csv', index=False)

    #will use eventually
    #combinedIRXC['recCode'] = combinedIRXC['IRXC Entry'].str.slice(12, 16)
    #combinedIRXC['actualValue'] = combinedIRXC['IRXC Entry'].str.slice(22,27)
    #combinedIRXC['actualValue'] = combinedIRXC['actualValue'].astype(int)
    #combinedIRXC['actualValue'] = combinedIRXC['actualValue']/100

    return combinedIRXC

def processIRXCAway(combinedACK, processedPath):
    read_IRXC_Away = sorted(Path(processedPath).glob('*.IRXC'))

    irxcfilesaway = []

    for file in read_IRXC_Away:
        irxcDF = pd.read_csv(file) # additional arguments up to your needs
        irxcDF['File Name'] = file.name
        irxcDF.rename(columns={list(irxcDF)[0]:'IRXC Entry'}, inplace=True)
        irxcfilesaway.append(irxcDF)

    combinedIRXCAway = pd.concat(irxcfilesaway)

    #Process outbound IRXC

    combinedIRXCAway['trxID'] = combinedIRXCAway['IRXC Entry'].str[:12]
    combinedIRXCAway['IRXC Creation Date'] = combinedIRXCAway['File Name'].str.slice(8,22)
    combinedIRXCAway['IRXC Creation Date'] = pd.to_datetime(combinedIRXCAway['IRXC Creation Date'])
    combinedIRXCAway = pd.merge(combinedIRXCAway,combinedACK,how='left',on='File Name')
    combinedIRXCAway = combinedIRXCAway.rename({'File Name':'IRXC File Name'}, axis=1)
    combinedIRXCAway["ACK Code"].fillna("no ACK", inplace = True)
    combinedIRXCAway.to_csv('combinedIRXCAway.csv', index=False)

    return combinedIRXCAway

def joinFiles(combinedICTX, combinedICRX, transactionBrowserRowCount):
    #Join
    ICTXtoICRX = pd.merge(combinedICTX,combinedICRX,how='left',on='trxID')
    


    flterMissingICRX = ICTXtoICRX.loc[ICTXtoICRX['ICRX Entry'].isnull()]
    flterMissingICRX = flterMissingICRX[['Creation Date', 'ICTX File Name', 'ICTX ACK Code', 'ICTX ACK Datetime', 'File Age (Days)']]
    flterMissingICRX = flterMissingICRX.drop_duplicates(subset="ICTX File Name", keep='first')
    flterMissingICRX = flterMissingICRX.sort_values(by='Creation Date', ascending=False)
    
    ICTXtoICRX = ICTXtoICRX.loc[ICTXtoICRX['ICRX Entry'].notnull()]
    transactionTable = ICTXtoICRX
    transactionTable = transactionTable.sort_values(by='Creation Date', ascending=False)
    transactionTable['Turnaround Time (Days)'] = transactionTable['Creation Date'].dt.date - transactionTable['dateTime'].dt.date
    transactionTable['Turnaround Time (Days)'] = transactionTable['Turnaround Time (Days)'].dt.total_seconds()/60/60/24
    transactionTable['Turnaround Time (Days)'] = transactionTable['Turnaround Time (Days)'].astype(int)
    transactionTable['Reconciliation Code'] = transactionTable['ICRX Entry'].str.slice(12, 16)
    transactionTable['tagID'] = transactionTable['ICTX Entry'].str.slice(47,55)
    transactionTable['tagID'].loc[(transactionTable['tagID'] == "********")] = 0
    transactionTable['tagID'] = transactionTable['tagID'].astype(int)
    transactionTable['Value'] = transactionTable['ICTX Entry'].str[-5:]
    transactionTable['Value'] = transactionTable['Value'].astype(int)
    transactionTable['Value'] = transactionTable['Value']/100
    transactionTable['Plate'] = transactionTable['ICTX Entry'].str.slice(64,74)
    transactionTable['Plate'] = transactionTable['Plate'].str.strip()
    transactionTable['Plate'].loc[(transactionTable['Plate'] == "**********")] = 0
    transactionTable['Transaction Agency'] = transactionTable['ICTX Entry'].str.slice(21,23)
    transactionTable['Transaction Agency'] = transactionTable['Transaction Agency'].str.zfill(3)
    transactionTable['Transponder Agency'] = transactionTable['ICTX Entry'].str.slice(45,47)
    transactionTable['Transponder Agency'] = transactionTable['Transponder Agency'].str.zfill(3)
    transactionTable['Transponder Agency'].loc[(transactionTable['tagID'] == 16777215)] = "IMAGE BASED"
    #transactionTable = transactionTable[['ICTX Entry', 'ICTX File Name', 'ICRX File Name', 'ACK Code', 'Turnaround Time (Days)']]
    transactionTable = transactionTable.head(transactionBrowserRowCount)
    ICTXtoICRX.to_csv('tester.csv', index=False)
    ICTXtoICRX['Turnaround Time (Days)'] = ICTXtoICRX['ICRX Creation Date'].dt.date - ICTXtoICRX['Creation Date'].dt.date
    ICTXtoICRX['Turnaround Time (Days)'] = ICTXtoICRX['Turnaround Time (Days)'].dt.total_seconds()/60/60/24
    ICTXtoICRX['Turnaround Time (Days)'] = ICTXtoICRX['Turnaround Time (Days)'].astype(int)
    ICTXtoICRX = ICTXtoICRX[['Creation Date', 'ICTX File Name', 'ICRX File Name', 'ACK Code', 'ICTX ACK Datetime', 'ACK Datetime', 'Turnaround Time (Days)']]
    ICTXtoICRX = ICTXtoICRX.drop_duplicates(subset="ICTX File Name", keep='first')
    ICTXtoICRX = ICTXtoICRX.sort_values(by='Creation Date', ascending=False)


    return flterMissingICRX, ICTXtoICRX, transactionTable

def joinCorrectionFiles(combinedITXC, combinedIRXC, transactionBrowserRowCount):
    #Join
    ITXCtoIRXC = pd.merge(combinedITXC,combinedIRXC,how='left',on='trxID')
    


    flterMissingIRXC = ITXCtoIRXC.loc[ITXCtoIRXC['IRXC Entry'].isnull()]
    flterMissingIRXC = flterMissingIRXC[['Creation Date', 'ITXC File Name', 'ITXC ACK Code', 'ITXC ACK Datetime', 'File Age (Days)']]
    flterMissingIRXC = flterMissingIRXC.drop_duplicates(subset="ITXC File Name", keep='first')
    flterMissingIRXC = flterMissingIRXC.sort_values(by='Creation Date', ascending=False)
    
    ITXCtoIRXC = ITXCtoIRXC.loc[ITXCtoIRXC['IRXC Entry'].notnull()]
    transactionTable = ITXCtoIRXC
    transactionTable = transactionTable.sort_values(by='Creation Date', ascending=False)
    transactionTable['Turnaround Time (Days)'] = transactionTable['Creation Date'].dt.date - transactionTable['dateTime'].dt.date
    transactionTable['Turnaround Time (Days)'] = transactionTable['Turnaround Time (Days)'].dt.total_seconds()/60/60/24
    #transactionTable['Turnaround Time (Days)'] = transactionTable['Turnaround Time (Days)']/60/60/24
    transactionTable['Turnaround Time (Days)'] = transactionTable['Turnaround Time (Days)'].astype(int)
    transactionTable['Reconciliation Code'] = transactionTable['IRXC Entry'].str.slice(12, 16)
    transactionTable['tagID'] = transactionTable['ITXC Entry'].str.slice(49,57)
    transactionTable['tagID'].loc[(transactionTable['tagID'] == "********")] = 0
    transactionTable['tagID'] = transactionTable['tagID'].astype(int)
    transactionTable['Value'] = transactionTable['ITXC Entry'].str[-5:]
    transactionTable['Value'] = transactionTable['Value'].astype(int)
    transactionTable['Value'] = transactionTable['Value']/100
    transactionTable['Plate'] = transactionTable['ITXC Entry'].str.slice(66,76)
    transactionTable['Plate'] = transactionTable['Plate'].str.strip()
    transactionTable['Plate'].loc[(transactionTable['Plate'] == "**********")] = 0
    transactionTable['Transaction Agency'] = transactionTable['ITXC Entry'].str.slice(23,25)
    transactionTable['Transaction Agency'] = transactionTable['Transaction Agency'].str.zfill(3)
    transactionTable['Transponder Agency'] = transactionTable['ITXC Entry'].str.slice(47,48)
    transactionTable['Transponder Agency'] = transactionTable['Transponder Agency'].str.zfill(3)
    transactionTable['Transponder Agency'].loc[(transactionTable['tagID'] == 16777215)] = "IMAGE BASED"
    #transactionTable = transactionTable[['ITXC Entry', 'ITXC File Name', 'IRXC File Name', 'ACK Code', 'Turnaround Time (Days)']]
    transactionTable = transactionTable.head(transactionBrowserRowCount)
    ITXCtoIRXC.to_csv('tester.csv', index=False)
    ITXCtoIRXC['Turnaround Time (Days)'] = ITXCtoIRXC['IRXC Creation Date'].dt.date - ITXCtoIRXC['Creation Date'].dt.date
    ITXCtoIRXC['Turnaround Time (Days)'] = ITXCtoIRXC['Turnaround Time (Days)'].dt.total_seconds()/60/60/24
    #ITXCtoIRXC['Turnaround Time (Days)'] = ITXCtoIRXC['Turnaround Time (Days)']/60/60/24
    ITXCtoIRXC['Turnaround Time (Days)'] = ITXCtoIRXC['Turnaround Time (Days)'].astype(int)
    ITXCtoIRXC = ITXCtoIRXC[['Creation Date', 'ITXC File Name', 'IRXC File Name', 'ACK Code', 'ITXC ACK Datetime', 'ACK Datetime', 'Turnaround Time (Days)']]
    ITXCtoIRXC = ITXCtoIRXC.drop_duplicates(subset="ITXC File Name", keep='first')
    ITXCtoIRXC = ITXCtoIRXC.sort_values(by='Creation Date', ascending=False)


    return flterMissingIRXC, ITXCtoIRXC, transactionTable
