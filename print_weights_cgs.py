
import numpy as np
import matplotlib.pyplot as plt

MTOW = 23000  # [kg] Maximum take off weight
MZFW = 21000  # [kg] Maximum zero fuel weight
OEW = 13600  # [kg] Operational empty weight
MAC = 2.37  # [m]
x_leadingedge = 11.23 # [m]

# Fuselage group; fuselage, horizontal tailplane, vertical tailplane, nose gear

xcg_f = 12  # [m]
W_f = 0.248*MTOW  # [kg]
print(f'Fuselage: {W_f} kg, {(xcg_f - x_leadingedge) / MAC * 100} %MAC')

xcg_h = 25.6  # [m]
W_h = 0.018*MTOW  # [kg]
print(f'Horizontal Tail: {W_h} kg, {(xcg_h - x_leadingedge) / MAC * 100} %MAC')

xcg_v = 25  # [m]
W_v = 0.02*MTOW  # [kg]
print(f'Vertical Tail: {W_v} kg, {(xcg_v - x_leadingedge) / MAC * 100} %MAC')

xcg_ng = 1.664  # [m]
W_ng = 0.005*MTOW  # [kg]
print(f'Nose Gear: {W_ng} kg, {(xcg_ng - x_leadingedge) / MAC * 100} %MAC')

xcg_cf = 4.6  # [m]
W_cargof = 600 # [kg]
xcg_cb = 22.9  # [m]
W_cargob = 600 # [kg]

seat_pitch = 0.7366  # [m]
xcg_frontpass = 6  # [m]
n_rows = 18
xcg_backpass = xcg_frontpass + (n_rows-1)*seat_pitch  # [m]
W_2pass = 160  # [kg]

W_fgroup = W_f + W_h + W_v + W_ng + W_cargof + W_cargob + (n_rows)*2*W_2pass
xcg_fgroup = (xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass)/(W_f + W_h + W_v + W_ng + W_cargof + W_cargob + n_rows*2*W_2pass)  # [m]
xcg_fgroup_mac = (xcg_fgroup - x_leadingedge)/MAC  # [MAC]

W_fgroup_no_cargo = W_f + W_h + W_v + W_ng
xcg_fgroup_no_cargo = (xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng)/(W_f + W_h + W_v + W_ng)  # [m]
xcg_fgroup_no_cargo_mac = (xcg_fgroup_no_cargo - x_leadingedge)/MAC  # [MAC]

print(f'Fuselage group: W = {W_fgroup_no_cargo} kg, X_cg = {xcg_fgroup_no_cargo} m, or {xcg_fgroup_no_cargo_mac * 100} %MAC')

# Wing group, wing, main landing gear, propulsion

xcg_w = 12.15  # [m] approximately
W_w = 0.149*MTOW  # [kg]
print(f'Wing: {W_w} kg, {(xcg_w - x_leadingedge) / MAC * 100} %MAC')

xcg_mg = 12.434  # [m]
W_mg = 0.035*MTOW  #[kg]
print(f'Main Gear: {W_mg} kg, {(xcg_mg - x_leadingedge) / MAC * 100} %MAC')

xcg_p = xcg_w - 2.0  # [m]
W_p = 0.103*MTOW  # [kg]
print(f'Propulsion: {W_p} kg, {(xcg_p - x_leadingedge) / MAC * 100} %MAC')

xcg_fuel = xcg_w
W_fuel = MTOW - (W_fgroup + W_w + W_mg + W_p)
print(f'W_fuel: {W_fuel}')

W_wgroup = W_w + W_mg + W_p + W_fuel
xcg_wgroup = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p + xcg_fuel*W_fuel) / (W_w + W_mg + W_p + W_fuel) # [m]
xcg_wgroup_mac = (xcg_wgroup - x_leadingedge)/MAC # [MAC]

