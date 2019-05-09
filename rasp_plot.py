
"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os,errno
import pickle
import sys
import collections
import bisect
import datetime
from rasp_data import Rasp_Data
from matplotlib import colors as mcolors


def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i
## INPUT DATA AND FILES DEFINITIONS

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

data_path = "D:\\Application_data\\yamzv8data\\test_P800521_P225"
enable_rasp = True
rasp_filename = "MDS_snP051_20190506_0900.csv"
report_name = "Rasperry_Datalog_Report_{}".format(rasp_filename.split('.')[0])

num_cyls = 8            # number of cylinders of engine, for plotting the exhaust temperatures of single cylinder

rasp_data = Rasp_Data(data_path,rasp_filename)

rasp_data_dict = rasp_data.load_data()

if rasp_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(1)

SMALL_SIZE = 7
MEDIUM_SIZE = 8
BIGGER_SIZE = 10

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

LEGEND_BEST =	0
LEGEND_UPPER_R = 1
LEGEND_UPPER_L = 2
LEGEND_LOWER_L = 3
LEGEND_LOWER_R = 4
LEGEND_RIGHT = 5
LEGEND_LEFT = 6
LEGEND_CENTER_R = 7
LEGEND_LOWER_C = 8
LEGEND_UPPER_C = 9
LEGEND_CENTER = 10

AM_toff= 0
AE_toff=100
x_lim=[0,720]                       #time
rpm_lim = [600,2000]
rpm_step=200                        #rpm for Power Curve


StatsPicture = False                   # Set True if plotting statistics is needed, False if only plot f(time) needed
## Define input signal names
# raspberry datafile parameters
rasp_signal_list = ['Timestamp_Unix','TC_HPH_GAS_IN','TC_HPH_GAS_OUT','TC_HPH_H2O_IN','TC_HPH_H2O_OUT', 'TC_HPH_BODY',
                    'TC_MDS_GAS_OUT', 'TC_TANK', 'TC_EXH', 'HPH_PCNG_IN', 'MDS_PTANK', 'MDS_P1S', 'MDS_PGAS_OUT',
                    'MDS_TRNG_IN', 'MDS_TRH2O_IN','MDS_TRH2O_OUT', 'HPH_QH2O', 'MDS_TRENV', 'MDS_TRBODY',
                    'Tachograph_Vehicle_Speed', 'Transmission_Current_Gear', 'Engine_Coolant_Temperature',
                    'Engine_Fuel_Temperature', 'Engine_Oil_Temperature', 'Engine_ECU_Temperature', 'Engine_Speed',
                    'Engine_Demand_Percent_Torque','Engine_Boost_Pressure', 'Engine_Intake_Manifold_Temperature',
                    'Engine_Intake_Manifold_Pressure', 'Engine_Exhaust_Temperature', 'Engine_Fuel_Rate', 'Spark_Advance',
                    'zsMap', 'asPre','zsPrail', 'asAirMain', 'qsTinj', 'WasteGateDC','EngineMode', 'fsKO2','usCorrAdat' ]


#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets



rasp_sigmap = dict()
for idx,signal in enumerate(rasp_data_dict):
    for idy, name in enumerate(rasp_signal_list):
        if rasp_data_dict['{:03d}'.format(idx)]['name']==name:
            rasp_sigmap[name]= idx
            rasp_signal_list[idy]= "Found"

print(rasp_sigmap)

