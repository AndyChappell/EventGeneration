from ROOT import TFile, TH3D
import numpy as np

def SelectParticleMomentumFromHist() :
    # Open file containing particle momentum distribution
    file = TFile("threeD.root", "READ")

    # Retrieve momentum distribution
    hist = file.Get("threeDHist")

    # Normalise histogram so that bin height represent probabilities
    hist.Scale(1./hist.Integral())

    # Pick a random number [0, 1) to use to select bin in momentum histogram 
    randomNum = np.random.uniform(0,1)
    
    # Find associated bin in momentum histogram
    cumulativeProb = 0
    momentumXBinIndex = 0
    momentumYBinIndex = 0
    momentumZBinIndex = 0
    found = False
    for xBin in range(1, hist.GetXaxis().GetNbins() + 1, 1) :
        if found :
            break
        for yBin in range(1, hist.GetYaxis().GetNbins() + 1, 1) :
            if found :
                break
            for zBin in range(1, hist.GetZaxis().GetNbins() + 1, 1) :
                cumulativeProb += hist.GetBinContent(xBin, yBin, zBin)
                print("Bin Content: ", hist.GetBinContent(xBin, yBin, zBin))
                print("Cumulative Prob: ", cumulativeProb)

                if(cumulativeProb > randomNum) :
                    momentumXBinIndex = xBin
                    momentumYBinIndex = yBin
                    momentumZBinIndex = zBin
                    found = True
                    break;

    # Select random momentum within this bin
    xMomentum = np.random.uniform(hist.GetXaxis().GetBinLowEdge(momentumXBinIndex), hist.GetXaxis().GetBinLowEdge(momentumXBinIndex) + hist.GetXaxis().GetBinWidth(momentumXBinIndex))
    yMomentum = np.random.uniform(hist.GetYaxis().GetBinLowEdge(momentumYBinIndex), hist.GetYaxis().GetBinLowEdge(momentumYBinIndex) + hist.GetYaxis().GetBinWidth(momentumYBinIndex))
    zMomentum = np.random.uniform(hist.GetZaxis().GetBinLowEdge(momentumZBinIndex), hist.GetZaxis().GetBinLowEdge(momentumZBinIndex) + hist.GetZaxis().GetBinWidth(momentumZBinIndex))

    print("X Momentum: ", xMomentum)
    print("Y Momentum: ", yMomentum)
    print("Z Momentum: ", zMomentum)

