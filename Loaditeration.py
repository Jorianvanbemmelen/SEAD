
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Load import *

MTOW = 23000  # [kg] Maximum take off weight
MZFW = 21000  # [kg] Maximum zero fuel weight
OEW = 13600  # [kg] Operational empty weight

MAC = 2.37  # [m]
x_leadingedge = 11.23 # [m]

# Fuselage group; fuselage, horizontal tailplane, vertical tailplane, nose gear

xcg_f = 12.9  # [m] old 11.5
xcg_f = xcg_f - 0.9
W_f = 0.248*MTOW  # [kg]
W_f_new = 1.02*W_f  # [kg] 460 kg increase

W_h = 0.018*MTOW  # [kg]

W_v = 0.02*MTOW  # [kg]

W_ng = 0.005*MTOW  # [kg]

W_cargof = 500 # [kg]
W_cargob = 500 # [kg]

seat_pitch = 0.7366  # [m]
xcg_frontpass = 6  # [m]
n_rows = 16
xcg_backpass = xcg_frontpass + (n_rows-1)*seat_pitch  # [m]
W_2pass = 180  # [kg]

W_batt = 1200  # [kg]
xcg_batt = (xcg_cb*800 + xcg_cf*400)/(800 + 400)  # 1200 kg increase

# Not really important:
W_fgroup = W_f_new + W_h + W_v + W_ng + W_cargof + W_cargob + (n_rows)*2*W_2pass + W_batt
xcg_fgroup = (xcg_f*W_f_new + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass + xcg_batt*W_batt)/(W_f + W_h + W_v + W_ng + W_cargof + W_cargob + n_rows*2*W_2pass + W_batt)  # [m]
xcg_fgroup_mac = (xcg_fgroup - x_leadingedge)/MAC  # [MAC]

# Wing group, wing, main landing gear, propulsion

W_w = 0.149*MTOW - 660  # [kg]

W_mg = 0.035*MTOW  #[kg]

W_p = 0.103*MTOW  # [kg]

W_fuel = MTOW - (W_fgroup + W_w + W_mg + W_p)

W_wgroup = W_w + W_mg + W_p + W_fuel
xcg_wgroup = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p + xcg_fuel*W_fuel)/(W_w + W_mg + W_p + W_fuel) # [m]
xcg_wgroup_mac = (xcg_wgroup - x_leadingedge)/MAC # [MAC]

# x_c.g calculation
xcgOEW = (xcg_w*W_w + xcg_f*W_f_new + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p + xcg_batt*W_batt)/(W_w + W_f_new + W_h + W_v + W_mg + W_ng + W_p + W_batt) # [m]
xcgOEWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_fixed = W_w + W_f_new + W_h + W_v + W_mg + W_ng + W_p + W_batt

xcgMTOW = (xcg_w*W_w + xcg_f*W_f_new + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p + xcg_fuel*W_fuel + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass + xcg_batt*W_batt)/(W_w + W_f_new + W_h + W_v + W_mg + W_ng + W_p + W_fuel + W_cargof + W_cargob + n_rows*2*W_2pass + W_batt)  # [m]
xcgMTOWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_MTOW = W_w + W_f_new + W_h + W_v + W_mg + W_ng + W_p + W_cargof + W_cargob + n_rows*2*W_2pass + W_fuel + W_batt


def cargoback(W_fixed, xcgOEWmac):
    W_old = W_fixed
    xcg_old = xcgOEWmac
    xcg_cargob = (xcg_cb - x_leadingedge)/MAC # [m]
    xcg_cargof = (xcg_cf - x_leadingedge)/MAC # [m]
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

xcg_carback, W_carback = cargoback(W_fixed, xcgOEWmac)

def cargofront(W_fixed, xcgOEWmac):
    W_old = W_fixed
    xcg_old = xcgOEWmac
    xcg_cargob = (xcg_cb - x_leadingedge)/MAC  # [m]
    xcg_cargof = (xcg_cf - x_leadingedge)/MAC  # [m]
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

xcg_carfront, W_carfront = cargofront(W_fixed, xcgOEWmac)