rasp_sign_lost = False
for idy, name in enumerate(rasp_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        ada_sign_lost = True

if not rasp_sign_lost:
    print("Found all signals from Raspberry datafile")
else:
    print("Missing signals from Raspberry datafile! Exit!")
    sys.exit(1)

print("Ready for assigning values and other stuffs")
t0_rasp =rasp_data_dict['000']['data'][0]
t = np.array(rasp_data_dict['000']['data'])
t_RASP = t-t0_rasp
t_mu = 's'

if max(t_RASP) < 60:
    x_lim = [0,60]
elif max(t_RASP) < 600 :
    x_lim = [0, 600]
elif max(t_RASP) < 1200 :
    x_lim = [0, 1200]
elif max(t_RASP) < 1800 :
    x_lim = [0, 2400]
elif max(t_RASP) < 3600 :
    x_lim = [0, 3600]
else:
    t_RASP = t_RASP/60
    x_lim = [0, 60]
    t_mu = 'min.'





del t0_rasp, t
for name, pos in rasp_sigmap.items():
    statement = "v_RASP_{} = np.array(rasp_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_RASP_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del rasp_data_dict, rasp_data






print("Ready for calculate other parameters ")

# Calculated parameters

try:
    if max(v_RASP_Engine_Demand_Percent_Torque) > 100:
        v_RASP_Engine_Demand_Percent_Torque = v_RASP_Engine_Demand_Percent_Torque -125.0
except:
    pass


# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '



#########################################################
## Report section preparing figures
#########################################################
## preparing arrays for plotting ---------------
#TODO here we are with debug

# Calculated parameters






report_path = os.path.join(data_path,report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
## Temperatures plus general

fig_name = "WorkingPoints_Temperatures"
fig = plt.figure(figsize=(10,8),dpi=200)
ax1 = fig.add_subplot(211)
ax1.plot(t_RASP,v_RASP_Engine_Speed,linestyle= 'solid',color = '#FF0000FF',label=l_RASP_Engine_Speed)
# ax1.plot(t_RASP,t_RASP,linestyle= 'solid',color = '#FFFF00FF',label="t_RASP")
ax1.set_xlim(x_lim)
ax1.set_xticks(range(x_lim[0],x_lim[1],int((x_lim[1]-x_lim[0])/5)))
ax1.set_ylim([0,2500])
ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250,2500])
ax1.legend(shadow=True, loc=(LEGEND_LOWER_R),fontsize ='xx-small')
ax1.grid()
ax2 = ax1.twinx()
ax2.plot(t_RASP,v_RASP_Engine_Demand_Percent_Torque, linestyle='solid',color = '#007F00FF',label=l_RASP_Engine_Demand_Percent_Torque)
ax2.plot(t_RASP,v_RASP_Engine_Intake_Manifold_Pressure, linestyle='solid',color = '#ff0087FF',label=l_RASP_Engine_Intake_Manifold_Pressure)
ax2.plot(t_RASP,v_RASP_Engine_Boost_Pressure, linestyle='solid',color = '#ff8787FF',label=l_RASP_Engine_Boost_Pressure)
ax2.set_ylim([0,250])
ax2.set_yticks(range(0,250,25))
ax2.legend(shadow=True, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
ax1.set_title('Datalog Raspberry - '+report_name+' - working points and temperatures')
ax1.set_xlabel('Time [{}]'.format(t_mu))
ax1.set_ylabel('Engine speed [rpm]')
ax2.set_ylabel('Pressures [kPa] - Torque demand [%]')



ax3 = fig.add_subplot(212)

ax3.plot(t_RASP,v_RASP_TC_TANK,linestyle='solid',color = '#FF0000FF',label=l_RASP_TC_TANK)
ax3.plot(t_RASP,v_RASP_MDS_TRENV,linestyle='solid',color = '#00002FFF',label=l_RASP_MDS_TRENV)
ax3.plot(t_RASP,v_RASP_TC_HPH_GAS_IN,linestyle='solid',color = '#AF0000FF',label=l_RASP_TC_HPH_GAS_IN)
ax3.plot(t_RASP,v_RASP_TC_HPH_GAS_OUT,linestyle='solid',color = '#8F0000FF',label=l_RASP_TC_HPH_GAS_OUT)
ax3.plot(t_RASP,v_RASP_TC_HPH_BODY,linestyle='solid',color = '#4F0000FF',label=l_RASP_TC_HPH_BODY)
ax3.plot(t_RASP,v_RASP_MDS_TRNG_IN,linestyle='solid',color = '#00FF00FF',label=l_RASP_MDS_TRNG_IN)
ax3.plot(t_RASP,v_RASP_MDS_TRBODY,linestyle='solid',color = '#00AF00FF',label=l_RASP_MDS_TRBODY)
ax3.plot(t_RASP,v_RASP_TC_MDS_GAS_OUT,linestyle='solid',color = '#008F00FF',label=l_RASP_TC_MDS_GAS_OUT)
ax3.plot(t_RASP,v_RASP_Engine_Fuel_Temperature,linestyle='solid',color = '#004F00FF',label=l_RASP_Engine_Fuel_Temperature)
ax3.plot(t_RASP,v_RASP_TC_HPH_H2O_IN,linestyle='solid',color = '#0000FFFF',label=l_RASP_TC_HPH_H2O_IN)
ax3.plot(t_RASP,v_RASP_TC_HPH_H2O_OUT,linestyle='solid',color = '#0000AFFF',label=l_RASP_TC_HPH_H2O_OUT)
ax3.plot(t_RASP,v_RASP_MDS_TRH2O_IN,linestyle='solid',color = '#00008FFF',label=l_RASP_MDS_TRH2O_IN)
ax3.plot(t_RASP,v_RASP_MDS_TRH2O_OUT,linestyle='solid',color = '#00004FFF',label=l_RASP_MDS_TRH2O_OUT)

ax3.set_xlim(x_lim)
ax3.set_xticks(range(x_lim[0],x_lim[1],int((x_lim[1]-x_lim[0])/5)))
ax3.set_ylim([-80,120])
ax3.set_yticks(range(-80,120,20))

ax3.set_xlabel('Time [{}]'.format(t_mu))
ax3.set_ylabel('Temperatures [degC]')
ax3.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
ax3.grid()
ax4 = ax3.twinx()
ax4.plot(t_RASP,v_RASP_HPH_QH2O, linestyle='solid',color = '#7F7F003F',label=l_RASP_HPH_QH2O)
ax4.set_ylim([0,5])
ax4.set_yticks([0,0.5,1.0,1.5,2,2.5,3,3.5,4,4.5,5])
ax4.legend(shadow=False, loc=(LEGEND_LOWER_R),fontsize ='xx-small')
ax4.set_ylabel('Q Coolant [l/min]')
ax4.grid()

fig.tight_layout()
fig.savefig(os.path.join(report_path,fig_name+'.svg'))
fig.savefig(os.path.join(report_path,fig_name+'.png'))


## Pressures plus flow rates

fig_name = "WorkingPoints_Pressures"
fig = plt.figure(num=2,figsize=(int(210/25.4),int(297/25.4)),dpi=200)
gs1 = gridspec.GridSpec(nrows=3, ncols=1, left=0.15, right=0.85, wspace=0.00,hspace=0.00)
ax1 = fig.add_subplot(gs1[0, :])
ax2 = fig.add_subplot(gs1[1:3, :])

ax1.plot(t_RASP,v_RASP_Engine_Speed,linestyle= 'solid',color = '#FF0000FF',label=l_RASP_Engine_Speed)
# ax1.plot(t_RASP,t_RASP,linestyle= 'solid',color = '#FFFF00FF',label="t_RASP")
ax1.set_xlim(x_lim)
ax1.set_xticks(range(x_lim[0],x_lim[1],int((x_lim[1]-x_lim[0])/5)))
ax1.set_ylim([0,2500])
ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250,2500])
ax1.legend(shadow=True, loc=(LEGEND_LOWER_R),fontsize ='xx-small')
ax1.grid()
ax1r = ax1.twinx()
ax1r.plot(t_RASP,v_RASP_Engine_Demand_Percent_Torque, linestyle='solid',color = '#007F00FF',label=l_RASP_Engine_Demand_Percent_Torque)
ax1r.plot(t_RASP,v_RASP_Engine_Intake_Manifold_Pressure, linestyle='solid',color = '#ff0087FF',label=l_RASP_Engine_Intake_Manifold_Pressure)
ax1r.plot(t_RASP,v_RASP_Engine_Boost_Pressure, linestyle='solid',color = '#ff8787FF',label=l_RASP_Engine_Boost_Pressure)
ax1r.set_ylim([0,250])
ax1r.set_yticks(range(0,250,25))
ax1r.legend(shadow=True, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
ax1.set_title(report_name+' - working points pressures')
ax1.set_ylabel('Engine speed [rpm]')
ax1r.set_ylabel('Pressures [kPa] - Torque demand [%]')

ax2.plot(t_RASP,v_RASP_HPH_PCNG_IN,linestyle='solid',color = '#0000FFFF',label=l_RASP_HPH_PCNG_IN)
ax2.plot(t_RASP,v_RASP_MDS_PTANK,linestyle='solid',color = '#0000AFFF',label=l_RASP_MDS_PTANK)
ax2.plot(t_RASP,v_RASP_Engine_Fuel_Rate,linestyle='solid',color = '#AF0000FF',label=l_RASP_Engine_Fuel_Rate)

ax2.set_xlim(x_lim)
ax2.set_xticks(range(x_lim[0],x_lim[1],int((x_lim[1]-x_lim[0])/5)))
ax2.set_ylim([0,250])
ax2.set_yticks(range(0,250,25))


ax2r=ax2.twinx()
ax2r.plot(t_RASP,v_RASP_MDS_P1S,linestyle='solid',color = '#00AF00FF',label=l_RASP_MDS_P1S)
ax2r.plot(t_RASP,v_RASP_MDS_PGAS_OUT,linestyle='solid',color = '#008F00FF',label=l_RASP_MDS_PGAS_OUT)

ax2r.set_xlim(x_lim)
ax2r.set_xticks(range(x_lim[0],x_lim[1],int((x_lim[1]-x_lim[0])/5)))
ax2r.set_ylim([0,50])
ax2r.set_yticks(range(0,50,5))


ax2.set_xlabel('Time [{}]'.format(t_mu))

ax2.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
ax2r.legend(shadow=False, loc=(LEGEND_LOWER_R),fontsize ='xx-small')
ax2.set_ylabel('Pressures [bar g] - FlowRate [kg/h]')
ax2r.set_ylabel('Pressures [bar g]')
ax2.grid()

fig.savefig(os.path.join(report_path, fig_name + '.svg'))
fig.savefig(os.path.join(report_path, fig_name + '.png'))