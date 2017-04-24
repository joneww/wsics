#from __future__ import division
import numpy as np
import math

def rgb2hsd(rgb):
    B = rgb[:, :, 0]
    G = rgb[:, :, 1]
    R = rgb[:, :, 2]

    DB = - (np.log((B + 1.0) / 257.0))
    DG = - (np.log((G + 1.0) / 257.0))
    DR = - (np.log((R + 1.0) / 257.0))

    D = (DR + DB + DG) / 3.0
    Cx = DR / D - 1
    Cy = (DG - DB) / (D * math.sqrt(3))
    #hsd =  np.array([Cx,Cy,D])
    hsd = np.zeros(np.shape(rgb))
    hsd[:, :, 0] = Cx
    hsd[:, :, 1] = Cy
    hsd[:, :, 2] = D

    return hsd


def hsd2rgb(hsd):
# hsd color space to rgb color space
#input:(Cx, Cy, D) in the hsd color space
#output:rgb

    Cx = hsd[:, :, 0]
    Cy = hsd[:, :, 1]
    D = hsd[:, :, 2]
    Dr = (Cx + 1) * D
    Dg = ((Cy * D * math.sqrt(3)) + (3 * D - Dr)) / 2
    Db = 3 * D - Dr - Dg

    b = np.exp(-Db) * 257.0 - 1
    g = np.exp(-Dg) * 257.0 - 1
    r = np.exp(-Dr) * 257.0 - 1

    #rgb = np.array([b,g,r])
    rgb = np.zeros(np.shape(hsd))

    rgb[:, :, 0] = b
    rgb[:, :, 1] = g
    rgb[:, :, 2] = r

    return rgb

##############################
#input rgb of a pixel,output hsd of the same pixel

def pixel_rgb2hsd(rgb):
    B = rgb[0]
    G = rgb[1]
    R = rgb[2]

    DB = - (np.log((B + 1.0) / 257.0))
    DG = - (np.log((G + 1.0) / 257.0))
    DR = - (np.log((R + 1.0) / 257.0))

    D = (DR + DB + DG) / 3.0
    Cx = DR / D - 1
    Cy = (DG - DB) / (D * math.sqrt(3))
    #hsd =  np.array([Cx,Cy,D])
    hsd = np.zeros(np.shape(rgb))
    hsd[0] = Cx
    hsd[1] = Cy
    hsd[2] = D

    return hsd