def passforwardwindow(W_carback, xcg_carback, W_2pass, seat_pitch):
    # print(W_carback)
    W_old = W_carback[2]
    xcg_old = xcg_carback[2]
    xcg_p = [(xcg_frontpass - seat_pitch - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, (n_rows + 1)):
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
    xcg_p = [(xcg_backpass + seat_pitch - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, (n_rows + 1)):
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
    xcg_p = [(xcg_frontpass - seat_pitch - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, (n_rows + 1)):
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
    xcg_p = [(xcg_backpass + seat_pitch - x_leadingedge)/MAC]
    xcg_list = [xcg_old]
    W_list = [W_old]
    for i in range(1, (n_rows + 1)):
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
    W_fueltotal = [W_old]
    xcg_fueltotal = [xcg_old]
    xcg_total = (W_passbackaisle[-1]*xcg_passbackaisle[-1] + W_fuel*xcg_fuel)/(W_passbackaisle[-1] + W_fuel)
    W_total = W_passbackaisle[-1] + W_fuel
    xcg_fueltotal.append(xcg_total)
    W_fueltotal.append(W_total)
    return xcg_fueltotal, W_fueltotal

xcg_fueltotal, W_fueltotal = fuel(xcg_passbackaisle, W_passbackaisle)

# Calculate min and max cg position

xcg_min_list = [min(xcg_carfront), min(xcg_carback), min(xcg_passforward), min(xcg_passback), min(xcg_passforwardaisle), min(xcg_passbackaisle), min(xcg_fueltotal)]
xcg_max_list = [max(xcg_carfront), max(xcg_carback), max(xcg_passforward), max(xcg_passback), max(xcg_passforwardaisle), max(xcg_passbackaisle), max(xcg_fueltotal)]
xcg_min = min(xcg_min_list)
xcg_max = max(xcg_max_list)

plt.plot(xcg_carfront, W_carfront, label = 'cargo front')
plt.plot(xcg_carback, W_carback, label = 'cargo back')
plt.plot(xcg_passforward, W_passforward, label = 'pass W. forward')
plt.plot(xcg_passback, W_passback, label = 'pass W. back')
plt.plot(xcg_passforwardaisle, W_passforwardaisle, label = 'pass A. forward')
plt.plot(xcg_passbackaisle, W_passbackaisle, label = 'pass A. back')
plt.plot(xcg_fueltotal, W_fueltotal, label = 'fuel')
plt.xlabel('Xcg w.r.t MAC [m]')
plt.ylabel('W [kg]')
plt.title('Loading diagram of the ATR72-HE')
plt.legend()
plt.show()


# Stick-fixed static stability diagram

# Aircraft fixed parameters

b_new = b*sqrt(1.2)
cg = S/b_new
AR = b_new**2/S

CL_alpha_h = 2*pi*ARh/(2 + sqrt(4 + (ARh*beta/eta)**2 * (1 + tan(Delta_halfCh)**2/beta**2)))
CL_alpha = 2*pi*AR/(2 + sqrt(4 + (AR*beta/eta)**2 * (1 + tan(Delta_halfC)**2/beta**2)))
CL_alpha_Ah = CL_alpha_h*(1 + 2.15*bf/b_new)*Snet/S + pi*bf**2/(2*S)

# Location of aerodynamic center x_ac without tail
xac_w = 0.25  # from lecture 7 slide 34
xac_f1 = -1.8*bf*hf*lfn/(CL_alpha_Ah*S*c)
xac_f2 = 0.273*bf*cg*(b_new-bf)*tan(Delta_quartc)/((1+taper)*c**2*(b_new+2.15*bf))
xac_n = -8.0*bn**2*ln*CL_alpha/(S*c*CL_alpha_Ah)
xac = xac_w + xac_f1 + xac_f2 + xac_n # - x_leadingedge/MAC  # tailless aircraft

Cmac = CLh*Sh*lh/(S*c) - CLAh*(xcg_fueltotal[-1] - xac)/c

# Stability curve

x_cg = np.linspace(0, 1, 2)
ShS_stable = x_cg/(CL_alpha_h*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - (xac-0.05)/(CL_alpha_h*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))
ShS_limit = x_cg/(CL_alpha_h*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - xac/(CL_alpha_h*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))

# Control curve

ShS_control = x_cg/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))
ShS_control_0 = xac - Cmac/CLAh
ShS_control_min = xcg_min/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))


# Sh/S - x_cg range plot
xcg_range = np.linspace(xcg_min, xcg_max, 2)
xcg_range2 = np.linspace(0, 1, 2)
ycg_range = [ShS_control_min, ShS_control_min]
print("Minimal value Sh/S =", ShS_control_min)
ycg_range2 = [ShS, ShS]


plt.plot(xcg_range, ycg_range, label='cg range')
plt.plot(xcg_range2, ycg_range2, label='cg range actual Sh/S')  # Actual Sh/S value
plt.plot(x_cg, ShS_stable, label='ShS stable')
plt.plot(x_cg, ShS_limit, label='ShS limit')
plt.plot(x_cg, ShS_control, label='ShS control')
plt.axvline(xcg_max, color='black' ,label='max Xcg')
plt.axvline(xcg_min, color='black', label='min Xcg')
# plt.axvline(xac, color='red')
# plt.axvline(ShS_control_0, color='blue')
plt.axhline(y=0, color='grey')
plt.legend(loc = 'upper left')
plt.ylabel('Sh/S [-]')
plt.xlabel('Xcg/MAC [-]')
plt.title('Scissor plot of the ATR72-HE')
plt.show()
