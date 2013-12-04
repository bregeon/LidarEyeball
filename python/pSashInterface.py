#!/bin/env python

## @file
#  An interface to get Lidar data from a Sash DataSet.
#  This is specific to HESS data as ROOT files and depens upon
#  a large part of the HESS software.

import os
import ROOT
import numpy
from datetime       import datetime

from __logging__    import *
from pDataInterface import *

####################################
## @brief Class to interface to Sash:DataSet
#
class pSashInterface(object):
    ####################################
    ## @brief Constructor for the interface
    #
    ## @param self
    #  the object instance
    ## @param run
    #  a HESS data run number
    def __init__(self, run, filename=None):
        ## A HESS data run number
        self.RunNumber=run
        ## Data interface to get data for a given run
        self.DataRunDict={}
        if filename is None:            
            self.DataInterface=pDataInterface(runsList=[run])
            self.DataRunDict=self.DataInterface.AllRunsDict[run]
        else:
            self.DataRunDict['LidarFiles']=[filename]
        ## Date and time of the run
        self.DateTime=None
        ## Pointer to the data run header that contains the target information
        self.RunHeader=None        
        # Start processing
        self.__loadLibs__()

    ####################################
    ## @brief Load dependencies as HESS ROOT libraries
    #
    ## @param self
    #  the object instance
    def __loadLibs__(self):     
        # Check if library is already available
        if 'libatmosphere.so' in ROOT.gSystem.GetLibraries():
            return 0
        # Check if HESSROOT is defined... no hope otherwise.
        if not os.environ.has_key('HESSROOT'):
            logger.error('$HESSROOT is not set, HESS software is needed for this code to run.')
            logger.error('Aborting...')
            sys.exit(1)
        # To read a LidarEvent, actually loads plenty of other libraries including
        # Sash:DataSet
        if ROOT.gSystem.Load("libatmosphere")!=0:
            logger.error('libatmosphere.so could not be loaded.\nAborting...')
            sys.exit(1)
        logger.info('Successfuly loaded HESS software libraries.')
        return 0

    ####################################
    ## @brief Open ROOT File and get data into numpy format
    #
    ## @param self
    #  the object instance
    def createSashDataSet(self):
        self.DataSet=ROOT.Sash.DataSet("run","run")
        self.DataSet.AddFile(self.DataRunDict['LidarFiles'][0])
        for camFile in self.DataRunDict['CameraFiles']:
            self.DataSet.AddFile(camFile)
        
        return self.DataSet
        
    ####################################
    ## @brief Open ROOT File and get data into numpy format
    #
    ## @param self
    #  the object instance
    def readLidarFile(self):
        lidarFile=self.DataRunDict['LidarFiles'][0]
        logger.info("Opening %s"%lidarFile)
        self.RootFile=ROOT.TFile(lidarFile)
        self.LidarDataSet=self.RootFile.Get("Lidar") # Sash DataSet
        try:
            logger.info('Found %s entries'%self.LidarDataSet.GetEntries())
        except:
            logger.error('Lidar tree does not exist or has no entry... aborting.')
            sys.exit(2)
            
        self.LidarDataSet.GetEntry(0) # not sure it's needed...        
        # Need to convert to datetime
        utc=self.LidarDataSet.GetTimeStamp(0).GetUTC()
        self.DateTime=utc
        self.DateTimeString='%s %02d:%02d:%02d'%(utc.GetDate(), utc.GetHour(),\
                     utc.GetMinute(), utc.GetSecond())
        logger.info("Run DateTime: %s"%self.DateTimeString)
        # Get Lidar tree and get branched to numpy arrays
        self.LidarTree=self.LidarDataSet.GetTree()
        green=self.LidarTree.LidarEvent.GetSignal355()
        blue=self.LidarTree.LidarEvent.GetSignal532()
        height=self.LidarTree.LidarEvent.GetRange()
        self.NPoints=height.fN

        self.RawAltitude=numpy.ndarray((self.NPoints),'d')
        self.RawWL1=numpy.ndarray((self.NPoints),'d')
        self.RawWL2=numpy.ndarray((self.NPoints),'d')

        for i in range(self.NPoints):
            self.RawAltitude[i]=height[i]
            self.RawWL1[i]=green[i]
            self.RawWL2[i]=blue[i]
            
        logger.info('%s points read'%self.NPoints)
        return 0

    def getData(self):
        return (self.RawAltitude, self.RawWL1, self.RawWL2)

    def getRunHeader(self):
        if self.RunHeader is None:
            dList=self.LidarDataSet.GetListOfRelatedSets()
            for d in dList:
                if d.GetName()=='run':
                    run=d
            runtree=run.GetTree()
            runtree.GetEntry(0)        
            self.RunHeader=runtree.RunHeader        
        return self.RunHeader
    
    def getRunNum(self):
        if self.RunNumber is None:
            self.RunNumber=self.getRunHeader().GetRunNum()
        return self.RunNumber

    def getSummaryString(self):
        summary = str(self.getRunNum())
        summary += ' %15s'%self.getRunHeader().GetTarget()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetTheta().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetPhi().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetBeta().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetLambda().GetDegrees()                        
        self.SummaryString=summary
        return self.SummaryString

if __name__ == '__main__':
    # Test read via run number
    import sys
    ps2=pSashInterface(67219)
    ps2.readLidarFile()
    print ps2.getData()
    ps2.createSashDataSet()
    
    
#    # Test read via filename
#    import os
#    filename=os.path.join(HESS_DATA_DIR,'run067219/run_067219_Lidar_001.root')
#    ps=pSashInterface(67219, filename)
#    ps.readLidarFile()
#    print ps.getData()
#        
#    # Header tests
#    ps.getRunHeader()
#    print "Run Type: ",ps.RunHeader.GetRunType()
#    print "Tels in Run: ", ps.RunHeader.GetNTelsInRun()
#    print "Tels in Trigger: ",ps.RunHeader.GetMinTelInTrigger()
#    print "Trigger pattern: ", ps.RunHeader.GetTriggerPattern()
#
#    print "Target: ", ps.RunHeader.GetTarget()
#    print "Target Postion Beta: %.02f"%ps.RunHeader.GetTargetPosition().GetBeta().GetDegrees()
#    print "Target Postion Lambda: %.02f"%ps.RunHeader.GetTargetPosition().GetLambda().GetDegrees()
#    print "Target Postion Phi: %.02f"%ps.RunHeader.GetTargetPosition().GetPhi().GetDegrees()
#    print "Target Postion Theta: %.02f"%ps.RunHeader.GetTargetPosition().GetTheta().GetDegrees()
#    
#    # in principe HESSArray gives access to everything else
#    # run is a Sash::DataSet
#    #array=run.GetHESSArray()
#    #array.GetRADecJ2000System()
#    
