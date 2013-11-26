#!/bin/env python

## @file
#  An interface to get Lidar data from a Sash DataSet.
#  This is specific to HESS data as ROOT files and depens upon
#  a large part of the HESS software.

import os
import ROOT
import numpy
from datetime import datetime

from __logging__        import *

####################################
## @brief Class to interface to Sash:DataSet
#
class pSashInterface(object):
    ####################################
    ## @brief Constructor for the interface
    #
    ## @param self
    #  the object instance
    ## @param filename
    #  a HESS ROOT file name with Lidar data in a Sash:DataSet
    def __init__(self, filename):
        self.Directory=directory
        self.FileName=filename
        self.RunNumber=None
        self.DateTime=None
        self.RunHeader=None        
        # Start processing
        self.__loadLibs()

    ####################################
    ## @brief Load dependencies as HESS ROOT libraries
    #
    ## @param self
    #  the object instance
    def __loadLibs(self):     
        # First check if HESSROOT is defined... no hope otherwise.
        if not os.environ.has_key('HESSROOT'):
            logger.error('$HESSROOT is not set, HESS software is needed for this code to run.')
            logger.error('Aborting...')
            sys.exit(1)
        # To read a LidarEvent, actually loads plenty of other libraries including
        # Sash:DataSet
        rc=ROOT.gSystem.Load("libatmosphere")
        if rc!=0:
            logger.error('libatmosphere.so could not be loaded.\nAborting...')
            sys.exit(1)
        logger.info('Successfuly loaded HESS software libraries.')


    ####################################
    ## @brief Open ROOT File and get data into numpy format
    #
    ## @param self
    #  the object instance
    def readLidarFile(self):
        logger.info("Opening %s"%self.FilePath)
        self.RootFile=ROOT.TFile(self.FilePath)
        self.LidarDataSet=self.RootFile.Get("Lidar") # Sash DataSet
        logger.info('Found %s entries'%self.LidarDataSet.GetEntries())
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

    def getData(self):
        return (self.RawAltitude, self.RawWL1, self.RawWL2)

    def getRunHeader(self):
        if self.RunHeader is None:
            dList=ps.LidarDataSet.GetListOfRelatedSets()
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
    
if __name__ == '__main__':
    # Do something
    import os
    ROOT_DATA_DIR='/home/bregeon/Hess/data/run067217/'
    filename=os.path.join(ROOT_DATA_DIR,'run_067217_Lidar_001.root')
    ps=pSashInterface(filename)
    ps.readFile()
    print ps.getData()
    
    # Various tests
    ps.getRunHeader()
    print "Run Type: ",ps.RunHeader.GetRunType()
    print "Tels in Run: ", ps.RunHeader.GetNTelsInRun()
    print "Tels in Trigger: ",ps.RunHeader.GetMinTelInTrigger()
    print "Trigger pattern: ", ps.RunHeader.GetTriggerPattern()

    print "Target: ", ps.RunHeader.GetTarget()
    print "Target Postion Beta: %.02f"%ps.RunHeader.GetTargetPosition().GetBeta().GetDegrees()
    print "Target Postion Lambda: %.02f"%ps.RunHeader.GetTargetPosition().GetLambda().GetDegrees()
    print "Target Postion Phi: %.02f"%ps.RunHeader.GetTargetPosition().GetPhi().GetDegrees()
    print "Target Postion Theta: %.02f"%ps.RunHeader.GetTargetPosition().GetTheta().GetDegrees()
    
    # in principe HESSArray gives access to everything else
    # run is a Sash::DataSet
    #array=run.GetHESSArray()
    #array.GetRADecJ2000System()
    
