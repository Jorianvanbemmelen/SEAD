

import numpy as np
import control
from math import *
import matplotlib.pyplot as plt


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

xcg_cf = 5 # [m]
xcg_cb = 23 # [m]

seat_pitch = 1.0 # [m]
W_pass = 800 # [N]

# x_c.g. calculation

xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p)
W_fixed = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p

def cargoback(W_fixed, xcgOEW):
    W_old = W_fixed
    xcg_old = xcgOEW
    W_cargob = 5000 # [N]
    W_cargof = 4000 # [N]
    xcg_cargob = 26 # [m]
    xcg_cargof = 4 # [m]
    xcg_carback = [xcg_old]
    W_carback = [W_old]
    xcg_carb = (W_old*xcg_old + W_cargob*xcg_cargob)/(W_old + W_cargob)
    W_carb = W_old + W_cargob
    xcg_carback.append(xcg_carb)
    W_carback.append(W_carb)
    xcg_carf = (W_carb*xcg_carb + W_cargof*xcg_cargof)/(W_carb + W_cargof)
    W_carf = W_carb + W_cargof
    xcg_carback.append(xcg_carf)
    W_carback.append(W_carf)
    return xcg_carback, W_carback

xcg_carback, W_carback = cargoback(W_fixed, xcgOEW)

def cargofront(W_fixed, xcgOEW):
    W_old = W_fixed
    xcg_old = xcgOEW
    W_cargob = 5000  # [N]
    W_cargof = 4000  # [N]
    xcg_cargob = 26  # [m]
    xcg_cargof = 4  # [m]
    xcg_carfront = [xcg_old]
    W_carfront = [W_old]
    xcg_carf = (W_old*xcg_old + W_cargof*xcg_cargof)/(W_old + W_cargof)
    W_carf = W_old + W_cargof
    xcg_carfront.append(xcg_carf)
    W_carfront.append(W_carf)
    xcg_carb = (W_carf*xcg_carf + W_cargob*xcg_cargob)/(W_carf + W_cargob)
    W_carb = W_carf + W_cargob
    xcg_carfront.append(xcg_carb)
    W_carfront.append(W_carb)
    return xcg_carfront, W_carfront

xcg_carfront, W_carfront = cargofront(W_fixed, xcgOEW)

def passforwardwindow(W_carback, xcg_carback, W_pass, seat_pitch):
    # print(W_carback)
    W_old = W_carback[2]
    xcg_old = xcg_carback[2]
    xcg_p = [6]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] + seat_pitch)
        xcg_new = (W_old*xcg_old + W_pass*xcg_p[i])/(W_old + W_pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_pass)
        W_old = W_old + W_pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passforward, W_passforward = passforwardwindow(W_carback, xcg_carback, W_pass, seat_pitch)

def passbackwindow(W_carback, xcg_carback, W_pass, seat_pitch):
    W_old = W_carback[2]
    xcg_old = xcg_carback[2]
    xcg_p = [24]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] - seat_pitch)
        xcg_new = (W_old*xcg_old + W_pass*xcg_p[i])/(W_old + W_pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_pass)
        W_old = W_old + W_pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passback, W_passback = passbackwindow(W_carback, xcg_carback, W_pass, seat_pitch)


def passforwardaisle(W_passforward, xcg_passforward, W_pass, seat_pitch):
    W_old = W_passforward[17]
    xcg_old = xcg_passforward[17]
    xcg_p = [6]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] + seat_pitch)
        xcg_new = (W_old*xcg_old + W_pass*xcg_p[i])/(W_old + W_pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_pass)
        W_old = W_old + W_pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passforwardaisle, W_passforwardaisle = passforwardaisle(W_passforward, xcg_passforward, W_pass, seat_pitch)

def passbackaisle(W_passforward, xcg_passforward, W_pass, seat_pitch):
    W_old = W_passforward[17]
    xcg_old = xcg_passforward[17]
    xcg_p = [24]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] - seat_pitch)
        xcg_new = (W_old*xcg_old + W_pass*xcg_p[i])/(W_old + W_pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_pass)
        W_old = W_old + W_pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passbackaisle, W_passbackaisle = passbackaisle(W_passforward, xcg_passforward, W_pass, seat_pitch)

def fuel(xcg_passbackaisle, W_passbackaisle):
    W_old = W_passbackaisle[17]
    xcg_old = xcg_passbackaisle[17]
    xcg_fuel = 11 # [m]
    W_fuel = 20000 # [N]
    W_fueltotal = [W_old]
    xcg_fueltotal = [xcg_old]
    xcg_total = (W_passbackaisle[17]*xcg_passbackaisle[17] + W_fuel*xcg_fuel)/(W_passbackaisle[17] + W_fuel)
    W_total = W_passbackaisle[17] + W_fuel
    xcg_fueltotal.append(xcg_fuel)
    W_fueltotal.append(W_total)
    return xcg_fueltotal, W_fueltotal

xcg_fueltotal, W_fueltotal = fuel(xcg_passbackaisle, W_passbackaisle)

plt.plot(xcg_carfront, W_carfront)
plt.plot(xcg_carback, W_carback)
plt.plot(xcg_passforward, W_passforward)
plt.plot(xcg_passback, W_passback)
plt.plot(xcg_passforwardaisle, W_passforwardaisle)
plt.plot(xcg_passbackaisle, W_passbackaisle)
plt.plot(xcg_fueltotal, W_fueltotal)
plt.show()

