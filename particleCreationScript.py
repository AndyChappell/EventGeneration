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

# Events to be created
numberOfEvents = 10

# OutputFileName
eventsFileName = "MuonProtonEvents.txt"

# PDG codes of particles to create
particleList = [14, 2212]

# Masses in GeV
PDGToMassDict = {14 : 0.106, 2212 : 0.938}

# sectorOpeningAngle defined to be the angle between boundaries of the sector
# Angle in degrees
sectorOpeningAngle  = 10
sectorOpeningAngleRad = np.radians(sectorOpeningAngle)

# Distributions to assign the vertex and particle momentum magnitudes
# Uniform = 0, Gaussian = 1, Histogram = 2 (momentum only)
# Momentum lists must be equal in length to the particleList
vertexDist = 0
vertexDistMean = [0, 0, 0]       # [x, y, z]
vertexDistStdDev = [4, 4, 4]     # [x, y, z]

vertexSettings = vertex.VertexSettings(vertexDist, vertexDistMean, vertexDistStdDev)
      
momentumDist = [0, 0]
momentumDistMean = [0, 0] 
momentumDistStdDev = [3, 100]
momentumDistHistName = ["", ""] 

particleMomentumSettings = []
for dist, mean, stdDev, hist in zip(momentumDist, momentumDistMean, momentumDistStdDev, momentumDistHistName) :
    particleMomentumSettings.append(momentum.MomentumSettings(dist, mean, stdDev, hist))


# CODE IMPLEMENTATION

# Open HEP event file
eventFile = open(eventsFileName, 'w') 

eventNumber = 0
for event in range() :
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
    particleMomentumVectorList = momentum.GetMomentumVectorListWithinSector(sectorOpeningAngle, particleMomentumMagList)

    # Write event as HEP event format
    firstLine = str(eventNumber) + str(len(particleList))
    eventFile.write(firstLine)

    for PDG, momentumVec, energy in zip(particleList, particleMomentumVectorList, particleEnergyList)
       secondLine = "1 " + str(PDG) + " 0 0 0 0 " + str(momentumVec[0]) + " " + str(momentumVec[1]) + " " + momentumVec[2] + " " + str(energy) + " " + str(PDGToMassDict[PDG]) + " " + str(interactionVertex[0]) + " " + str(interactionVertex[1]) + " " + str(interactionVertex[2]) + " " + "0" 
       eventFile.write(secondLine)
    eventNumber += 1

   
    print("Particles", particleList)
    print("Vertex: ", interactionVertex)
    print("Momentum Magnitudes: ", particleMomentumMagList)
    print("Energy: ", particleEnergy)
    print("Momentum Vectors:", particleMomentumVectorList)




















