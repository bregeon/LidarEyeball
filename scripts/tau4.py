#!/bin/env python
import glob
from datetime import datetime
import ROOT
from pLidarRun import pLidarRun
from pLidarRunPlotter import pLidarRunPlotter

# get all available runs
#runList=glob.glob('data/run*.root.txt')
#runList=glob.glob('alldata/run_06645*.root.txt')
#runList=glob.glob('alldata/run_0672*.root.txt') 
runList=glob.glob('alldata/run_0*.root.txt')
runList.sort()

# clean up bad runs
#runList.pop(runList.index('alldata/run_069054_Lidar_001.root.txt'))
#runList.pop(runList.index('alldata/run_069436_Lidar_001.root.txt'))
#runList.pop(runList.index('alldata/run_070085_Lidar_001.root.txt'))

# Parameters
nBins=100
nRuns=600

# Analyze data
rList=[]
nMax=min(nRuns+1,len(runList))
for run in runList[0:nMax]:
    newRun=pLidarRun(run, process=True, nBins=nBins)
    rList.append(newRun)

# Get Tau4 and fill in TGraph
gTau4=ROOT.TGraph(nMax)
i=0
for run in rList:
    tau4=run.getTau4()[1]
    runnb=int(run.RunNumber)
    gTau4.SetPoint(i, runnb, tau4)
    print i, runnb, tau4
    i+=1

# Plot Tau4 for the list of runs
cTau4=ROOT.TCanvas("Tau4Can","Tau4",30,50,850,650)
gTau4.GetYaxis().SetTitle("Tau4")
gTau4.GetXaxis().SetTitle("Run Number")
gTau4.Draw('AP*')
