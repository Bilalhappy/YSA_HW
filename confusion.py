from pretty_confusion_matrix import pp_matrix
import numpy as np
import pandas as pd

array = np.array([[547,   2,   0], [ 55, 146,   2], [  0,   5, 119]])
# get pandas dataframe
df_cm = pd.DataFrame(array, index=["no_rain", "modarate_rain", "intense_rain"], columns=["no_rain", "modarate_rain", "intense_rain"])
# colormap: see this and choose your more dear
cmap = 'twilight'
pp_matrix(df_cm, cmap=cmap)


import netCDF4
from netCDF4 import Dataset
import numpy as np
import datetime as dt
import time
import os 
import pandas as pd
import matplotlib
import matplotlib.dates as mdates
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.stats.stats import pearsonr   
from itertools import chain

f1= Dataset("data/data.nc")

date = []
for i in range(len(f1.variables['time'])):
    dd = dt.timedelta(hours = f1.variables['time'][:].tolist()[i])
    date.append((dt.datetime.strptime("1900-01-01","%Y-%m-%d")+dd))
def interpolation(lat,long,lats,longs,zs):
    ds = []
    p  = []
    for i in range(len(lats)):
        for j in range(len(longs)):
            ds.append(np.sqrt((lat-lats[i])**2 + (long-longs[j])**2))
            p.append(1/ds[-1]**2)
    w = []
    for i in range(len(p)):
        w.append(p[i]/sum(p))
    z = 0
    for i in range(len(zs)):
        z += zs[i]*w[i]
    return z

tp = []

for i in range(len(date)):
    tp.append(interpolation(41.104, 29.019,f1.variables["latitude"][:],f1.variables["longitude"][:],list(chain.from_iterable(f1.variables["tp"][i,:,:])))*1000)
print(date[0],date[-1])
plt.plot(date,tp)
print(date[0],date[-1])
print(tp[-10:])

tro_xlsx = pd.read_excel("data/tro/tro.xlsx")
meteo_xlsx = pd.read_excel("data/meteo/meteo_RNX.xlsx")

K2 = 16.48		#atmospheric refractivity constant (K / mbar)
K3 = 3.776*10**5	#atmospheric refractivity constant (K^2 / mbar)
pw = 103		#the density of liquid water (kg/m^3)
Rw = 461.5	#the specific gas constant for water vapor (J/(kg . K)) [J = kg * m^2 / s^2]
Ts = 288.15	#seosanal mean temperature (unit: K)
pwv = []
print(len(tro_xlsx["date"]),len(meteo_xlsx["date"]))
for i in range(len(tro_xlsx["date"])):
    Tm = 44.05 + 0.81 * (meteo_xlsx["WetT"][i]+273.15)
    pi = 10e6 / (pw * Rw * (K2 + K3 / Tm))
    pwv.append(pi * tro_xlsx["trowet"][i])
    
plt.gcf().set_size_inches(10, 5)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
plt.plot(date,tp,label = "Precipitation")
plt.legend()
plt.xlabel('Date')
plt.title('Precipitation')
plt.xlabel('Precipitation')
plt.ylabel('Precipitation')
plt.savefig("Precipitation.jpeg",bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close("all")
plt.gcf().set_size_inches(10, 5)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
plt.plot(tro_xlsx["date"],pwv,label="PWV")
plt.legend()
plt.title('PWV')
plt.xlabel('Date')
plt.ylabel('PWV')
plt.savefig("PWV.jpeg",bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close("all")
press = meteo_xlsx["press."]
dryt =  meteo_xlsx["DryT"]
hum =  meteo_xlsx["Hum."]
Temps = [i for i in range(len(hum))]
meteo_xlsx["Temps"] = Temps

plt.gcf().set_size_inches(10, 5)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
plt.plot(tro_xlsx["date"],hum,label="Humidity")
plt.legend()
plt.title('Humidity')
plt.xlabel('Date')
plt.ylabel('Humidity')
plt.savefig("Humidity.jpeg",bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close("all")
plt.gcf().set_size_inches(10, 5)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
plt.plot(tro_xlsx["date"],dryt,label="Temperature")
plt.legend()
plt.title('Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.savefig("DryTemperature.jpeg",bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close("all")
plt.gcf().set_size_inches(10, 5)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
plt.plot(tro_xlsx["date"],press,label="Pressure")
plt.legend()
plt.title('Pressure')
plt.xlabel('Date')
plt.ylabel('Pressure')
plt.savefig("Pressure.jpeg",bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close()
plt.close("all")