W_wgroup_no_fuel = W_w + W_mg + W_p
xcg_wgroup_no_fuel = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p) / (W_w + W_mg + W_p) # [m]
xcg_wgroup_no_fuel_mac = (xcg_wgroup_no_fuel - x_leadingedge) / MAC # [MAC]

print(f'Wing group: W = {W_wgroup_no_fuel} kg, X_cg = {xcg_wgroup_no_fuel} m, or {xcg_wgroup_no_fuel_mac * 100} %MAC')

# x_c.g calculation

xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p) # [m]
xcgOEWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]

print(f'Operational Empty: W = {W_fgroup_no_cargo + W_wgroup_no_fuel} kg, X_cg = {xcgOEW} m, or {xcgOEWmac * 100} %MAC')

W_fixed = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p

xcgMTOW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p + xcg_fuel*W_fuel + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p + W_fuel + W_cargof + W_cargob + n_rows*2*W_2pass) # [m]
xcgMTOWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_MTOW = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p + W_cargof + W_cargob + n_rows*2*W_2pass + W_fuel

# HE modifications to weights

W_wgroup_no_fuel_HE = 0.9 * W_w + W_mg + W_p
W_fgroup_no_cargo_HE = 1.02 * W_f + W_ng + W_h + W_v

print(f'W_wgroup_no_fuel_HE: {W_wgroup_no_fuel_HE} kg\n'
      f'W_fgroup_no_cargo_HE: {W_fgroup_no_cargo_HE} kg')

OEW_HE = W_wgroup_no_fuel_HE + W_fgroup_no_cargo_HE + 400 + 800
xcgOEW_HE = (W_fgroup_no_cargo_HE * xcg_fgroup_no_cargo + W_wgroup_no_fuel_HE * xcg_wgroup_no_fuel
             + xcg_cf * 400 + xcg_cb * 800) / (W_fgroup_no_cargo_HE + W_wgroup_no_fuel_HE + 1200)

print(f'OEW_HE: {OEW_HE} kg, xcgOEW_HE: {xcgOEW_HE} m')

print(f'Fuel Weight: {MTOW - OEW_HE - 7550} kg')





