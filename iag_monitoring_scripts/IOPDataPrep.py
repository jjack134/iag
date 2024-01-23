# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:37:55 2023
@author: dcox
"""

import pandas as pd
from datetime import date
import os
from pathlib import Path
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from dashy import processACK, processICTX, processICTXAway, processICRX, processICRXAway, processITXC, processITXCAway, processICLP, processICLPAway, processITAG, processITAGAway, processIRXC, processIRXCAway, joinFiles, joinCorrectionFiles

today = date.today()
transactionBrowserRowCount = 1000000
todaysDate = today.strftime("%m.%d")

processedPath = r"D:\IOP\IOP Phase II Sync\ProcessedFolder"
sentPath = r"D:\IOP\IOP Phase II Sync\SentFolder"

combinedACK = processACK(sentPath, processedPath)
combinedICTX = processICTX(combinedACK, sentPath)
combinedICTXAway = processICTXAway(combinedACK, processedPath)
combinedICRX = processICRX(combinedACK, sentPath)
combinedICRXAway = processICRXAway(combinedACK, processedPath)

try:
    combinedITXC = processITXC(combinedACK, sentPath)
except:
    print("no ITXC")
combinedITXCAway = processITXCAway(combinedACK, processedPath)
combinedIRXC = processIRXC(combinedACK, sentPath)
try:
    combinedIRXCAway = processIRXCAway(combinedACK, processedPath) 
except:
    print("no IRXC")

ICLPFileList = processICLP(combinedACK, sentPath)
ICLPFileListAway = processICLPAway(combinedACK, processedPath)
ITAGFileList = processITAG(combinedACK, sentPath)
ITAGFileListAway = processITAGAway(combinedACK, processedPath)

ICLPFileList.to_csv('ICLPFileList ' + todaysDate + '.csv', index=False)
ICLPFileListAway.to_csv('ICLPFileListAway ' + todaysDate + '.csv', index=False)
ITAGFileList.to_csv('ITAGFileList ' + todaysDate + '.csv', index=False)
ITAGFileListAway.to_csv('ITAGFileListAway ' + todaysDate + '.csv', index=False)

flterMissingICRX, ICTXtoICRX, homeTransactionTable = joinFiles(combinedICTX, combinedICRXAway, transactionBrowserRowCount)
flterMissingICRX.to_csv('missingResponse ' + todaysDate +'.csv', index=False)
ICTXtoICRX.to_csv('mergedFiles ' + todaysDate +'.csv', index=False)
homeTransactionTable.to_csv('homeTransactionTable ' + todaysDate +'.csv', index=False)
homeAgencyCount = homeTransactionTable.groupby(['Transponder Agency']).count()
homeAgencyCount.to_csv('homeAgencyCount ' + todaysDate +'.csv', index=True)
flterMissingICRXAway, ICTXtoICRXAway, awayTransactionTable = joinFiles(combinedICTXAway, combinedICRX, transactionBrowserRowCount)
flterMissingICRXAway.to_csv('missingResponseAway ' + todaysDate +'.csv', index=False)
ICTXtoICRXAway.to_csv('mergedFilesAway ' + todaysDate +'.csv', index=False)
awayTransactionTable.to_csv('awayTransactionTable ' + todaysDate +'.csv', index=False)
awayAgencyCount = awayTransactionTable.groupby(['Transaction Agency']).count()
awayAgencyCount.to_csv('awayAgencyCount ' + todaysDate +'.csv', index=True)

try:
    flterMissingIRXC, ITXCtoIRXC, homeCorrectionTable = joinCorrectionFiles(combinedITXC, combinedIRXCAway, transactionBrowserRowCount)
except:
    print("no ITXC")

try:
    flterMissingIRXC.to_csv('missingCorrection ' + todaysDate +'.csv', index=False)
    ITXCtoIRXC.to_csv('mergedCorrectionFiles ' + todaysDate +'.csv', index=False)
    homeCorrectionTable.to_csv('homeCorrectionTable ' + todaysDate +'.csv', index=False)
    homeCorrectionCount = homeCorrectionTable.groupby(['Transponder Agency']).count()
    homeCorrectionCount.to_csv('homeCorrectionCount ' + todaysDate +'.csv', index=True)
except:
    print("no Home Correction files")

flterMissingIRXCAway, ITXCtoIRXCAway, awayCorrectionTable = joinCorrectionFiles(combinedITXCAway, combinedIRXC, transactionBrowserRowCount)
flterMissingIRXCAway.to_csv('missingCorrectionAway ' + todaysDate +'.csv', index=False)
ITXCtoIRXCAway.to_csv('mergedCorrectionFilesAway ' + todaysDate +'.csv', index=False)
awayCorrectionTable.to_csv('awayCorrectionTable ' + todaysDate +'.csv', index=False)
awayCorrectionCount = awayCorrectionTable.groupby(['Transaction Agency']).count()
awayCorrectionCount.to_csv('awayCorrectionCount ' + todaysDate +'.csv', index=True)
