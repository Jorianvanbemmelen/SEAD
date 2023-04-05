
import numpy as np
import matplotlib.pyplot as plt
import math
from math import *

MTOW = 23000  # [kg] Maximum take off weight
MZFW = 21000  # [kg] Maximum zero fuel weight
OEW = 13600  # [kg] Operational empty weight

MAC = 2.37  # [m]
x_leadingedge = 11.23 # [m]

# Fuselage group; fuselage, horizontal tailplane, vertical tailplane, nose gear

xcg_f = 10.1  # [m] old 12.9
W_f = 0.248*MTOW  # [kg]

xcg_h = 25.6  # [m]
W_h = 0.018*MTOW  # [kg]

xcg_v = 25  # [m]
W_v = 0.02*MTOW  # [kg]

xcg_ng = 1.664  # [m]
W_ng = 0.005*MTOW  # [kg]

xcg_cf = 4.6  # [m]
W_cargof = 900 # [kg] max 900
xcg_cb = 22.9  # [m]
W_cargob = 500 # [kg] max 700

seat_pitch = 0.7366  # [m]
xcg_frontpass = 6  # [m]
n_rows = 18
xcg_backpass = xcg_frontpass + (n_rows-1)*seat_pitch  # [m]
W_2pass = 180  # [kg]

W_fgroup = W_f + W_h + W_v + W_ng + W_cargof + W_cargob + (n_rows)*2*W_2pass
xcg_fgroup = (xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_ng*W_ng + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass)/(W_f + W_h + W_v + W_ng + W_cargof + W_cargob + n_rows*2*W_2pass)  # [m]
xcg_fgroup_mac = (xcg_fgroup - x_leadingedge)/MAC  # [MAC]

# Wing group, wing, main landing gear, propulsion

xcg_w = 12.1  # [m] do not change
W_w = 0.149*MTOW  # [kg]

xcg_mg = 12.2  # [m]
xcg_mg_mac = (xcg_mg - x_leadingedge)/MAC
W_mg = 0.035*MTOW  #[kg]

xcg_p = xcg_w - 2.0  # [m]
W_p = 0.103*MTOW  # [kg]

xcg_fuel = xcg_w
W_fuel = MTOW - (W_fgroup + W_w + W_mg + W_p + 156)

W_wgroup = W_w + W_mg + W_p + W_fuel
xcg_wgroup = (xcg_w*W_w + xcg_mg*W_mg + xcg_p*W_p + xcg_fuel*W_fuel)/(W_w + W_mg + W_p + W_fuel) # [m]
xcg_wgroup_mac = (xcg_wgroup - x_leadingedge)/MAC # [MAC]

# x_c.g calculation

xcgOEW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p) # [m]
xcgOEWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_fixed = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p + 156

xcgMTOW = (xcg_w*W_w + xcg_f*W_f + xcg_h*W_h + xcg_v*W_v + xcg_mg*W_mg + xcg_ng*W_ng + xcg_p*W_p + xcg_fuel*W_fuel + xcg_cf*W_cargof + xcg_cb*W_cargob + (xcg_backpass + xcg_frontpass)*n_rows*W_2pass)/(W_w + W_f + W_h + W_v + W_mg + W_ng + W_p + W_fuel + W_cargof + W_cargob + n_rows*2*W_2pass) # [m]
xcgMTOWmac = (xcgOEW - x_leadingedge)/MAC  # [MAC]
W_MTOW = W_w + W_f + W_h + W_v + W_mg + W_ng + W_p + W_cargof + W_cargob + n_rows*2*W_2pass + W_fuel

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

# check main landing gear clearance
if xcg_mg_mac - xcg_fueltotal[-1] <= 0.1:
    print("xcg of main landing gear is ", (xcg_mg_mac - xcg_fueltotal[-1])*100, "% in front of the MTOW xcg, xcg_mg should be more than 10% behind aft cg.")


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
plt.title('Loading diagram of the ATR72-600')
# plt.ylim(13000, 24000)
# plt.xlim(0.35, 0.75)
plt.legend()
plt.ylim(13000, 24000)
plt.xlim(-0.05, 0.42)
plt.show()

# Stick-fixed static stability diagram

# Aircraft fixed parameters

S = 61.0
b = 27.05  # [m]
cg = S/b
AR = b**2/S
bh = 8.1  # [m] approximately
Sh = 12  # [m] approximately
ShS = Sh/S
ARh = bh**2/Sh  # or 4.4
bf = 2.64  # [m] fuselage diameter estimate
hf = bf  # [m] fuselage height=diameter estimate
lf = 27.17  # [m] fuselage length
lfn = 11.17 # [m] distance nose to root LE wing
c_r = 2.56
c_t = 1.1
taper = c_t / c_r  # c_tip/c_root estimation
Snet = (S - bf* c_r) # approximately
bn = 0.679  # [m] engine diameter wikipedia
ln = 2.130  # [m] distance front nacelle to 1/4 cord wikipedia

