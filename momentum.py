#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 20:10:51 2020

@author: isobelmawby
"""

import numpy as np
import math

DUNEFDSettings = {
    "p_dist": 0,
    "p_dist_mean": {11: 0.1, 13: 2.5, 2212: 1},
    "p_dist_sd": {11: 0.1, 13: 2.5, 2212: 1},
    "p_dist_histname": "" 
}

ProtoDUNESPSettings = {
    "p_dist": 1,
    "p_dist_mean": {11: 0.1, 13: 1, 2212: 1},
    "p_dist_sd": {11: 0.1, 13: 1, 2212: 1},  # 0.05
    "p_dist_histname": "" 
}

class MomentumSettings :
    def __init__(self, pid, settings_dict) : 
        self.dist = settings_dict["p_dist"]
        self.mean = settings_dict["p_dist_mean"][pid]
        self.stdDev = settings_dict["p_dist_sd"][pid]
        self.distHistName = settings_dict["p_dist_histname"] 
        
######################################################################################################

# Fill the particle momentum MAGNITUDE list according to distribution option
def GetMomentumMag(momentumSettings) :
    if momentumSettings.dist == 0 :
        momentumMagList = GetUniformMomentumMag(momentumSettings)
        return momentumMagList
    if momentumSettings.dist == 1 :
        momentumMagList = GetGaussianMomentumMag(momentumSettings)
        return momentumMagList

    

# Fill the particle momentum MAGNITUDE list following a uniform distribution 
# Uniform distribution parameters given in MomentumSettings
def GetUniformMomentumMag(momentumSettings) :
    momentumMag = np.random.uniform(momentumSettings.mean - momentumSettings.stdDev, momentumSettings.mean + momentumSettings.stdDev)
    return momentumMag


# Fill the particle momentum MAGNITUDE list following a gaussian distribution 
# Gaussian distribution parameters given in MomentumSettings
def GetGaussianMomentumMag(momentumSettings) :
    momentumMag = np.random.normal(momentumSettings.mean, momentumSettings.stdDev)
    return momentumMag


######################################################################################################

# Fill momentum VECTOR list such that all momentum vectors lie within a sector
# Opening angle (angle between sector boundaries) passed 
def GetMomentumVectorListWithinSector(sectorOpeningAngle, particleMomentumList) :
    momentumVectorList = []

    # Get random sector axis for particles to be distributed around
    sectorAxis = GetRandom2DAxis()
    
    for particleMomentum in particleMomentumList :
        momentumXZVector = GetMomentumVectorWithinSector(sectorAxis, sectorOpeningAngle, particleMomentum) 
        momentumVector =  np.insert(momentumXZVector, 1, 0)
        momentumVectorList.append(momentumVector)    
    return momentumVectorList
    

# Calculate a momentum VECTOR that lies within the sector
def GetMomentumVectorWithinSector(sectorAxis, sectorOpeningAngle, particleMomentum) :
    maxAngle = sectorOpeningAngle/2.0
    randomAngle = np.random.uniform(-maxAngle, maxAngle)
    
    c = np.cos(randomAngle)
    s = np.sin(randomAngle)
    rotMatrix = np.array(((c, -s), (s, c)))
    
    rotatedAxis = np.dot(rotMatrix, sectorAxis)
    
    momentumVector = particleMomentum * rotatedAxis
    return momentumVector

######################################################################################################


# Obtain a random axis in 2D space 
# (ATTN - CAN POINT IN -VE Z)
def GetRandom2DAxis() :
    randomAngle = np.random.uniform(-np.pi, np.pi)
    return (np.cos(randomAngle), np.sin(randomAngle))


# Fill momentum VECTOR list with random 3D mometum VECTORS 
# (ATTN - CANNOT POINT IN -VE Z)
def GetRandom3DMomentumVectorList(particleMomentumMagList) :
    particleMomentumVecList = []
    for momentumMag in particleMomentumMagList :
        particleMomentumVecList.append(GetRandom3DMomentumVector(momentumMag))
    return particleMomentumVecList


# Calculate a random 3D VECTOR given a momentum MAGNITUDE
# DOES NOT PREVENT POINTING IN NEGATIVE DIRECTIONS
def GetRandom3DMomentumVector(momentumMag) :

    theta = np.random.uniform(0, np.pi)
    phi = np.random.uniform(0, 2*np.pi)

    pX = momentumMag*np.cos(phi)*np.sin(theta)
    pY = momentumMag*np.sin(phi)*np.sin(theta)
    pZ = momentumMag*np.cos(theta) 

    return [pX, pY, pZ]


######################################################################################################


def Get3DMomentumVectorListWithAngles(momentumMagList, angles) :
    momentumVecList = []
    zipped_vals = zip(momentumMagList, angles.theta0YZList, angles.deltaTheta0YZList,
        angles.theta0XZList, angles.deltaTheta0XZList)
    for momentumMag, theta0YZ, delta0YZ, theta0XZ, delta0XZ in zipped_vals :
        momentumVec = Get3DMomentumVectorWithAngles(momentumMag, theta0YZ,
            delta0YZ, theta0XZ, delta0XZ)
        momentumVecList.append(momentumVec)
    return momentumVecList


def Get3DMomentumVectorWithAngles(momentumMag, theta0YZ, delta0YZ, theta0XZ, delta0XZ) :

    randomTheta0XZ = np.random.uniform(theta0XZ - delta0XZ, theta0XZ + delta0XZ)
    randomTheta0YZ = np.random.uniform(theta0YZ - delta0YZ, theta0YZ + delta0YZ)

    pX = momentumMag*np.cos(randomTheta0YZ)*np.sin(randomTheta0XZ)
    pY = momentumMag*np.sin(randomTheta0YZ) 
    pZ = momentumMag*np.cos(randomTheta0YZ)*np.cos(randomTheta0XZ)
    return (pX, pY, pZ) 


######################################################################################################


# Will fill a two particle event
def Get3DMomentumVectorsWithRandomOpeningAngle(momentumMagList) :

    isForward = False
    rnd3DAxis = None
    vecOnCircle = None

    while not isForward :

        openingAngle = np.random.uniform(-np.pi, np.pi)

        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2*np.pi)

        rnd3DAxis = [np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)]

        rotatedTheta = theta + openingAngle

        vecOnCircle = [np.sin(rotatedTheta)*np.cos(phi), np.sin(rotatedTheta)*np.sin(phi), np.cos(rotatedTheta)]
  
        rotationAngle = np.random.uniform(0.0, 2.0*np.pi)

        c = np.cos(rotationAngle)
        s = np.sin(rotationAngle)
 
        vecRotated = np.dot(vecOnCircle, c) + np.cross(rnd3DAxis, vecOnCircle)*s + np.dot(np.dot(rnd3DAxis, np.dot(rnd3DAxis, vecOnCircle)), 1 - c)

        if (rnd3DAxis[2] + vecRotated[2]) > 0 :
            isForward = True    

    return [np.dot(rnd3DAxis, momentumMagList[0]), np.dot(vecRotated, momentumMagList[1])]


######################################################################################################
