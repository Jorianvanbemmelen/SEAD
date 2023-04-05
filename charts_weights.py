import numpy as np
import matplotlib.pyplot as plt

MTOW = 23000    # Maximum Take-Off Weight [kg]
OEW = 13450     # Operational Empty Weight [kg]
PW = 7550       # Max Payload Weight [kg]
FW = 5000       # Max Fuel Weight [kg]

payload = 36 * 180 + 900 + 500
Fuel = 1736     # Fuel Weight Using MTOW - payload [kg]

Ws = [OEW, payload, Fuel]
Wlabels = ['Operational Empty Weight', 'Payload Weight', 'Fuel Weight']

fig, ax = plt.subplots(figsize=(8, 3), subplot_kw=dict(aspect='equal'))

print(sum(Ws))

def label(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.0f}%\n({absolute:d} kg)"


wedges, texts, autotexts = ax.pie(Ws, #center=(-1.5, 0),
                                  autopct=lambda pct: label(pct, Ws),
                                  textprops=dict(color='w'))

ax.legend(wedges, Wlabels, title="Contributions",
          loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight='bold')

ax.set_title("Weight Contributions to MTOW")
plt.show()