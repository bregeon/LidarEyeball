## @file
#  An interface to get data from a directory
#  or a run number
#  To be seen how general that will be

import os

from __logging__        import *

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
    def __init__(self, directory='', runNumber=-1):
        self.Directory=diretory
        self.RunNumber=runNumber


    ####################################
    ## @brief Hash a directory to find known data files
    #
    ## @param self
    #  the object instance
    def __hashDir(self):
        logger.info('Hashing input directory for HESS ROOT files: '%self.Directory)
        rootFiles=glob.glob(os.path.join(self.Directory,'*.root')
        txtFiles=glob.glob(os.path.join(self.Directory,'*.txt')
