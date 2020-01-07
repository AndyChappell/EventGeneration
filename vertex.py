#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:52:53 2020

@author: isobelmawby
"""

import numpy as np

class VertexSettings :
    
    def __init__(self, distribution, mean, stdDev) :    
        
        self.dist = distribution
        self.mean = mean
        self.stdDev = stdDev
    

def GetVertex(vertexSettings) :
    
    if vertexSettings.dist == 0 :
        vertex = GetUniformDistVertex(vertexSettings)
        
    return vertex

def GetUniformDistVertex(vertexSettings) :
    
    mean_np = np.array(vertexSettings.mean)
    stdDev_np = np.array(vertexSettings.stdDev)
    
    vertex_np = np.random.uniform(mean_np - stdDev_np, mean_np + stdDev_np)

    return tuple(vertex_np)
