#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:52:53 2020

@author: isobelmawby
"""

import numpy as np

# vertex_dist: Uniform = 0, Gaussian = 1, Histogram = 2 (momentum only)
# vertex_dist_mean and vetex_dist_sd: [x, y, z]
DUNEFDSettings = {
    "vertex_dist": 0,
    "vertex_dist_mean": [0, 0, 600],
    "vertex_dist_sd": [360, 600, 600]
}

ProtoDUNESPSettings = {
    "vertex_dist": 0,
    "vertex_dist_mean": [0, 304, 347],
    "vertex_dist_sd": [375, 299, 347]
}

class VertexSettings :
    def __init__(self, settings_dict) :
        self.dist = settings_dict["vertex_dist"]
        self.mean = settings_dict["vertex_dist_mean"]
        self.stdDev = settings_dict["vertex_dist_sd"]

def GetVertex(vertexSettings) :
    if vertexSettings.dist == 0 :
        vertex = GetUniformDistVertex(vertexSettings)

    return vertex

def GetUniformDistVertex(vertexSettings) :    
    mean_np = np.array(vertexSettings.mean)
    stdDev_np = np.array(vertexSettings.stdDev)
    
    vertex_np = np.random.uniform(mean_np - stdDev_np, mean_np + stdDev_np)

    return tuple(vertex_np)
