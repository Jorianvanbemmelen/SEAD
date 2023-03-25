#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:33:14 2023

@author: jorian
"""
import numpy as np

print('test')

MTOW = 300000

xcg_w = 10 # [m]
W_w = 0.149*MTOW # [N]

xcg_f = 11 # [m]
W_f = 0.248*MTOW # [N]

xcg_h = 25 # [m]
W_h = 0.018*MTOW # [N]

xcg_v = 25 # [m]
W_v = 0.02*MTOW # [N]

xcg_mg = 12 # [m]
W_mg = 0.035*MTOW #[N]

xcg_ng = 3 # [m]
W_ng = 0.005*MTOW # [N]

xcg_p = 9 # [m]
W_p = 0.103*MTOW # [N]

# Variable weights

seat_pitch = 1.5 # [m]
xcg_s_front = 6 # [m]
W_pass = 1000 # [N]
n = 100

xcg_p = np.zeros(pax_row) 
xcg_p [0]= xcg_s_front

for i in range(1,pax_row):
    xcg_p[i] = xcg_p[i-1]+seat_pitch

xcg_p[:] = (xcg_p[:]-x_lemac)/3.48 
inv_pos_pas = pos_pas[::-1]


xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p)





 
 
 
 
 
 