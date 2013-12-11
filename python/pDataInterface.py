## @file
#  An interface to get data from a directory
#  or a run number, locally.

import os
import glob

from __logging__ import *

## Default data directory on mmy laptop
HESS_DATA_DIR='/data/Hess/data/'

####################################
## @brief Class to interface to data input
#
class pDataInterface(object):

    ####################################
    ## @brief Constructor for the interface
    #
    ## @param self
    #  the object instance
    ## @param directory
    #  a directory with data files
    def __init__(self, runsList=[], directory=HESS_DATA_DIR):
        self.RunsList=runsList
        self.Directory=directory
        self.AllRunsDir=[]
        self.AllRunsDict={}
        self.FailedRunsList=[]
        self.__hashDataDir__()


    ####################################
    ## @brief Hash a directory to get HESS runs
    #   Also remove the one for which either Lidar or Camera data
    #   are not available
    #
    ## @param self
    #  the object instance
    def __hashDataDir__(self):
        logger.info('Hashing input directory for HESS runs:\n%s'%self.Directory)
        self.AllRunsDir=glob.glob(HESS_DATA_DIR+'/run*')
        for adir in self.AllRunsDir:
            run=int(adir.split('/run0')[1])
            self.AllRunsDict[run]={}
            self.AllRunsDict[run]['DataDir']=adir
        self.__checkRuns__()
        
    ####################################
    ## @brief Check that required runs are available
    #
    ## @param self
    #  the object instance
    def __checkRuns__(self):
        for run in self.RunsList:
            runRC=self.__hashRunDir__(run)
            if runRC==1:
                logger.warning('Run %s is not available. Removed from dictionnary.'%run)
                self.RunsList.remove(run)
                self.FailedRunsList.append(run)
            elif runRC>=1:
                self.RunsList.remove(run)
                self.FailedRunsList.append(run)                
                self.AllRunsDict.pop(run)
                logger.warning('Data not available for run %s. Removed from list and dictionnary.'%run)
        logger.info("Failed runs list: %s"%self.FailedRunsList)        
                
    ####################################
    ## @brief Hash a directory to find known data files
    #
    ## @param self
    #  the object instance
    ## @param run
    #  a run number
    def __hashRunDir__(self, run):
        if run not in self.AllRunsDict.keys():
           return 1
        logger.debug('Hashing input directory for HESS runs directory:\n%s'%self.AllRunsDict[run]['DataDir'])
        self.AllRunsDict[run]['LidarFiles']=glob.glob(os.path.join(self.AllRunsDict[run]['DataDir'],'run_%06d_Lidar_*.root'%run))
        self.AllRunsDict[run]['CameraFiles']=glob.glob(os.path.join(self.AllRunsDict[run]['DataDir'],'run_%06d_Camera_*.root'%run))        
        self.AllRunsDict[run]['TxtFiles']=glob.glob(os.path.join(self.AllRunsDict[run]['DataDir'],'*.txt'))
        self.AllRunsDict[run]['FitsFiles']=glob.glob(os.path.join(self.AllRunsDict[run]['DataDir'],'*.fits'))
        for key in self.AllRunsDict[run].keys():
            if key not in ['DataDir']:
                self.AllRunsDict[run][key].sort()
            if len(self.AllRunsDict[run]['LidarFiles'])>0 and\
               len(self.AllRunsDict[run]['CameraFiles'])>0:
                return 0
            else:           
                return 2


if __name__ == '__main__':
    # Unit Test 
    di=pDataInterface(runsList=[67227,67229, 34])
    print(di.AllRunsDict.keys())
    print(di.RunsList)
    print(di.FailedRunsList)
    