deda = 4/(AR + 2)  # de/ da: the higher, the less stable.
lh = 13.5  # lh: the higher, the more stable.
c = 2.37
Vh = 138.89
V = 138.89  # Vh/V: the higher, the more stable.
V_app = 58.132
V_cr = 141.66666667 #estimated
VhV = 1

eta = 0.95  # efficiency factor
Delta_halfC = 0.0  # half cord sweep in rad
Delta_LE = 0.0
Delta_quartc = 0.0
Delta_halfCh = 4.5*pi/180  # half cord sweep tail in rad
Delta_LEh = 14.0*pi/180

# W_landing = MZFW * 9.80665
rho_landing = 1.225 #rho sealevel
# V_approach = 87 #[m/s] just an estimation


CLh = -0.8  # True value Lift coefficient adjustable tail
CLAh = 2*W_fueltotal[0]*9.80665/(rho_landing*S*V_app**2)  # Tailless lift coefficient 1.5?
print("Wfueltotal=", W_fueltotal[0])
print("rho=",rho_landing)
print("S=",S)
print("Vapp=",V_app)
def CL_alpha_Vcr(Vcr, eta, AR, ARh, Delta_halfC, Delta_halfCh):
    M = Vcr / 343
    beta = sqrt(1 - M ** 2)
    CL_alpha_h_cr = 2*pi*ARh/(2 + sqrt(4 + (ARh*beta/eta)**2 * (1 + tan(Delta_halfCh)**2/beta**2)))
    CL_alpha_cr = 2*pi*AR/(2 + sqrt(4 + (AR*beta/eta)**2 * (1 + tan(Delta_halfC)**2/beta**2)))
    CL_alpha_Ah_cr = CL_alpha_h_cr*(1 + 2.15*bf/b)*Snet/S + pi*bf**2/(2*S)
    return CL_alpha_h_cr, CL_alpha_cr, CL_alpha_Ah_cr

def CL_alpha_Vapp(V_app, eta, AR, ARh, Delta_halfC, Delta_halfCh):
    M = V_app / 343
    beta = sqrt(1 - M ** 2)
    CL_alpha_h_app = 2*pi*ARh/(2 + sqrt(4 + (ARh*beta/eta)**2 * (1 + tan(Delta_halfCh)**2/beta**2)))
    CL_alpha_app = 2*pi*AR/(2 + sqrt(4 + (AR*beta/eta)**2 * (1 + tan(Delta_halfC)**2/beta**2)))
    CL_alpha_Ah_app = CL_alpha_h_app*(1 + 2.15*bf/b)*Snet/S + pi*bf**2/(2*S)
    return CL_alpha_h_app, CL_alpha_app, CL_alpha_Ah_app

CL_alpha_h_cr, CL_alpha_cr, CL_alpha_Ah_cr = CL_alpha_Vcr(V_cr, eta, AR, ARh, Delta_halfC, Delta_halfCh)
CL_alpha_h_app, CL_alpha_app, CL_alpha_Ah_app = CL_alpha_Vapp(V_app, eta, AR, ARh, Delta_halfC, Delta_halfCh)

# Location of aerodynamic center x_ac without tail

def xac_Vcr(bf,hf,lfn, CL_alpha_Ah_cr, S, c, cg, Delta_quartc, taper, b, bn, ln, CL_alpha_cr):
    xac_w = 0.25  # from lecture 7 slide 34
    xac_f1 = -1.8*bf*hf*lfn/(CL_alpha_Ah_cr*S*c)
    xac_f2 = 0.273*bf*cg*(b-bf)*tan(Delta_quartc)/((1+taper)*c**2*(b+2.15*bf))
    xac_n = 2 * -4.0*bn**2*ln*CL_alpha_cr/(S*c*CL_alpha_Ah_cr)
    xac_Vcr = xac_w + xac_f1 + xac_f2 + xac_n # - x_leadingedge/MAC  # tailless aircraft
    # print('X_ac', xac)
    return xac_Vcr

def xac_Vapp(bf,hf,lfn, CL_alpha_Ah_app, S, c, cg, Delta_quartc, taper, b, bn, ln, CL_alpha_app):
    xac_w = 0.25  # from lecture 7 slide 34
    xac_f1 = -1.8*bf*hf*lfn/(CL_alpha_Ah_app*S*c)
    xac_f2 = 0.273*bf*cg*(b-bf)*tan(Delta_quartc)/((1+taper)*c**2*(b+2.15*bf))
    xac_n = 2 * -4.0*bn**2*ln*CL_alpha_app/(S*c*CL_alpha_Ah_app)
    xac_Vapp = xac_w + xac_f1 + xac_f2 + xac_n # - x_leadingedge/MAC  # tailless aircraft
    # print('X_ac', xac)
    return xac_Vapp

