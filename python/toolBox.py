## @file
#  A set of Tools to be used in the LidarEyeball package
# 

import ROOT

import math
from datetime import datetime, timedelta

from LidarRunDict import LIDAR_RUN_DICT

####################################
## @brief Simple estimate of the transmission
#  probability and its variation given 2 Tau4
#
## @param tau1
#  Tau4 at the beginning of the night
## @param tau2
#  Tau4 at the end of the night
def getTransProb(tau1,tau2):
    p1=math.exp(-2*tau1)
    p2=math.exp(-2*tau2)
    diff=(p2-p1)/p1
    print('Transmission probability from %.02f to %.02f'%(p1,p2))
    print('Variation %.02f'%(diff))
    return p1,p2,diff

####################################
## @brief Get run numbers for a given night,
#  using the run dictionnary LIDAR_RUN_DICT
#
## @param Date
#  start date and time as a string'%Y-%m-%d %H:%M:%S'
def getRunsForNight(Date):
    runNumbers=[]
    date1=datetime.strptime(Date,'%Y-%m-%d %H:%M:%S')
    date2=date1+timedelta(hours=16)
    for key,val in LIDAR_RUN_DICT.items():
        runDate=datetime.strptime(val['DateTime'],'%Y-%m-%d %H:%M:%S')
        if runDate>=date1 and runDate<=date2 and val['IsGood']:
            runNumbers.append(key)   
    runNumbers.sort()
    return runNumbers

####################################
## @brief Get run numbers for a given period,
#  using the run dictionnary LIDAR_RUN_DICT
#
## @param Date1
#  start date as a string'%Y-%m-%d %H:%M:%S'
## @param Date2
#  stop date as a string'%Y-%m-%d %H:%M:%S'

def getRunsFromTo(Date1,Date2):
    runNumbers=[]
    date1=datetime.strptime(Date1,'%Y-%m-%d %H:%M:%S')
    date2=datetime.strptime(Date2,'%Y-%m-%d %H:%M:%S')
    for key,val in LIDAR_RUN_DICT.items():
        runDate=datetime.strptime(val['DateTime'],'%Y-%m-%d %H:%M:%S')
        if runDate>=date1 and runDate<=date2:
            runNumbers.append(key)
    runNumbers.sort()
    return runNumbers

