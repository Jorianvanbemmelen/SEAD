
import numpy as np
import control
from math import *
import matplotlib.pyplot as plt


MTOW = 23000  # [kg]
MAC = 2.5  # [m]
x_leadingedge = 11.23  # [m]

# Wing group, wing, main landing gear, propulsion

xcg_w = 14  # [m] Wing
W_w = 0.149*MTOW   # [kg]

xcg_mg = xcg_w + 3  # [m] Main landing gear
W_mg = 0.035*MTOW  #[kg]

xcg_p = xcg_w - 1  # [m] Propulsion including nacelle
W_p = 0.103*MTOW - 660.1  # [kg]

W_wgroup = W_w + W_mg + W_p
W_p_new = W_p - 0.9*W_wgroup  # 0.1*6601 = 660.1 kg lighter
xcg_wgroup = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p_new)/(W_w + W_mg + W_p_new) # [m]
xcg_wgroup_mac = (xcg_wgroup - x_leadingedge)/MAC # [MAC]

# Fuselage group; fuselage, horizontal tailplane, vertical tailplane, nose gear

xcg_cargof = 5  # [-] Cargo front
xcg_cargob = 22  # [-] Cargo back

W_f = 0.248*MTOW  # [kg] Fuselage
W_f_new = 1.02*W_f  # [kg] 460 kg increase
xcg_f = 13  # [m]

W_batt = 1200  # [kg]
xcg_batt = (xcg_cargob*800 + xcg_cargof*400)/(800 + 400)  # 1200 kg increase

xcg_h = 25  # [m] Horizontal tail plane
W_h = 0.018*MTOW  # [kg]

xcg_v = 25  # [m] Vertical tailplane
W_v = 0.02*MTOW  # [kg]

xcg_ng = 3  # [m] Nose gear
W_ng = 0.005*MTOW  # [kg]

W_fgegroup = W_f + W_h + W_v + W_ng + W_batt
xcg_fgroup = (xcg_f*W_f_new + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng + xcg_batt*W_batt)/(W_f + W_h + W_v + W_ng + W_batt)  # [m]
xcg_fgroup_mac = (xcg_fgroup - x_leadingedge)/MAC  # [MAC]

# Variable weights

seat_pitch = 0.7366  # [m]
xcg_frontpass = 6  # [m]
xcg_backpass = xcg_frontpass + 17*seat_pitch  # [m]
W_2pass = 160  # [kg]

xcg_cargof = (xcg_cargof - x_leadingedge)/MAC  # [-] Cargo front
xcg_cargob = (xcg_cargob - x_leadingedge)/MAC  # [-] Cargo back

# x_c.g calculation

xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p) # [m]
xcgOEWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_fixed = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p


def cargoback(W_fixed, xcgOEW):
    W_old = W_fixed
    xcg_old = xcgOEWmac
    W_cargob = 1000 # [kg]
    W_cargof = 1000 # [kg]
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
    xcg_p = [(xcg_frontpass - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 17):
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
    xcg_p = [(xcg_backpass - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 17):
        xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passback, W_passback = passbackwindow(W_carback, xcg_carback, W_2pass, seat_pitch)

def passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
    W_old = W_passforward[-1]
    xcg_old = xcg_passforward[-1]
    xcg_p = [(xcg_frontpass - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 17):
        xcg_p.append(xcg_p[i-1] + seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passforwardaisle, W_passforwardaisle = passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)

def passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
    W_old = W_passforward[-1]
    xcg_old = xcg_passforward[-1]
    xcg_p = [(xcg_backpass - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, 17):
        xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
        xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
        xcg_list.append(xcg_new)
        W_list.append(W_old + W_2pass)
        W_old = W_old + W_2pass
        xcg_old = xcg_new
    return xcg_list, W_list

xcg_passbackaisle, W_passbackaisle = passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)

def fuel(xcg_passbackaisle, W_passbackaisle):
    W_old = W_passbackaisle[-1]
    xcg_old = xcg_passbackaisle[-1]
    xcg_fuel = (xcg_w - x_leadingedge)/MAC # [m]
    W_fuel = 5000 - 1000 # [kg]
    W_fueltotal = [W_old]
    xcg_fueltotal = [xcg_old]
    xcg_total = (W_passbackaisle[-1]*xcg_passbackaisle[-1] + W_fuel*xcg_fuel)/(W_passbackaisle[-1] + W_fuel)
    W_total = W_passbackaisle[-1] + W_fuel
    xcg_fueltotal.append(xcg_fuel)
    W_fueltotal.append(W_total)
    return xcg_fueltotal, W_fueltotal

xcg_fueltotal, W_fueltotal = fuel(xcg_passbackaisle, W_passbackaisle)

# Calculate min and max cg position

xcg_min_list = [min(xcg_carfront), min(xcg_carback), min(xcg_passforward), min(xcg_passback), min(xcg_passforwardaisle), min(xcg_passbackaisle), min(xcg_fueltotal)]
xcg_max_list = [max(xcg_carfront), max(xcg_carback), max(xcg_passforward), max(xcg_passback), max(xcg_passforwardaisle), max(xcg_passbackaisle), max(xcg_fueltotal)]
xcg_min = min(xcg_min_list)
xcg_max = max(xcg_max_list)

plt.plot(xcg_carfront, W_carfront)
plt.plot(xcg_carback, W_carback)
plt.plot(xcg_passforward, W_passforward)
plt.plot(xcg_passback, W_passback)
plt.plot(xcg_passforwardaisle, W_passforwardaisle)
plt.plot(xcg_passbackaisle, W_passbackaisle)
plt.plot(xcg_fueltotal, W_fueltotal)
plt.show()


# Stick-fixed static stability diagram

CLah = 3.5  # CLah : the higher, the more stable.
CL_alpha_Ah = 2.0  # the higher, the less stable.
deda = 0.4  # de/ da: the higher, the less stable.
lh = 10/MAC  # lh: the higher, the more stable.
c = 1
Vh = 138.89/MAC
V = 138.89/MAC  # Vh/V: the higher, the more stable.
VhV = Vh/V
xac = (13 - x_leadingedge)/MAC
S = 61.0/(MAC*MAC)

# Stability curve

x_cg = np.linspace(0.5, 1.8, 2)
ShS_stable = x_cg/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - (xac-0.05)/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))
ShS_limit = x_cg/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - xac/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))

# Control curve

# CLh = -0.5  # Controllable
Cmac = -0.8  # not controllable
CLAh = 1.5  # not controllable

Sh = 1
ShS = Sh/S
CLh = (Cmac + CLAh*(xcg_fueltotal[-1] - xac)/c)*c/(ShS*lh)
ShS_control = x_cg/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))
ShS_control_0 = xac - Cmac/CLAh

ShS_control_min = xcg_min/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))

xcg_range = np.linspace(xcg_min, xcg_max, 2)
ycg_range = [ShS_control_min, ShS_control_min]

plt.plot(x_cg, ShS_stable)
plt.plot(x_cg, ShS_limit)
plt.plot(x_cg, ShS_control)
plt.axvline(xcg_max, color='black')
plt.axvline(xcg_min, color='black')
# plt.axvline(xac, color='red')
# plt.axvline(ShS_control_0, color='blue')
plt.axhline(y=0, color='black')
plt.plot(xcg_range, ycg_range)
plt.show()



