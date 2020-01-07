#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 20:10:51 2020

@author: isobelmawby
"""

import numpy as np

class MomentumSettings :
    
    def __init__(self, distributionList, meanList, stdDevList, distHistNameList) :
        
        self.dist = distributionList
        self.mean = meanList
        self.stdDev = stdDevList
        self.distHistName = distHistNameList
        
def GetMomentumMag(momentumSettings) :
    
    if momentumSettings.dist == 0 :
        momentumMagList = GetUniformMomentumMag(momentumSettings)
        
    return momentumMagList
    
        
def GetUniformMomentumMag(momentumSettings) :
    
    momentumMag = np.random.uniform(momentumSettings.mean - momentumSettings.stdDev, momentumSettings.mean + momentumSettings.stdDev)
    
    return momentumMag

def GetMomentumVectorListWithinSector(sectorOpeningAngle, particleMomentumList) :
    
    momentumVectorList = []
    # Get random sector axis for particles to be distributed around
    
    sectorAxis = GetRandom2DAxis()
    
    for particleMomentum in particleMomentumList :
        momentumXZVector = GetMomentumVectorWithinSector(sectorAxis, sectorOpeningAngle, particleMomentum) 
        momentumVector =  np.insert(momentumXZVector, 1, 0)
        momentumVectorList.append(momentumVector)
    
    return momentumVectorList
    

def GetMomentumVectorWithinSector(sectorAxis, sectorOpeningAngle, particleMomentum) :
    
    maxAngle = sectorOpeningAngle/2.0
    randomAngle = np.random.uniform(-maxAngle, maxAngle)
    
    c = np.cos(randomAngle)
    s = np.sin(randomAngle)
    rotMatrix = np.array(((c, -s), (s, c)))
    
    rotatedAxis = np.dot(rotMatrix, sectorAxis)
    
    momentumVector = particleMomentum * rotatedAxis
    
    return momentumVector


def GetRandom2DAxis() :
    randomAngle = np.random.uniform(-np.pi, np.pi)
    return (np.cos(randomAngle), np.sin(randomAngle))
