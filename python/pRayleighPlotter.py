#!/bin/env python

## @file
#  A class to plot pRayleigh objects
# 

import ROOT

import pRayleigh

####################################
## @brief Class to plot pRayleigh objects
#
class pRayleighPlotter(object):

    ####################################
    ## @brief Constructor 
    #
    ## @param self
    #  the object instance
    ## @param rayleigh
    #  a pRayleigh object
    
    def __init__(self, rayleigh):
        self.Rayleigh=rayleigh
        self.createTF1()
        self.createRevTF1()

    def createTF1(self):
      self.TF1 = ROOT.TF1("Rayleigh_%d"%self.Rayleigh.Lambda,self.Rayleigh.getRayleighForTF1, 0.1 ,25.,2)
      #ray.SetParameters(costheta, Lambda)
      self.TF1.GetXaxis().SetTitle('Altitude (km)')
      self.TF1.GetYaxis().SetTitle('Extinction')
      return self.TF1
        
    def plotRayleigh(self, wl=1, gPad=None, opt='AP', color=1):
        if gPad is None:
            self.RayleighCan=ROOT.TCanvas('RayleighCan','Rayleigh',30,50,650,850)
        else:
            gPad.cd()
        self.TF1.Draw()
        return self.RayleighCan

    def getReverseRayleigh(self, rayleigh):
        # gives back the altitude for a given rayleigh absorption value
        # I should really invert the function analytically
        return self.TF1.GetX(rayleigh,0.1,30)  
              
    def getReverseRayleighForTF1(self, x, par):
        return self.getReverseRayleigh(x[0])

    def createRevTF1(self):
        self.RevTF1=ROOT.TF1("RevRayleigh_%d"%self.Rayleigh.Lambda,self.getReverseRayleighForTF1,0.0001, 0.1, 2)
        self.RevTF1.GetXaxis().SetTitle('Extinction')
        self.RevTF1.GetYaxis().SetTitle('Altitude (km)')
        return self.RevTF1

    def plotRevRayleigh(self, wl=1, gPad=None, opt='AP', color=1):
        if gPad is None:
            self.RevRayleighCan=ROOT.TCanvas('RevRayleighCan','RevRayleigh',30,50,650,850)
        else:
            gPad.cd()
        self.RevTF1.Draw()
        return self.RevRayleighCan
#
#    def plotRevRayleigh():
#        revrayBlue=revRayTF1(1, 355.)
#        revrayGreen=revRayTF1(1,532.)
#        c=ROOT.TCanvas('RevRayleighCan','RevRayleigh',30,50,850,850)
#        c.Divide(1,2)
#        c.cd(1)
#        revrayBlue.Draw()
#        c.cd(2)
#        revrayGreen.Draw()
#        c.Update()
#        return c,revrayGreen, revrayBlue

if __name__ == '__main__':
#    rayBlue=rayleighTF1(1, 355.)
#    rayGreen=rayleighTF1(1,532.)
#    c=ROOT.TCanvas('RayleighCan','Rayleigh',30,50,850,850)
#    c.Divide(1,2)
#    c.cd(1)
#    rayBlue.Draw()
#    c.cd(2)
#    rayGreen.Draw()
#    return c,rayGreen, rayBlue
   r=pRayleigh.pRayleigh(1,532)
   p= pRayleighPlotter(r)
   p.plotRayleigh()
   p.plotRevRayleigh()
   
