#!/bin/env python
import os
import ROOT
from pLidarRun import pLidarRun
from pLidarRunPlotter import pLidarRunPlotter
from toolBox import *

DATA_DIR='/home/bregeon/CTA/Lidar/alldata'

# Choose wl to plot and NBins
wl=2
nBins=100

# Choose night 
#date='2011-06-30 16:00:00'   # June 30th - quite good night ~ 10%
#date='2011-07-02 16:00:00'   # July 2nd - excellent night ~ 3%
date='2011-08-24 16:00:00'   # Aout 24th - ideal night ~ 1%
#date='2011-09-23 16:00:00'   # September 23rd - bad night ~ 68%
titleDate=date.split()[0]

# Get Runs for a given night
runList=[]
runNumbers=getRunsForNight(date)
for run in runNumbers:
  #if run%3==0:
    runList.append(os.path.join(DATA_DIR,LIDAR_RUN_DICT[run]['FileName']))
    

# Analyze data and prepare plots
pList=[]
for run in runList:
    newRun=pLidarRun(run, process=False, nBins=nBins)
    newRun.process(nBins=nBins)
    newPlotter=pLidarRunPlotter(newRun)
    newPlotter.fillKlettGraphs()
    pList.append(newPlotter)
  

# Plot Power
cPower=ROOT.TCanvas("PowerCan","Power",30,50,850,650)
legP=ROOT.TLegend(0.5,0.65,0.9,0.9)
gFakeLnPw=ROOT.TGraph(2)
gFakeLnPw.SetNameTitle('gFakeLnPw','Ln(Power): %s'%titleDate)
gFakeLnPw.SetPoint(0,-4,0)
gFakeLnPw.SetPoint(1,-1,10)
gFakeLnPw.Draw('AP')
i=1
for p in pList:
   if i==1:
       p.plotOneLnPower(wl, gPad=cPower, opt='PS', color=i)
   else:
       p.plotOneLnPower(wl, gPad=cPower, opt='PS', color=i)
   legP.AddEntry(p.getLnPower(wl), '%s (%s)'%(p.LidarRun.DateTime,p.LidarRun.RunNumber))
   i+=1
gFakeLnPw.GetXaxis().SetTitle("Ln(Power)")
gFakeLnPw.GetYaxis().SetTitle("Altitude (km)")
legP.Draw()

# Plot Alpha
cAlpha=ROOT.TCanvas("AlphaCan","Alpha",30,50,850,650)
legA=ROOT.TLegend(0.5,0.65,0.9,0.9)
gFakeAlpha=ROOT.TGraph(2)
gFakeAlpha.SetNameTitle('gFakeAlpha','Alpha: %s'%titleDate)
gFakeAlpha.SetPoint(0,0.01,0)
gFakeAlpha.SetPoint(1,1,10)
gFakeAlpha.Draw('AP')
i=1
for p in pList:
   if i==1:
       p.plotOneAlpha(wl, gPad=cAlpha, opt='PS', color=i)
   else:
       p.plotOneAlpha(wl, gPad=cAlpha, opt='PS', color=i)
   legA.AddEntry(p.getLnPower(wl), '%s (%s)'%(p.LidarRun.DateTime,p.LidarRun.RunNumber))
   i+=1
legA.Draw()
gFakeAlpha.GetXaxis().SetTitle("Alpha")
gFakeAlpha.GetYaxis().SetTitle("Altitude bins (km)")

# Get Tau4 and fill in TGraph
gTau4=ROOT.TGraph(len(pList))
i=0
for run in pList:
    tau4=run.LidarRun.calcTau4()[1]
    runnb=int(run.LidarRun.RunNumber)
    gTau4.SetPoint(i, runnb, tau4)
    print i, runnb, tau4
    i+=1

# Plot Tau4 for the list of runs
cTau4=ROOT.TCanvas("Tau4Can","Tau4",30,50,850,650)
gTau4.SetTitle("Tau4: %s -- %s"%(pList[0].LidarRun.DateTime,pList[-1].LidarRun.DateTime))
gTau4.GetYaxis().SetTitle('Tau4')
gTau4.GetYaxis().SetTitleOffset(1.4)
gTau4.GetYaxis().SetRangeUser(0,2)
gTau4.GetXaxis().SetTitle("Run Number")
gTau4.Draw('AP*')

# Transmission probability
getTransProb(pList[0].LidarRun.calcTau4()[1], pList[-1].LidarRun.calcTau4()[1])