xac_Vcr = xac_Vcr(bf,hf,lfn, CL_alpha_Ah_cr, S, c, cg, Delta_quartc, taper, b, bn, ln, CL_alpha_cr)
xac_Vapp = xac_Vapp(bf,hf,lfn, CL_alpha_Ah_app, S, c, cg, Delta_quartc, taper, b, bn, ln, CL_alpha_app)

Cm0_airfoil =  -0.01  # Zero aoa moment coefficient
CL_0_landing =  0.1 # Lift coefficient aircraft zero aoa, landing config
mu1 = 0.2
mu2 = 0.7
mu3 = 0.062
delta_Cl_max = 0.1
c_prime = c + 0.2
c_primec = c_prime / c
S_wf = 12.28
Cmacw = Cm0_airfoil*(AR*cos(Delta_LE)**2)/(AR+2*cos(Delta_LE))
delta_flap_quarter = mu2 * (-mu1 * delta_Cl_max * c_primec - (CLAh + delta_Cl_max*(1-S_wf/S))) * 1/8 * c_primec*(c_primec-1) + 0.7 * AR/(1+2/AR) * mu3 * delta_Cl_max * tan(Delta_quartc)
delta_flap = delta_flap_quarter - CLAh*(0.25 - xac_Vapp / c)
delta_fus = -1.8*(1 - 2.5*bf/lf)*pi*bf*hf*lf*CL_0_landing/(4*S*c*CL_alpha_Ah_app)
delta_nac = -0.05 #because we have wing mounted engines
Cmac = Cmacw + delta_flap + delta_fus + delta_nac

# CG range - x-as
x_cg = np.linspace(-0.2, 1, 2)

print('Cmac', Cmac)
print('CLah', CLAh)
print('xac_cr', xac_Vcr)
print('xac_app', xac_Vapp)
print('deda', deda)
print('CL_alpha_h_cr', CL_alpha_h_cr)
print('CL_alpha_h_app', CL_alpha_h_app)
print('CL_alpha_Ah_cr', CL_alpha_Ah_cr)
print('CL_alpha_Ah_app', CL_alpha_Ah_app)

# Stability curve - Vcr
ShS_stable = x_cg/(CL_alpha_h_cr*(1-deda)*lh*VhV**2/(CL_alpha_Ah_cr*c)) - (xac_Vcr-0.05)/(CL_alpha_h_cr*(1-deda)*lh*VhV**2/(CL_alpha_Ah_cr*c))
ShS_limit = x_cg/(CL_alpha_h_cr*(1-deda)*lh*VhV**2/(CL_alpha_Ah_cr*c)) - (xac_Vcr)/(CL_alpha_h_cr*(1-deda)*lh*VhV**2/(CL_alpha_Ah_cr*c))

# Control curve - Landing configuration V_app
a_control = 1/((CLh/CLAh)*(lh/c)*VhV**2) # hier iets proberen check CLh
b_control = (Cmac/CLAh) - xac_Vapp
y_control = a_control*x_cg+a_control*b_control

#ShS_control = x_cg/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac)/(CLh*lh*VhV**2/(CLAh*c))
#ShS_control_0 = xac - Cmac/CLAh
ShS_control_min = (xcg_min - 0.02*xcg_min)/(CLh*lh*VhV**2/(CLAh*c)) + (Cmac/CLAh - xac_Vapp)/(CLh*lh*VhV**2/(CLAh*c))

# Sh/S - x_cg range plot
xcg_range = np.linspace((xcg_min - 0.02*xcg_min), (xcg_max + 0.02*xcg_max), 2)
xcg_range1 = np.linspace(xcg_min, xcg_max, 2)
xcg_range2 = np.linspace(-1, 1, 2)
ycg_range = [ShS_control_min, ShS_control_min]
#print("Minimal value Sh/S =", ShS_control_min)
ycg_range2 = [ShS, ShS]

plt.plot(xcg_range, ycg_range, label='cg range')
plt.plot(xcg_range2, ycg_range2, label='cg range actual Sh/S')  # Actual Sh/S value
plt.plot(x_cg, ShS_stable, label='ShS stable')
plt.plot(x_cg, ShS_limit, label='ShS limit')
# plt.plot(x_cg, ShS_control, label='ShS control')
plt.plot(x_cg,y_control, label="ShS control")
plt.axvline(xcg_max, color='grey' ,label='max Xcg')
plt.axvline(xcg_min, color='grey', label='min Xcg')
plt.axvline((xcg_max + 0.02*xcg_max), color='black' ,label='max Xcg margin')
plt.axvline((xcg_min - 0.02*xcg_min), color='black', label='min Xcg margin')
# plt.axvline(xac, color='red')
# plt.axvline(ShS_control_0, color='blue')
plt.axhline(y=0, color='grey')
plt.legend(loc = 'upper left')
plt.ylabel('Sh/S [-]')
plt.xlabel('Xcg/MAC [-]')
plt.title('Scissor plot of the ATR72-600')
plt.xlim(-0.5,0.6)
plt.ylim(0,0.4)
plt.show()


