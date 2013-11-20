#!/bin/env python
import glob
import ROOT
from pLidarRun import pLidarRun
from pLidarRunPlotter import pLidarRunPlotter

# get all available runs
#runList=glob.glob('alldata/run*.root.txt')
runList=glob.glob('23Sept2011/run*.root.txt')
runList.sort()

# clean up bad runs
#runList.pop(runList.index('alldata/run_069054_Lidar_001.root.txt'))
#runList.pop(runList.index('alldata/run_069436_Lidar_001.root.txt'))
#runList.pop(runList.index('alldata/run_070085_Lidar_001.root.txt'))

# Parameters
nBins=100
nRuns=600
nMax=min(nRuns+1,len(runList))

# Analyze data and prepare plots
pList=[]
for run in runList[0:nMax]:
    newRun=pLidarRun(run, process=False, nBins=nBins)
    #if newRun.RunNumber>69375 and newRun.RunNumber<69392:
    if newRun.RunNumber>67216:
        newRun.process(nBins=nBins)
        newPlotter=pLidarRunPlotter(newRun)
        newPlotter.fillKlettGraphs()
        pList.append(newPlotter)
  
# Choose wl to plot
wl=2

# Plot Power
cPower=ROOT.TCanvas("PowerCan","Power",30,50,850,650)
legP=ROOT.TLegend(0.5,0.65,0.9,0.9)
i=1
for p in pList:
   if i==1:
       p.plotOneLnPower(wl, gPad=cPower, opt='AP', color=i)
   else:
       p.plotOneLnPower(wl, gPad=cPower, opt='PS', color=i)
   legP.AddEntry(p.getLnPower(wl), '%s (%s)'%(p.LidarRun.DateTime,p.LidarRun.RunNumber))
   i+=1
legP.Draw()

# Plot Alpha
cAlpha=ROOT.TCanvas("AlphaCan","Alpha",30,50,850,650)
legA=ROOT.TLegend(0.5,0.65,0.9,0.9)
i=1
for p in pList:
   if i==1:
       p.plotOneAlpha(wl, gPad=cAlpha, opt='AP', color=i)
   else:
       p.plotOneAlpha(wl, gPad=cAlpha, opt='PS', color=i)
   legA.AddEntry(p.getLnPower(wl), '%s (%s)'%(p.LidarRun.DateTime,p.LidarRun.RunNumber))
   i+=1
legA.Draw()
