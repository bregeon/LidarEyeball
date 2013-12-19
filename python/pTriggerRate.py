#!/bin/env python

## @file
#  Calculate a simple trigger rate for a HESS nominal science data taking run

import os
import ROOT

from datetime       import datetime

from __logging__    import *
from pDataInterface import *
from pSashInterface import *


####################################
## @brief Class to calculate a simple Trigger rate
#
class pTriggerRate(object):
    ####################################
    ## @brief Constructor
    #
    ## @param self
    #  the object instance
    ## @param runNumber
    #  a runNumber, e.g. 67227
    #  
    def __init__(self, runNumber):
        ## run number
        self.RunNumber=runNumber
        ## "events_tree" TChain of Camera files
        self.EventsChain=None
        ## Histogram of the events time stamp with a 1 s binning
        self.hTrgRate=None
        ## Average trigger rate obtained by a fit of hTrgRate with a constant
        self.AverageTriggerRate=-1
        ## Canvas to plot the histogram of time stamps
        self.TrigCan=None
        ## Interface to get the run data files
        self.DataInterface=pDataInterface(runsList=[runNumber])
        ## Dictionnary with run files information
        self.DataRunDict=self.DataInterface.AllRunsDict[runNumber]

        self.openCamFile()
    
    ####################################
    ## @brief Use a TChain to open HESS ROOT camera files for a given run
    #
    ## @param self
    #  the object instance
    def openCamFile(self):
        ## TChain of events_tree
        self.EventsChain=ROOT.TChain("events_tree")
        for camFile in self.DataRunDict['CameraFiles']:
            self.EventsChain.Add(camFile)

        ## Sash::DataSet of events
        self.DataSet=ROOT.Sash.DataSet("events","events")
        for camFile in self.DataRunDict['CameraFiles']:
            self.DataSet.AddFile(camFile)

        self.nEvents=self.DataSet.GetEntries()
        logger.debug("NEvent %s"%self.nEvents)
        self.tStart=self.DataSet.GetTimeStamp(0).GetTimeDouble()
        logger.debug("tStart %s"%self.tStart)
        self.tStop=self.DataSet.GetTimeStamp(int(self.nEvents-1)).GetTimeDouble()
        logger.debug("tStop %s"%self.tStop)
         

    ####################################
    ## @brief Create a histogram of time stamps with 1 s bins
    #  and fit it with a constant
    #
    ## @param self
    #  the object instance
    def fillRawTriggerRate(self):
        logger.info('Fill raw trigger rate histogram for run %06d'%self.RunNumber)
        hName="hTrgRate_%d"%self.RunNumber
        hTitle="Trigger Rate for run %d"%self.RunNumber
        self.hTrgRate=ROOT.TH1F(hName, hTitle, 4000,-2000,1900)
        self.hTrgRate.GetXaxis().SetTitle("Seconds from run start")
        self.hTrgRate.GetYaxis().SetTitle("Raw Trigger rate (Hz)")         
        self.EventsChain.Project(hName,"fTime+1e-9*fNanosec-%f"%self.tStart)
        fit=self.hTrgRate.Fit("pol0","QS")
        fitparams=fit.Get().GetParams()
        self.hTrgRate.SetMaximum(250)
        self.AverageTriggerRate=fitparams[0]
        logger.info("Run %s Average Trigger Rate: %.02f"%\
                     (self.RunNumber,self.AverageTriggerRate))
    
    ####################################
    ## @brief Create a histogram of time stamps with 1 s bins
    #  and fit it with a constant
    #
    ## @param self
    #  the object instance
    def averageCorrectedTriggerRate(self):
        logger.info('Estimate the averaged corrected trigger rate for run %06d'%self.RunNumber)
        # create raw trigger rate histogram if it does not exist
        if self.hTrgRate is None:
            self.fillRawTriggerRate()
        
        self.LidarSashInterface=pSashInterface(self.RunNumber)
        self.LidarSashInterface.readLidarFile()
        logger.info(self.LidarSashInterface.getSummaryString())
        self.RunHeader=self.LidarSashInterface.getRunHeader()
        theta=self.RunHeader.GetTargetPosition().GetTheta().GetDegrees()
        cor=ROOT.TMath.Cos(theta*ROOT.TMath.DegToRad())
        self.AverageCorrectedTriggerRate=self.AverageTriggerRate*cor
        logger.info("Run %s Average Corrected Trigger Rate: %.02f"%\
                     (self.RunNumber,self.AverageCorrectedTriggerRate))

    ####################################
    ## @brief Plot histogram of the trigger rate in a TPad
    #
    ## @param self
    #  the object instance
    ## @param gPad
    #  a TCanvas TPad to plot the histogram in
    #
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
    c=ROOT.TCanvas("Trigger", "Trigger", 30,50,850,650)
    trg.plotRawTriggerRate(ROOT.gPad)
    trg.averageCorrectedTriggerRate()
    