# '''
# def cargoback(W_fixed, xcgOEW):
#     W_old = W_fixed
#     xcg_old = xcgOEWmac
#     xcg_cargob = (xcg_cb - x_leadingedge)/MAC # [m]
#     xcg_cargof = (xcg_cf - x_leadingedge)/MAC # [m]
#     xcg_carback = [xcg_old]
#     W_carback = [W_old]
#     xcg_carb = (W_old*xcg_old + W_cargob*xcg_cargob)/(W_old + W_cargob)
#     W_carb = W_old + W_cargob
#     xcg_carback.append(xcg_carb)
#     W_carback.append(W_carb)
#     xcg_carf = (W_carb*xcg_carb + W_cargof*xcg_cargof)/(W_carb + W_cargof)
#     W_carf = W_carb + W_cargof
#     xcg_carback.append(xcg_carf)
#     W_carback.append(W_carf)
#     return xcg_carback, W_carback
#
# xcg_carback, W_carback = cargoback(W_fixed, xcgOEW)
#
# def cargofront(W_fixed, xcgOEW):
#     W_old = W_fixed
#     xcg_old = xcgOEWmac
#     xcg_cargob = (xcg_cb - x_leadingedge)/MAC  # [m]
#     xcg_cargof = (xcg_cf - x_leadingedge)/MAC  # [m]
#     xcg_carfront = [xcg_old]
#     W_carfront = [W_old]
#     xcg_carf = (W_old*xcg_old + W_cargof*xcg_cargof)/(W_old + W_cargof)
#     W_carf = W_old + W_cargof
#     xcg_carfront.append(xcg_carf)
#     W_carfront.append(W_carf)
#     xcg_carb = (W_carf*xcg_carf + W_cargob*xcg_cargob)/(W_carf + W_cargob)
#     W_carb = W_carf + W_cargob
#     xcg_carfront.append(xcg_carb)
#     W_carfront.append(W_carb)
#     return xcg_carfront, W_carfront
#
# xcg_carfront, W_carfront = cargofront(W_fixed, xcgOEW)
#
# def passforwardwindow(W_carback, xcg_carback, W_2pass, seat_pitch):
#     # print(W_carback)
#     W_old = W_carback[2]
#     xcg_old = xcg_carback[2]
#     xcg_p = [(xcg_frontpass - seat_pitch - x_leadingedge)/MAC]
#     xcg_list = [xcg_old]
#     W_list = [W_old]
#     for i in range(1, (n_rows + 1)):
#         xcg_p.append(xcg_p[i-1] + seat_pitch/MAC)
#         xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
#         xcg_list.append(xcg_new)
#         W_list.append(W_old + W_2pass)
#         W_old = W_old + W_2pass
#         xcg_old = xcg_new
#     return xcg_list, W_list
#
# xcg_passforward, W_passforward = passforwardwindow(W_carback, xcg_carback, W_2pass, seat_pitch)
#
# def passbackwindow(W_carback, xcg_carback, W_2pass, seat_pitch):
#     W_old = W_carback[2]
#     xcg_old = xcg_carback[2]
#     xcg_p = [(xcg_backpass + seat_pitch - x_leadingedge)/MAC]
#     xcg_list = [xcg_old]
#     W_list = [W_old]
#     for i in range(1, (n_rows + 1)):
#         xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
#         xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
#         xcg_list.append(xcg_new)
#         W_list.append(W_old + W_2pass)
#         W_old = W_old + W_2pass
#         xcg_old = xcg_new
#     return xcg_list, W_list
#
# xcg_passback, W_passback = passbackwindow(W_carback, xcg_carback, W_2pass, seat_pitch)
#
# def passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
#     W_old = W_passforward[-1]
#     xcg_old = xcg_passforward[-1]
#     xcg_p = [(xcg_frontpass - seat_pitch - x_leadingedge)/MAC]
#     xcg_list = [xcg_old]
#     W_list = [W_old]
#     for i in range(1, (n_rows + 1)):
#         xcg_p.append(xcg_p[i-1] + seat_pitch/MAC)
#         xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
#         xcg_list.append(xcg_new)
#         W_list.append(W_old + W_2pass)
#         W_old = W_old + W_2pass
#         xcg_old = xcg_new
#     return xcg_list, W_list
#
# xcg_passforwardaisle, W_passforwardaisle = passforwardaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)
#
# def passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch):
#     W_old = W_passforward[-1]
#     xcg_old = xcg_passforward[-1]
#     xcg_p = [(xcg_backpass + seat_pitch - x_leadingedge)/MAC]
#     xcg_list = [xcg_old]
#     W_list = [W_old]
#     for i in range(1, (n_rows + 1)):
#         xcg_p.append(xcg_p[i-1] - seat_pitch/MAC)
#         xcg_new = (W_old*xcg_old + W_2pass*xcg_p[i])/(W_old + W_2pass)
#         xcg_list.append(xcg_new)
#         W_list.append(W_old + W_2pass)
#         W_old = W_old + W_2pass
#         xcg_old = xcg_new
#     return xcg_list, W_list
#
# xcg_passbackaisle, W_passbackaisle = passbackaisle(W_passforward, xcg_passforward, W_2pass, seat_pitch)
#
# def fuel(xcg_passbackaisle, W_passbackaisle):
#     W_old = W_passbackaisle[-1]
#     xcg_old = xcg_passbackaisle[-1]
#     xcg_fuel = (xcg_w - x_leadingedge)/MAC # [m]
#     W_fueltotal = [W_old]
#     xcg_fueltotal = [xcg_old]
#     xcg_total = (W_passbackaisle[-1]*xcg_passbackaisle[-1] + W_fuel*xcg_fuel)/(W_passbackaisle[-1] + W_fuel)
#     W_total = W_passbackaisle[-1] + W_fuel
#     xcg_fueltotal.append(xcg_total)
#     W_fueltotal.append(W_total)
#     return xcg_fueltotal, W_fueltotal
#
# xcg_fueltotal, W_fueltotal = fuel(xcg_passbackaisle, W_passbackaisle)
#
# # Calculate min and max cg position
#
# xcg_min_list = [min(xcg_carfront), min(xcg_carback), min(xcg_passforward), min(xcg_passback), min(xcg_passforwardaisle), min(xcg_passbackaisle), min(xcg_fueltotal)]
# xcg_max_list = [max(xcg_carfront), max(xcg_carback), max(xcg_passforward), max(xcg_passback), max(xcg_passforwardaisle), max(xcg_passbackaisle), max(xcg_fueltotal)]
# xcg_min = min(xcg_min_list)
# xcg_max = max(xcg_max_list)
#
# plt.plot(xcg_carfront, W_carfront)
# plt.plot(xcg_carback, W_carback)
# plt.plot(xcg_passforward, W_passforward)
# plt.plot(xcg_passback, W_passback)
# plt.plot(xcg_passforwardaisle, W_passforwardaisle)
# plt.plot(xcg_passbackaisle, W_passbackaisle)
# plt.plot(xcg_fueltotal, W_fueltotal)
# plt.show()
#
#
# # Stick-fixed static stability diagram
#
# S = 61.0/(MAC*MAC)
# Snet = (61.0 - 8.94)/(MAC*MAC)  # approsimately
# b = 27.05  # [m]
# AR = b**2/S
# bh = 8.1 / MAC  # [m] approximately
# CLah = 1.2  # CLah : the higher, the more stable.
# CL_alpha_Ah = 3.0  # the higher, the less stable.
# deda = 4/(AR + 2)  # de/ da: the higher, the less stable.
# lh = 13.5/MAC  # lh: the higher, the more stable.
# c = 1
# Vh = 138.89/MAC
# V = 138.89/MAC  # Vh/V: the higher, the more stable.
# VhV = Vh/V
# xac_w = (xcg_w - x_leadingedge)/MAC #this is (Xac)w not Xac for tailless aircraft!
# xac_f1 = 1 #opvulling hier zijn formules voor
# xac_f2 = 1 #opvulling
# xac_n = 1 #opvulling
# xac = xac_w + xac_f1 + xac_f2 +xac_n
# # Stability curve
#
# x_cg = np.linspace(0, 1, 2)
# ShS_stable = x_cg/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - (xac-0.05)/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))
# ShS_limit = x_cg/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c)) - xac/(CLah*(1-deda)*lh*VhV**2/(CL_alpha_Ah*c))
#
# # Control curve
#
# # CLh = -0.5  # Controllable
# Cmac = -0.6  # not controllable
# CLAh = 1.5  # not controllable
#
# Sh = 1
# ShS = Sh/S
# CLh = (Cmac + CLAh*(xcg_fueltotal[-1] - xac)/c)*c/(ShS*lh)
# ShS_control = x_cg/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))
# ShS_control_0 = xac - Cmac/CLAh
#
# ShS_control_min = xcg_min/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))
#
# xcg_range = np.linspace(xcg_min, xcg_max, 2)
# ycg_range = [ShS_control_min, ShS_control_min]
#
# plt.plot(x_cg, ShS_stable)
# plt.plot(x_cg, ShS_limit)
# plt.plot(x_cg, ShS_control)
# plt.axvline(xcg_max, color='black')
# plt.axvline(xcg_min, color='black')
# # plt.axvline(xac, color='red')
# # plt.axvline(ShS_control_0, color='blue')
# plt.axhline(y=0, color='grey')
# plt.plot(xcg_range, ycg_range)
# plt.show()
# '''

