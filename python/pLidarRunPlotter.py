#!/bin/env python

## @file
#  The analysis plotter class
# 

from pDataInterface import *
import pLidarRun

import ROOT


####################################
## @brief Class to plot LIDAR run data
#
class pLidarRunPlotter(object):
    ####################################
    ## @brief Constructor for a pulsar source
    #
    ## @param self
    #  the object instance
    ## @param lidarRun 
    #  a pLidarRun object
    def __init__(self, lidarRun=None):
        print 'New plotter for run %s'%lidarRun.RunNumber
        self.LidarRun=lidarRun
        #self.fillAll()
        self.fillLnPowerGraphs()
        self.fillBinnedLnPowerGraphs()
        self.fillPowerGraphs()
        self.fillBinnedPowerGraphs()
        #self.fillKlettGraphs()
               
    def fillRawData(self):
        # TGraphs first    
        # WL1
        self.gRawWL1=ROOT.TGraph(self.LidarRun.NPoints,\
                                 self.LidarRun.RawWL1, self.LidarRun.RawAltitude)
        self.gRawWL1.SetNameTitle('gRawWL1_%s'%self.LidarRun.RunNumber, 'Raw WL1 %s'%self.LidarRun.RunNumber)
        self.gRawWL1.GetXaxis().SetTitle("Raw Signal (V)")
        self.gRawWL1.GetYaxis().SetTitle("Altitude(km)")
        # WL2
        self.gRawWL2=ROOT.TGraph(self.LidarRun.NPoints,\
                                 self.LidarRun.RawWL2, self.LidarRun.RawAltitude)
        self.gRawWL2.SetNameTitle('gRawWL2_%s'%self.LidarRun.RunNumber, 'Raw WL2%s'%self.LidarRun.RunNumber)
        self.gRawWL2.GetXaxis().SetTitle("Raw Signal (V)")
        self.gRawWL2.GetYaxis().SetTitle("Altitude(km)")
        
        # A histogram to understand better the "raw" signal
        self.hRawWL1=ROOT.TH1F("hRawWL1","Raw WL1 (V)",50000,-5,0)
        self.hRawWL2=ROOT.TH1F("hRawWL2","Raw WL2 (V)",50000,-5,0)
        for (v1,v2) in zip(self.LidarRun.RawWL1,self.LidarRun.RawWL2):
            self.hRawWL1.Fill(v1)
            self.hRawWL2.Fill(v2)
    
    def fillReducedData(self):
        # WL1
        self.gReducedWL1=ROOT.TGraph(self.LidarRun.NData,\
                                     self.LidarRun.WL1, self.LidarRun.Alt)
        self.gReducedWL1.SetNameTitle('gWL1_%s'%self.LidarRun.RunNumber, 'Reduced WL1%s'%self.LidarRun.RunNumber)
        self.gReducedWL1.GetXaxis().SetTitle("Reduced Signal (V)")
        self.gReducedWL1.GetYaxis().SetTitle("Altitude(km)")
        # WL2
        self.gReducedWL2=ROOT.TGraph(self.LidarRun.NData,\
                                     self.LidarRun.WL1, self.LidarRun.Alt)
        self.gReducedWL2.SetNameTitle('gWL2_%s'%self.LidarRun.RunNumber, 'Reduced WL2%s'%self.LidarRun.RunNumber)
        self.gReducedWL2.GetXaxis().SetTitle("Reduced Signal (V)")
        self.gReducedWL2.GetYaxis().SetTitle("Altitude(km)")

    def fillPowerGraphs(self):
        # WL1
        self.gPowerWL1=ROOT.TGraph(self.LidarRun.NData,\
                                   self.LidarRun.PW1, self.LidarRun.Alt)
        self.gPowerWL1.SetNameTitle('gPW1_%s'%self.LidarRun.RunNumber, 'Power WL1 %s'%self.LidarRun.RunNumber)
        self.gPowerWL1.GetXaxis().SetTitle("Power V*R^2 (V.km^2)")
        self.gPowerWL1.GetYaxis().SetTitle("Altitude(km)")
        # WL2
        self.gPowerWL2=ROOT.TGraph(self.LidarRun.NData,\
                                   self.LidarRun.PW2, self.LidarRun.Alt)
        self.gPowerWL2.SetNameTitle('gPW2_%s'%self.LidarRun.RunNumber, 'Power WL2%s'%self.LidarRun.RunNumber)
        self.gPowerWL2.GetXaxis().SetTitle("Power (V*R^2)")
        self.gPowerWL2.GetYaxis().SetTitle("Altitude(km)")

    def fillLnPowerGraphs(self):
        # WL1
        self.gLnPowerWL1=ROOT.TGraph(self.LidarRun.NData, self.LidarRun.LnPW1, self.LidarRun.Alt)
        self.gLnPowerWL1.SetNameTitle('gLnPW1_%s'%self.LidarRun.RunNumber, 'Ln(Power WL1 %s)'%self.LidarRun.RunNumber)
        self.gLnPowerWL1.GetXaxis().SetTitle("Ln(Power V*R^2)")
        self.gLnPowerWL1.GetYaxis().SetTitle("Altitude(km)")
        self.gLnPowerWL1.GetXaxis().SetRangeUser(-4,-1)
        # WL2
        self.gLnPowerWL2=ROOT.TGraph(self.LidarRun.NData, self.LidarRun.LnPW2, self.LidarRun.Alt)
        self.gLnPowerWL2.SetNameTitle('gLnPW2_%s'%self.LidarRun.RunNumber, 'Ln(Power WL2 %s)'%self.LidarRun.RunNumber)
        self.gLnPowerWL2.GetXaxis().SetTitle("Ln(Power V*R^2)")
        self.gLnPowerWL2.GetYaxis().SetTitle("Altitude(km)")
        self.gLnPowerWL2.GetXaxis().SetRangeUser(-4,0)

    def fillBinnedPowerGraphs(self):
        # Should use TGraphAsymmErrors
        # Power WL1
        self.gBinnedPowerWL1=ROOT.TGraph(self.LidarRun.NBins,\
                                         self.LidarRun.BinnedPW1, self.LidarRun.BinsAltCenter)
        self.gBinnedPowerWL1.SetNameTitle('gBinnedPW1_%s'%self.LidarRun.RunNumber, 'Binned (Power WL1 %s)'%self.LidarRun.RunNumber)
        self.gBinnedPowerWL1.GetXaxis().SetTitle("Power V*R^2")
        self.gBinnedPowerWL1.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedPowerWL1.GetXaxis().SetRangeUser(-4,-1)
        self.gBinnedPowerWL1.SetMarkerStyle(25)

        # Power WL2
        self.gBinnedPowerWL2=ROOT.TGraph(self.LidarRun.NBins,\
                                         self.LidarRun.BinnedPW2, self.LidarRun.BinsAltCenter)
        self.gBinnedPowerWL2.SetNameTitle('gBinnedPW2_%s'%self.LidarRun.RunNumber, 'Binned (Power WL2 %s)'%self.LidarRun.RunNumber)
        self.gBinnedPowerWL2.GetXaxis().SetTitle("Power V*R^2")
        self.gBinnedPowerWL2.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedPowerWL2.GetXaxis().SetRangeUser(-4,-1)
        self.gBinnedPowerWL2.SetMarkerStyle(25)

    def fillBinnedLnPowerGraphs(self):
        # Ln Power WL1
        self.gBinnedLnPowerWL1=ROOT.TGraph(self.LidarRun.NBins,\
                                           self.LidarRun.BinnedLnPW1, self.LidarRun.BinsAltCenter)
        self.gBinnedLnPowerWL1.SetNameTitle('gBinnedLnPW1_%s'%self.LidarRun.RunNumber, 'Binned Ln(Power WL1 %s)'%self.LidarRun.RunNumber)
        self.gBinnedLnPowerWL1.GetXaxis().SetTitle("Ln(Power V*R^2)")
        self.gBinnedLnPowerWL1.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedLnPowerWL1.GetXaxis().SetRangeUser(-4,-1)
        self.gBinnedLnPowerWL1.SetMarkerStyle(24)
        # Ln Power WL2
        self.gBinnedLnPowerWL2=ROOT.TGraph(self.LidarRun.NBins,\
                                           self.LidarRun.BinnedLnPW2, self.LidarRun.BinsAltCenter)
        self.gBinnedLnPowerWL2.SetNameTitle('gBinnedLnPW2_%s'%self.LidarRun.RunNumber, 'Binned Ln(Power WL2 %s)'%self.LidarRun.RunNumber)
        self.gBinnedLnPowerWL2.GetXaxis().SetTitle("Ln(Power V*R^2)")
        self.gBinnedLnPowerWL2.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedLnPowerWL2.GetXaxis().SetRangeUser(-4,-1)
        self.gBinnedLnPowerWL2.SetMarkerStyle(24)


    def fillKlettGraphs(self):
        # Should use TGraphAsymmErrors
        # Alpha WL1
        self.gBinnedAlphaPW1=ROOT.TGraph(self.LidarRun.AlphaNBins,\
                                         self.LidarRun.BinnedAlphaPW1, self.LidarRun.BinsAltCenter)
        self.gBinnedAlphaPW1.SetNameTitle('BinnedAlphaPW1_%s'%self.LidarRun.RunNumber, 'Klett Alpha WL1 %s'%self.LidarRun.RunNumber)
        self.gBinnedAlphaPW1.GetXaxis().SetTitle("Alpha")
        self.gBinnedAlphaPW1.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedAlphaPW1.GetXaxis().SetRangeUser(1e-2,1)
        self.gBinnedAlphaPW1.SetMarkerStyle(4)

        # Alpha WL2
        self.gBinnedAlphaPW2=ROOT.TGraph(self.LidarRun.AlphaNBins,\
                                         self.LidarRun.BinnedAlphaPW2, self.LidarRun.BinsAltCenter)
        self.gBinnedAlphaPW2.SetNameTitle('BinnedAlphaPW2_%s'%self.LidarRun.RunNumber, 'Klett Alpha WL2 %s'%self.LidarRun.RunNumber)
        self.gBinnedAlphaPW2.GetXaxis().SetTitle("Alpha")
        self.gBinnedAlphaPW2.GetYaxis().SetTitle("Altitude bins (km)")
        self.gBinnedAlphaPW2.GetXaxis().SetRangeUser(1e-2,1)
        self.gBinnedAlphaPW2.SetMarkerStyle(4)


    def fillAll(self):
        self.fillRawData()
        self.fillReducedData()
        self.fillPowerGraphs()
        self.fillLnPowerGraphs()
        self.fillBinnedPowerGraphs()
        self.fillBinnedLnPowerGraphs()
        self.fillKlettGraphs()
        
        
    def plotAll(self):
        self.fillAll()
        self.MainCanvas=ROOT.TCanvas('LidarDataCan_%s'%self.LidarRun.RunNumber,\
                                     'Lidar Data for run %s'%self.LidarRun.RunNumber,\
                                     30,50,850,650)
        self.MainCanvas.Divide(2,4)
        self.MainCanvas.cd(1)
        self.gRawWL1.Draw('AP')
        self.MainCanvas.cd(2)
        self.gRawWL2.Draw('AP')
        self.MainCanvas.cd(3)
        self.gReducedWL1.Draw('AP')
        self.MainCanvas.cd(4)
        self.gReducedWL2.Draw('AP')
        self.MainCanvas.cd(5)
        self.gPowerWL1.Draw('AP')
        self.MainCanvas.cd(6)
        self.gPowerWL2.Draw('AP')
        self.MainCanvas.cd(7)
        self.gLnPowerWL1.Draw('AP')
        self.MainCanvas.cd(8)
        self.gLnPowerWL2.Draw('AP')


    def getAlpha(self, wl=1):
        if wl==1:
            return self.gBinnedAlphaPW1   
        elif wl==2:
            return self.gBinnedAlphaPW2
        else:
            print 'unknown graph gBinnedAlphaPW%s'%wl
            return None

    def getLnPower(self, wl=1):
        if wl==1:
            return self.gLnPowerWL1   
        elif wl==2:
            return self.gLnPowerWL2
        else:
            print 'unknown graph gLnPowerWL%s'%wl
            return None

    def getBinnedLnPower(self, wl=1):
        if wl==1:
            return self.gBinnedLnPowerWL1   
        elif wl==2:
            return self.gBinnedLnPowerWL2
        else:
            print 'unknown graph gBinnedLnPowerWL%s'%wl
            return None
            
    def plotBothPower(self, gPad=None):
        if gPad is None:
            self.PWCanvas=ROOT.TCanvas('PowerCan_%s'%self.LidarRun.RunNumber,\
                                         'Power for run %s'%self.LidarRun.RunNumber,\
                                         30,50,850,650)
        self.gPowerWL1.Draw('AP')
        self.gPowerWL2.Draw('PS')
        self.gPowerWL2.SetMarkerColor(2)
        self.gBinnedPowerWL1.Draw('PS')
        self.gBinnedPowerWL2.Draw('PS')
        self.gBinnedPowerWL2.SetMarkerColor(2)

    def plotBothLnPower(self, gPad=None):
        if gPad is None:
            self.LnPWCanvas=ROOT.TCanvas('LnPowerCan_%s'%self.LidarRun.RunNumber,\
                                         'Ln(Power) for run %s'%self.LidarRun.RunNumber,\
                                         30,50,850,650)
        self.gLnPowerWL1.Draw('AP')
        self.gLnPowerWL2.Draw('PS')
        self.gLnPowerWL2.SetMarkerColor(2)
        self.gBinnedLnPowerWL1.Draw('PS')
        self.gBinnedLnPowerWL2.Draw('PS')
        self.gBinnedLnPowerWL2.SetMarkerColor(2)


    def plotBothAlpha(self, gPad=None):
        if gPad is None:
            self.AlphaCanvas=ROOT.TCanvas('AlphaCan_%s'%self.LidarRun.RunNumber,\
                                         'Power for run %s'%self.LidarRun.RunNumber,\
                                         30,50,850,650)
        self.gBinnedAlphaPW1.Draw('AP')
        self.gBinnedAlphaPW2.Draw('PS')
        self.gBinnedAlphaPW2.SetMarkerColor(2)
        

    def plotOneLnPower(self, wl=1, gPad=None, opt='', color=1):
        if gPad is None:
            self.LnPWCanvas=ROOT.TCanvas('LnPowerCan_%s'%self.LidarRun.RunNumber,\
                                         'Ln(Power) for run %s'%self.LidarRun.RunNumber,\
                                         30,50,850,650)
        else:
            gPad.cd()
        pw=self.getLnPower(wl)
        pw.Draw(opt)
        pw.SetMarkerColor(color)
        pw.SetLineColor(color)


    def plotOneAlpha(self, wl=1, gPad=None, opt='AP', color=1):
        if gPad is None:
            self.gAlphaCanvas=ROOT.TCanvas('AlphaCan_%s'%self.LidarRun.RunNumber,\
                                         'Alpha for run %s'%self.LidarRun.RunNumber,\
                                         30,50,850,650)
        else:
            gPad.cd()
        alpha=self.getAlpha(wl)
        alpha.Draw(opt)
        alpha.SetMarkerColor(color)
        alpha.SetLineColor(color)


if __name__ == '__main__':
    import os    
#    run=pLidarRun.pLidarRun('data/run_065160_Lidar_001.root.txt',process=True, nBins=100)
#    run=pLidarRun.pLidarRun('alldata/run_069377_Lidar_001.root.txt',process=True, nBins=100)
    run=pLidarRun.pLidarRun(os.path.join(HESS_DATA_DIR,'run067217/run_067217_Lidar_001.root'),process=True, nBins=100)
    plotter=pLidarRunPlotter(run)
    #plotter.plotAll()
    
    c=ROOT.TCanvas()
    c.Divide(3)
    c.cd(1)
    plotter.plotBothLnPower(ROOT.gPad)
    c.cd(2)
    plotter.plotBothPower(ROOT.gPad)
    
    #run Klett
    plotter.LidarRun.run_Klett()
    plotter.fillKlettGraphs()
    c.cd(3)
    plotter.plotBothAlpha(ROOT.gPad)
    c.Update()
    
