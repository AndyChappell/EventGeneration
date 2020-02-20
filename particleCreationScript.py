#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:26:56 2020

@author: isobelmawby

Python Script to create 'neutrino-like' events

Particles are created such that they originate from the same vertex with momentum vectors lying 
within a sector of a circle defined by their respective momenta and a given 'sectorOpeningAngle'

"""
import vertex
import momentum
import math
import numpy as np

# SETTTINGS

#Events to be created
numberOfEvents = 500

# OutputFileName
eventsFileName = "MCParticleData.txt"

# PDG codes of particles to create
particleList = [13]

# Masses in GeV
PDGToMassDict = {13 : 0.106, 2212 : 0.938}

# sectorOpeningAngle defined to be the angle between boundaries of the sector
# Angle in degrees
#sectorOpeningAngleDeg  = 10
#sectorOpeningAngle = np.radians(sectorOpeningAngle)

# Opening angle between two particles, given in degrees
# openingAngleDeg = 40
# openingAngle = np.radians(openingAngleDeg)

# Theta0YZ angles, input in degrees
theta0YZListDeg = [0]
theta0YZList = np.radians(theta0YZListDeg)
deltaTheta0YZListDeg = [90]
deltaTheta0YZList = np.radians(deltaTheta0YZListDeg)

# Theta0XZ angles, input in degrees
theta0XZListDeg = [0]
theta0XZList = np.radians(theta0XZListDeg)
deltaTheta0XZListDeg = [90]
deltaTheta0XZList = np.radians(deltaTheta0XZListDeg)

# Distributions to assign the vertex and particle momentum magnitudes
# Uniform = 0, Gaussian = 1, Histogram = 2 (momentum only)
# Momentum lists must be equal in length to the particleList
vertexDist = 0
vertexDistMean = [0, 304, 347]           # [x, y, z]   #DUNE FD [0, 0, 600]         #ProtoDUNE [0, 304, 347]
vertexDistStdDev = [375, 299, 347]     # [x, y, z]     #DUNE FD [360, 600, 600]     #ProtoDUNE [375, 299, 347]

vertexSettings = vertex.VertexSettings(vertexDist, vertexDistMean, vertexDistStdDev)

momentumDist = [1]                 
momentumDistMean = [1]         #DUNEFD 2.5 for Muons, 1 for Protons (Uniform)  #ProtoDUNE 1 (Gaussian)
momentumDistStdDev = [1]       #DUNEFD 2.5 for Muons, 1 for Protons (Uniform)  #ProtoDUNE 0.05 (Gaussian)
momentumDistHistName = [""] 

particleMomentumSettings = []
for dist, mean, stdDev, hist in zip(momentumDist, momentumDistMean, momentumDistStdDev, momentumDistHistName) :
    particleMomentumSettings.append(momentum.MomentumSettings(dist, mean, stdDev, hist))


# CODE IMPLEMENTATION

# Open HEP event file
eventFile = open(eventsFileName, 'w') 

eventNumber = 0
for event in range(numberOfEvents) :
    # Get vertex  
    interactionVertex = vertex.GetVertex(vertexSettings)

    # Get particle momentum magnitude list    
    particleMomentumMagList = []
    for momentumSettings in particleMomentumSettings :
        particleMomentumMagList.append(momentum.GetMomentumMag(momentumSettings))

    # Get particle energy list
    particleEnergyList = []
    for PDG, p in zip(particleList, particleMomentumMagList) :
        particleEnergyList.append(math.sqrt(math.pow(p, 2) + math.pow(PDGToMassDict[PDG], 2)))

    # Get momentum vectors of particles 
    # particleMomentumVectorList = momentum.GetRandom3DMomentumVectorList(particleMomentumMagList)
    particleMomentumVectorList = momentum.Get3DMomentumVectorListWithAngles(particleMomentumMagList, theta0YZList, deltaTheta0YZList, theta0XZList, deltaTheta0XZList)
    #particleMomentumVectorList = momentum.Get3DMomentumVectorsWithRandomOpeningAngle(particleMomentumMagList)

    # Write event as HEP event format
    firstLine = str(eventNumber) + " " + str(len(particleList))
    eventFile.write(firstLine)
    eventFile.write("\n")


    for PDG, momentumVec, energy in zip(particleList, particleMomentumVectorList, particleEnergyList) :
    
       secondLine = "1 " + str(PDG) + " 0 0 0 0 " + str(momentumVec[0]) + " " + str(momentumVec[1]) + " " + str(momentumVec[2]) + " " + str(energy) + " " + str(PDGToMassDict[PDG]) + " " + str(interactionVertex[0]) + " " + str(interactionVertex[1]) + " " + str(interactionVertex[2]) + " " + "0.0" 
       eventFile.write(secondLine)
       eventFile.write("\n")

    eventNumber += 1







