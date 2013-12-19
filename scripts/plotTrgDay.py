#!/bin/env python

from pDataInterface import *
from pSashInterface import *
from pTriggerRate   import *

import glob

runsDir=glob.glob(HESS_DATA_DIR+'/run*')
runsDir.sort()

trgList=[]
siList=[]
targetsList=[]

for adir in runsDir[2:]:
    run=int(adir.split('/run0')[1])
    si=pSashInterface(os.path.join(adir,"run_%06d_Lidar_001.root"%run))
    si.readLidarFile()
    si.getData()
    si.getRunHeader()
    #siList.append(si)
#    targetsList.append(str(si.getRunNum())+' '+str(si.RunHeader.GetTarget()))
    targetsList.append(si.getSummaryString())

for adir in runsDir[2:]:
    run=int(adir.split('/run0')[1])
    trg=pTriggerRate(run)
    trg.fillRawTriggerRate()
    trgList.append(trg)    
    
n=len(trgList)
npads=int((n+1)/2)

# plot raw trigger rates
print 'Run Target Theta Phi Beta Lambda\n'
can=ROOT.TCanvas("AllTriggerRates", "All Trigger Rates", 30,50,850,650)
can.Divide(2,npads)
for i in range(n):
    can.cd(i+1)
    trgList[i].plotRawTriggerRate(ROOT.gPad)
    print "Target: ", targetsList[i]

can.cd()
can.Update()

# plot average trigger rates
canAve=ROOT.TCanvas("AverageTriggerRates", "Average Trigger Rates", 30,50,850,650)
gAveTrg=ROOT.TGraph(n)
for i in range(n):
    gAveTrg.SetPoint(i,trgList[i].RunNumber,trgList[i].AverageTriggerRate)
gAveTrg.Draw("AP*")
gAveTrg.SetNameTitle("gAveTrg","Average Raw Trigger Rate")
gAveTrg.GetXaxis().SetTitle("Run Number")
gAveTrg.GetYaxis().SetTitle("Trigger Rate (Hz)")
gAveTrg.GetYaxis().SetRangeUser(0,200)
canAve.Update()
