#!/bin/env python
import glob
import os
from pLidarRun import pLidarRun
from toolBox import *

DATA_DIR='/home/bregeon/CTA/Lidar'

runList=glob.glob('%s/alldata/run*.root.txt'%DATA_DIR)

#runList=[]
#runList.append(os.path.join(DATA_DIR,'alldata/run_065238_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_065240_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_065241_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_065242_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_069054_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_069436_Lidar_001.root.txt'))
#runList.append(os.path.join(DATA_DIR,'alldata/run_070085_Lidar_001.root.txt'))

runList.sort()

sDict=['LIDAR_RUN_DICT={\n']
for run in runList:
    p=pLidarRun(run, process=True, nBins=100)
    p.calcTau4()
    sDict.append(p.dumpToDict())
sDict.append('}')

open('LidarRunDict.py','w').writelines(sDict)

