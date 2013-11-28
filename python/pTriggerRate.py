#!/bin/env python

## @file
#  Calculate a simple trigger rate for a HESS nominal science data taking run

import os
import ROOT

from datetime       import datetime

from __logging__    import *
from pDataInterface import *


####################################
## @brief Class to calculate a simple Trigger rate
#
class pTriggerRate(object):
    ####################################
    ## @brief Constructor for the interface
    #
    ## @param self
    #  the object instance
    ## @param runNumber
    #  a runNumber that will use to 
    def __init__(self, runNumber):
        self.RunNumber=runNumber
        self.EventsChain=None
        self.openCamFile()
    
    def openCamFile(self):
         # Data are in another ROOT File - fix readFile above
         #data=ROOT.Sash.DataSet("/home/bregeon/Hess/data/run067217/run_067217_Camera_001.root")
         self.EventsChain=ROOT.TChain("events_tree")
         self.EventsChain.Add(os.path.join(HESS_DATA_DIR,"run%06d/run_%06d_Camera_*.root"%\
                                     (self.RunNumber, self.RunNumber)))
         

    def fillRawTriggerRate(self):
         hName="hTrgRate_%d"%self.RunNumber
         hTitle="Trigger Rate for Tel_%d"%self.RunNumber
         self.hTrgRate=ROOT.TH1F(hName, hTitle, 2000,-100,1900)
         self.hTrgRate.GetXaxis().SetTitle("Seconds from run start")
         self.hTrgRate.GetYaxis().SetTitle("Raw Trigger rate (Hz)")
         tStart=self.EventsChain.GetMinimum("fTime")
         if tStart < 10:
             tStart=self.EventsChain.GetMaximum("fTime")-1800
         self.EventsChain.Project(hName,"fTime-%f"%tStart)
         fit=self.hTrgRate.Fit("pol0","QS")
         fitparams=fit.Get().GetParams()
         self.AverageTriggerRate=fitparams[0]
         logger.info("Run %s Average Trigger Rate: %.02f"%\
                     (self.RunNumber,self.AverageTriggerRate))
    
    def plotRawTriggerRate(self, gPad=None):
         if gPad is None:
             self.TrigCan=ROOT.TCanvas('TrigerCan_%s'%self.RunNumber,\
                                         'Raw Trigger Rate for run %s'%self.RunNumber,\
                                         30,50,850,650)
         else:
             gPad.cd()
         self.hTrgRate.Draw()
                                         

if __name__ == '__main__':
    trg=pTriggerRate(67221)
    trg.fillRawTriggerRate()
    trg2=pTriggerRate(67227)
    trg2.fillRawTriggerRate()
    c=ROOT.TCanvas("Trigger", "Trigger", 30,50,850,650)
    c.Divide(1,2)
    c.cd(1)
    trg.plotRawTriggerRate(ROOT.gPad)
    c.cd(2)
    trg2.plotRawTriggerRate(ROOT.gPad)
    c.cd()
