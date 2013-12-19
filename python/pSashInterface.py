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
        ## pDataInterface to get data for current run
        self.DataInterface=None
        ## Dictionnary to access to data files for current run
        self.DataRunDict={}
        # By-pass for convenience
        if filename is None:            
            self.DataInterface=pDataInterface(runsList=[run])
            self.DataRunDict=self.DataInterface.AllRunsDict[run]
        else:
            self.DataRunDict['LidarFiles']=[filename]
        ## Date and time of the run
        self.DateTime=None
        ## Pointer to the data run header that contains the target information
        self.RunHeader=None
        ## Lidar Sash::DataSet
        self.LidarDataSet=None
        ## Event Sash::EventDataSet
        self.EventsDataSet=None
        ## Run Sash::EventDataSet
        self.RunDataSet=None
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
    ## @brief Open ROOT File and get all Sash::DataSet and HESSArray
    #
    #  Sash::DataSets of interests:
    #  * from camera files: run, events
    #  * from Lidar file: Lidar
    #
    ## @param self
    #  the object instance
    ## @param dtypes
    #  DataSet types to be looked for
    #
    def createSashDataSet(self, dtypes=['run','events','Lidar']):        
        if 'run'in dtypes and self.RunDataSet is None:
            self.createRunDataSets()
        if 'events'in dtypes and self.EventsDataSet is None:
            self.createEventsDataSets()            
        if 'Lidar' in dtypes and self.LidarDataSet is None:
            self.createLidarDataSet()

    ####################################
    ## @brief Create a run Sash::DataSet
    #
    ## @param self
    #  the object instance
    def createRunDataSets(self):
        self.RunDataSet=ROOT.SashFile.EventDataSet("run","run")
        for camFile in self.DataRunDict['CameraFiles']:
            self.RunDataSet.AddFile(camFile)
        try:
            self.RunDataSet.GetEntry(0)
            logger.info('Successfully created the run DataSet')
        except:
            logger.error('Failed to create the run DataSet')
            sys.exit(1)                                                               
                    
    ####################################
    ## @brief Create an events Sash::DataSet
    #  and get here HESSArray and EventHeader as well
    ## @param self
    #  the object instance
    #
    def createEventsDataSets(self):
        self.EventsDataSet=ROOT.SashFile.EventDataSet("events","events")
        for camFile in self.DataRunDict['CameraFiles']:
            self.EventsDataSet.AddFile(camFile)
        try:
            logger.info('Events DataSet ready with %d entries'%self.EventsDataSet.GetEntries())            
        except:
            logger.error('Failed to create the Events DataSet')
            sys.exit(1)
        self.HESSArray=self.EventsDataSet.GetHESSArray()
        self.EventHeader=self.HESSArray.Get(ROOT.Sash.EventHeader())
        self.EventsDataSet.GetEntry(0)


    ####################################
    ## @brief Create a Lidar Sash::DataSet
    #
    ## @param self
    #  the object instance
    def createLidarDataSet(self):
        lidarFile=self.DataRunDict['LidarFiles'][0]                                   
        logger.info("Opening %s"%lidarFile)                                           
        self.LidarRootFile=ROOT.TFile(lidarFile)                                           
        self.LidarDataSet=self.LidarRootFile.Get("Lidar") # Sash DataSet                   
        try:                                                                          
            logger.info('Lidar DataSet ready with %d entries'%self.LidarDataSet.GetEntries())            
        except:                                                                       
            logger.error('Lidar tree does not exist or has no entry... aborting.')    
            sys.exit(1)                                                               
        self.LidarDataSet.GetEntry(0) # not sure it's needed...                       

    ####################################
    ## @brief Open ROOT File and get data into numpy format
    #
    ## @param self
    #  the object instance
    def readLidarFile(self):
        if self.LidarDataSet is None:
            self.createSashDataSet(dtypes=['Lidar'])
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

        ## Number of points of the Lidar data acquisition
        self.LidarNPoints=height.fN
        ## Lidar data Altitude array in km
        self.LidarRawAltitude=numpy.ndarray((self.LidarNPoints),'d')
        ## Lidar data raw signal array for green light
        self.LidarRawWL1=numpy.ndarray((self.LidarNPoints),'d')
        ## Lidar data raw signal array for blue light
        self.LidarRawWL2=numpy.ndarray((self.LidarNPoints),'d')

        for i in range(self.LidarNPoints):
            self.LidarRawAltitude[i]=height[i]
            self.LidarRawWL1[i]=green[i]
            self.LidarRawWL2[i]=blue[i]
            
        logger.info('%s points read'%self.LidarNPoints)
        return 0

    ####################################
    ## @brief Returns Lidar Data
    #
    ## @param self
    #  the object instance

    def getLidarData(self):
        return (self.LidarRawAltitude, self.LidarRawWL1, self.LidarRawWL2)

    ####################################
    ## @brief Return the run header through the related data set
    #
    ## @param self
    #  the object instance

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
    
    ####################################
    ## @brief Returns the run number from the run header
    #
    ## @param self
    #  the object instance

    def getRunNum(self):
        if self.RunNumber is None:
            self.RunNumber=self.getRunHeader().GetRunNum()
        return self.RunNumber

    ####################################
    ## @brief Returns Lidar Data
    #
    ## @param self
    #  the object instance

    def getSummaryString(self):
        summary = str(self.getRunNum())
        summary += ' %15s'%self.getRunHeader().GetTarget()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetTheta().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetPhi().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetBeta().GetDegrees()
        summary += ' %03.02f'%self.getRunHeader().GetTargetPosition().GetLambda().GetDegrees()                        
        self.SummaryString=summary
        return self.SummaryString


    ####################################
    ## @brief Loop over events
    #
    ## @param self
    #  the object instance

    def EventLoop(self):
        self.createSashDataSet()
        for i in range(10):
            logger.info("Loading event %d"%i)
            self.EventsDataSet.GetEntry(i)            
            self.EventHeader.GetTelWData().Print()
            
        logger.info("Event loop done.")

if __name__ == '__main__':
    # Test read via run number
    import sys
    ps2=pSashInterface(67219)
    ps2.createSashDataSet()
    ps2.readLidarFile()
    print ps2.getLidarData()

    ps2.EventLoop()
    
    
#    # Test read via filename
#    import os
#    filename=os.path.join(HESS_DATA_DIR,'run067219/run_067219_Lidar_001.root')
#    ps=pSashInterface(67219, filename)
#    ps.readLidarFile()
#    print ps.getLidarData()
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
