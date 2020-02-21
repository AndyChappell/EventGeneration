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

# Masses in GeV
PDGToMassDict = {13 : 0.106, 2212 : 0.938}

class Angles:
    def __init__(self):
        self.theta0YZList = np.zeros(1)
        self.deltaTheta0YZList = np.zeros(1)
        self.theta0XZList = np.zeros(1)
        self.deltaTheta0XZList = np.zeros(1)

def generate(args):
    # SETTTINGS

    #Events to be created
    numberOfEvents = args.num_events

    # OutputFileName
    eventsFileName = args.events_filename

    # PDG codes of particles to create
    particleList = [args.pid]

    # sectorOpeningAngle defined to be the angle between boundaries of the sector
    # Angle in degrees
    #sectorOpeningAngle = np.radians(10)

    # Opening angle between two particles, given in degrees
    # openingAngle = np.radians(40)

    # Theta0YZ angles and Theta0XZ angles, input in degrees
    angles = Angles()
    angles.theta0YZList = np.radians([0])
    angles.deltaTheta0YZList = np.radians([90])
    angles.theta0XZList = np.radians([0])
    angles.deltaTheta0XZList = np.radians([90])

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
        particleMomentumVectorList = momentum.Get3DMomentumVectorListWithAngles(particleMomentumMagList, angles)
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a HEP style event text file")
    parser.add_argument("--events-filename", "-f", type=str, required=False,
        default="MCParticleData.txt", help="The name of the output events file")
    parser.add_argument("--num-events", "-n", type=int, required=False, default=5,
        help="The number of events to create")
    parser.add_argument("--pid", type=int, required=False, default=13,
        help="The PDG code for the particle to be created")
    args = parser.parse_args()

    np.random.seed(42)
    generate(args)
