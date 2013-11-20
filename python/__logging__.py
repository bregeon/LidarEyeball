#!/usr/bin/env python
# Stolen from
#__source__   = "$Source: /nfs/slac/g/glast/ground/cvs/users/lbaldini/MeritUtils/python/__logging__.py,v $"
#__author__   = "Luca Baldini (luca.baldini@pi.infn.it)"

import logging
import sys

logger = logging.getLogger('resample')
logger.setLevel(logging.DEBUG)

# Terminal setting.
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleFormatter = logging.Formatter(">>> %(message)s")
consoleHandler.setFormatter(consoleFormatter)
logger.addHandler(consoleHandler)

