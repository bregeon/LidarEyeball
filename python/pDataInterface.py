## @file
#  An interface to get data from a directory
#  or a run number
#  To be seen how general that will be

import os
import glob

from __logging__        import *

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
    def __init__(self, directory='', runNumber=-1):
        self.Directory=directory
        self.RunNumber=runNumber


    ####################################
    ## @brief Hash a directory to find known data files
    #
    ## @param self
    #  the object instance
    def __hashDir__(self):
        logger.info('Hashing input directory for HESS ROOT files:\n%s'%self.Directory)
        rootFiles=glob.glob(os.path.join(self.Directory,'*.root'))
        txtFiles=glob.glob(os.path.join(self.Directory,'*.txt'))
        logger.debug(rootFiles)
        logger.debug(txtFiles)        


if __name__ == '__main__':
    di=pDataInterface(os.path.join(HESS_DATA_DIR,'run067217'))
    di.__hashDir__()
    
    
