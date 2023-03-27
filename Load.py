

import numpy as np
import control
from math import *
import matplotlib.pyplot as plt


MTOW = 23000 # [kg]
MAC = 2.5 # [m]
l_leadingedge = 11.23 # [m]

# Wing group, wing, main landing gear, propulsion

xcg_w = 14 # [m]
W_w = 0.149*MTOW # [kg]

xcg_mg = xcg_w + 3 # [m]
W_mg = 0.035*MTOW #[kg]

xcg_p = xcg_w - 1 # [m]
W_p = 0.103*MTOW # [kg]

W_wgroup = W_w + W_mg + W_p
xcg_wgroup = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p)/(W_w + W_mg + W_p)
xcg_wgroup_mac = (xcg_wgroup - l_leadingedge)/MAC

# Fuselage group; fuselage, horizontal tailplane, vertical tailplane, nose gear

xcg_f = 15 # [m]
W_f = 0.248*MTOW # [kg]

xcg_h = 25 # [m]
W_h = 0.018*MTOW # [kg]

xcg_v = 25 # [m]
W_v = 0.02*MTOW # [kg]

xcg_ng = 3 # [m]
W_ng = 0.005*MTOW # [kg]

W_fgegroup = W_f + W_h + W_v + W_ng
xcg_fgroup = (xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng)/(W_f + W_h + W_v + W_ng)
xcg_fgroup_mac = (xcg_fgroup - l_leadingedge)/MAC

# Variable weights

xcg_cf = 5 # [m]
xcg_cb = 22 # [m]

seat_pitch = 1 # [m]
W_2pass = 160 # [kg]

# x_c.g. calculation

xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p)
xcgOEWmac = (xcgOEW - l_leadingedge)/MAC
W_fixed = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p

def cargoback(W_fixed, xcgOEW):
    W_old = W_fixed
    xcg_old = xcgOEWmac
    W_cargob = 1000 # [kg]
    W_cargof = 1000 # [kg]
    xcg_cargob = (26 - l_leadingedge)/MAC # [m]
    xcg_cargof = (4 - l_leadingedge)/MAC # [m]
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
    xcg_old = xcgOEWmac
    W_cargob = 1000  # [N]
    W_cargof = 1000  # [N]
    xcg_cargob = (26 - l_leadingedge)/MAC  # [m]
    xcg_cargof = (4 - l_leadingedge)/MAC  # [m]
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

def passforwardwindow(W_carback, xcg_carback, W_2pass, seat_pitch):
    # print(W_carback)
    W_old = W_carback[2]
    xcg_old = xcg_carback[2]
    xcg_p = [(6 - l_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] + seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passforward, W_passforward = passforwardwindow(W_carback, xcg_carback, W_2pass, seat_pitch)

def passbackwindow(W_carback, xcg_carback, W_2pass, seat_pitch):
    W_old = W_carback[2]
    xcg_old = xcg_carback[2]
    xcg_p = [(24 - l_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passback, W_passback = passbackwindow(W_carback, xcg_carback, W_2pass, seat_pitch)

def passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
    W_old = W_passforward[17]
    xcg_old = xcg_passforward[17]
    xcg_p = [(6 - l_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] + seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passforwardaisle, W_passforwardaisle = passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)

def passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
    W_old = W_passforward[17]
    xcg_old = xcg_passforward[17]
    xcg_p = [(24 - l_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 18):
        xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passbackaisle, W_passbackaisle = passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)

def fuel(xcg_passbackaisle, W_passbackaisle):
    W_old = W_passbackaisle[17]
    xcg_old = xcg_passbackaisle[17]
    xcg_fuel = (xcg_w - l_leadingedge)/MAC # [m]
    W_fuel = 5000 # [kg]
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


# Stick-fixed static stability diagram

# CLah = 1.1
# CLAh = 1.2
# deda = 1.1
# lh = 10
# c = 2.5
# Vh = 100
# V = 110
# xac = 5
#
# ShS = xcg_fueltotal[1]/(CLah*(1-deda)*lh*(Vh/V)*(Vh/V)/(CLAh*c)) - (xac-0.05)/(CLah*(1-deda)*lh*(Vh/V)*(Vh/V)/(CLAh*c))
#
# plt.plot(xcg_fueltotal, (ShS))
# plt.show()



