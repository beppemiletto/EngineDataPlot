
"""
Import and elaborate ETC cycle
version 02 - DYNO_Prague
"""
import numpy as np
import matplotlib.pyplot as plt
import os,errno
import sys
from matplotlib import colors as mcolors
from ARAI_dyno_data import Dyno_Data
from mdf_data import Mdf_Data
from esc_cycle_detect import ESC_Detect
import datetime
import pickle

def timestr2time(timestr):
    time_zero_str = timestr.split(' ')[-1]
    time_zero_hh = float(time_zero_str.split(':')[0]) * 3600  # second from hours
    time_zero_mm = float(time_zero_str.split(':')[1]) * 60  # second from minutes
    time_zero_ss = float(time_zero_str.split(':')[2])  # second
    time_zero_ms = float(time_zero_str.split(':')[3]) / 1000  # msec
    time_zero = time_zero_hh + time_zero_mm + time_zero_ss + time_zero_ms
    return time_zero


def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i

# esc_seq_segment: return the index [i start : i end] of any kind of signal Y=f(time)
def esc_seq_segment(times,values,segment):
    """
    :type times: object 1d array float times
    :type values: object 1d array (int, float, bool) values for Y signal
    :type segment: object tuple (float time_start, float time_end)
    """
    start_found = False
    end_found = False
    t_start = segment[0]
    t_end = segment[1]
    for idx, t in enumerate(times):

        if (not start_found) and (t >= t_start):
            i_start = idx
            start_found = True
        if (not end_found) and (t >= t_end):
            i_end  = idx
            end_found = True
            break
    return [times[i_start:i_end],values[i_start:i_end]]



# INPUT DATA AND FILES DEFINITIONS

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))
engine_name = 'CRYOGAS - Ashok Leyland 5.7 '
data_path = "/home/gmiletto/projects/data_dataplot/ARAISession/ETC13"
dyno_filename = "ETC13_dyno.csv"
mdf_filename_list = ["ETC13_mdf.TXT"]
report_name = "ETC13"
mdf_time_offsets_list = [0]                        # offset time in seconds (initial points of DYNO file)

x_lim=[0,1800] ; x_tick = 100
ETC_segments=[(0,300),(300,600),(600,900),(900,1200),(1100,1500),(1400,1800)]

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

canape_data_dict_list = []
for idx, mdf_filename in enumerate(mdf_filename_list):
    canape_data = Mdf_Data(data_path,mdf_filename)
    canape_data_dict = canape_data.load_data()
    canape_data_dict_list.append(canape_data_dict)

    if canape_data_dict is None:
        print("Errore, controlla i dati di input")
        sys.exit(1)


dyno_data = Dyno_Data(data_path, dyno_filename)

dyno_data_dict = dyno_data.load_data()

if dyno_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(2)

print('finish data import')
print("starting data analysis")

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))




## Define input signal names
# CANAPE datafile parameters
mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'zsPotenzAcc', 'zsMap', 'zsPBoost',
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
                   "qsTInj", "fsKO2", "qsAutoLeanSwitch", "esQAir_Request", "qsAutoLeanSwitch", "qsQAirReqDiff",
                   "qsQAirReqLeanIn", "qsQAirReqLeanOut", "qsQAIR_INT_THR"]

# DYNO datafile parameters
dyno_signal_list = [ "TimeStamp", "SPEED", "TORQUE", "THROTTLEFB", "T_WATER_OUT", "T_OIL", "T_AIRIN", "T_BIC",
                   "TC_TURB1", "TC_BF_CAT", "TC_AF_CAT", "P_OIL", "P_EXH_BACK", "AIRFLOWRATE_DRY",  "COH_4",
                   "COL_4",  "CH4_4", "THC_4", "NOX_4", "CNG_Flow", "EXH_FLOWRATE", "ESpeedDemand", "ETorqueDemand",
                     "RT_ETHROTLDMD", "POWER_obs"]

#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets

mdf_sigmap_list = []
mdf_sigmap = dict()
for canape_data_dict in canape_data_dict_list:
    for idx,signal in enumerate(canape_data_dict):
        for idy, name in enumerate(mdf_signal_list):
            if canape_data_dict['{:03d}'.format(idx)]['name']==name:
                mdf_sigmap[name]= idx
                mdf_signal_list[idy]= "Found"
    mdf_sigmap_list.append(mdf_sigmap)

print(mdf_sigmap)

mdf_sign_lost = False
for idy, name in enumerate(mdf_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        mdf_sign_lost = True

if not mdf_sign_lost:
    print("Found all signals from Canape datafile")
else:
    print("Missing signals from Canape datafile! Exit!")
    sys.exit(1)

dyno_sigmap = dict()
for idx,signal in enumerate(dyno_data_dict):
    for idy, name in enumerate(dyno_signal_list):
        if dyno_data_dict['{:03d}'.format(idx)]['name'] == name:
            dyno_sigmap[name]= idx
            dyno_signal_list[idy]= "Found"

print(dyno_sigmap)
dyno_sign_lost = False
for idy, name in enumerate(dyno_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        dyno_sign_lost = True

if not dyno_sign_lost:
    print("Found all signals from Dyno_prague datafile")
else:
    print("Missing signals from Dyno_prague datafile! Exit!")
    sys.exit(1)

print("Ready for assigning values and other stuffs")
if len(mdf_sigmap_list)<2:
    mdf_sigmap = mdf_sigmap_list[0]
    mdf_time_offset = mdf_time_offsets_list[0]
    for name, pos in mdf_sigmap.items():
        statement = "t_MDF_{} = np.array(canape_data_dict['{:03d}']['time'])+mdf_time_offset".format(name,pos)
        print(statement)
        exec(statement)
        statement = "v_MDF_{} = np.array(canape_data_dict['{:03d}']['data'])".format(name,pos)
        print(statement)
        exec(statement)
        statement = "l_MDF_{} = '{}'".format(name, name)
        print(statement)
        exec(statement)

else:
    for name, pos in mdf_sigmap.items():
        t_segments=[]
        v_segments=[]
        for idx, mdf_sigmap in enumerate(mdf_sigmap_list):
            canape_data_dict = canape_data_dict_list[idx]
            mdf_time_offset = mdf_time_offsets_list[idx]
            statement = "t_segments.append( np.array(canape_data_dict['{:0>3d}']['time'])+mdf_time_offset)".format(pos)
            print(statement)
            exec(statement)
            statement = "v_segments.append( np.array(canape_data_dict['{:0>3d}']['data']))".format(pos)
            print(statement)
            exec(statement)
        mdf_t_statement = "t_MDF_{} = np.concatenate(t_segments)".format(name)
        exec(mdf_t_statement)
        mdf_v_statement = "v_MDF_{} = np.concatenate(v_segments)".format(name)
        exec(mdf_v_statement)

        statement = "l_MDF_{} = '{}'".format(name, name)
        print(statement)
        exec(statement)

    del t_segments, v_segments, mdf_v_statement, mdf_t_statement, canape_data_dict_list

try:
    t_CAL_qsQAIR_INT_THR = np.array([t_MDF_qsQAIR_INT_THR[0],  max(t_MDF_bsRPM)])
    v_CAL_qsQAIR_INT_THR = np.array([v_MDF_qsQAIR_INT_THR[0], v_MDF_qsQAIR_INT_THR[0]])
    qsQAIR_INT_THR_flag = True
except:
    print('v_MDF_qsQAIR_INT_THR not present')
    qsQAIR_INT_THR_flag = False

del canape_data_dict, canape_data, statement

for name, pos in dyno_sigmap.items():
    # filtering the column for timestamp that is a string not convertible directly into float
    if name == 'TimeStamp':
        timestamp_str_begin = dyno_data_dict['{:03d}'.format(pos)]['data'][0]
        time_zero = timestr2time(timestamp_str_begin)
        t = []
        time_strings = dyno_data_dict['{:03d}'.format(pos)]['data']
        for timestamp_str in time_strings:
            ti = timestr2time(timestamp_str)
            tic = ti - time_zero
            t.append(tic)
        statement = "v_DYNO_{} = np.array(t)".format(name, pos)
        del time_zero, timestamp_str, timestamp_str_begin

    else:
        statement = "v_DYNO_{} = np.array(dyno_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_DYNO_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del dyno_data_dict, dyno_data, t


t_DYNO = v_DYNO_TimeStamp
del v_DYNO_TimeStamp

print("Ready for calculate other parameters ")

# Calculate cumulative and specifc emissions


max_emx_cumul = 0
max_emx_spec = 0

power_kw = np.empty(len(t_DYNO))

for idx, power in enumerate(v_DYNO_POWER_obs):
    if power < 1.5:
        power_kw[idx] = 1.5
    else:
        power_kw[idx] = power

grh = np.empty(len(t_DYNO))
mgrkwh = np.empty(len(t_DYNO))
for idx, conc in enumerate(v_DYNO_COH_4):
    grh[idx] = 0.000966 * conc * v_DYNO_EXH_FLOWRATE[idx] # g/h value
    mgrkwh[idx] = grh[idx] * 1000 / power_kw[idx]
v_cum_CO = np.cumsum(grh)/(3600 * 10) # divider seconds in hour and frequency 10 that is the integration interval
l_cum_CO = "cum. sum. CO dil."
if np.max(v_cum_CO) > max_emx_cumul:
    max_emx_cumul = np.max(v_cum_CO)
v_spec_CO = np.array(mgrkwh)
l_spec_CO = "specific cum. sum. CO"
if np.max(v_spec_CO) > max_emx_spec:
    max_emx_spec = np.max(v_spec_CO)


grh = np.empty(len(t_DYNO))
mgrkwh = np.empty(len(t_DYNO))
for idx, conc in enumerate(v_DYNO_CH4_4):
    grh[idx] = 0.000478 * conc * v_DYNO_EXH_FLOWRATE[idx]
    mgrkwh[idx] = grh[idx] * 1000 / power_kw[idx]
v_cum_CH4 = np.cumsum(grh)/(3600 * 10)  # divider seconds in hour and frequency 10 that is the integration interval
l_cum_CH4 = "cum. sum. CH4 dil."
if np.max(v_cum_CH4) > max_emx_cumul:
    max_emx_cumul = np.max(v_cum_CH4)
v_spec_CH4 = np.array(mgrkwh)
l_spec_CH4 = "specific cum. sum. CH4"
if np.max(v_spec_CH4) > max_emx_spec:
    max_emx_spec = np.max(v_spec_CH4)

grh = np.empty(len(t_DYNO))
mgrkwh = np.empty(len(t_DYNO))
for idx, conc in enumerate(v_DYNO_NOX_4):
    grh[idx] = 0.001587 * conc * v_DYNO_EXH_FLOWRATE[idx]
    mgrkwh[idx] = grh[idx] * 1000 / power_kw[idx]

v_cum_NOx = np.cumsum(grh)/(3600 * 10)  # divider seconds in hour and frequency 10 that is the integration interval
l_cum_NOx = "cum. sum. NOx dil."
if np.max(v_cum_NOx) > max_emx_cumul:
    max_emx_cumul = np.max(v_cum_NOx)
v_spec_NOx = np.array(mgrkwh)
l_spec_NOx = "specific cum. sum. NOx"
if np.max(v_spec_NOx) > max_emx_spec:
    max_emx_spec = np.max(v_spec_NOx)

grh = np.empty(len(t_DYNO))
mgrkwh = np.empty(len(t_DYNO))
for idx, conc in enumerate(v_DYNO_THC_4):
    grh[idx] = 0.000478 * conc * v_DYNO_EXH_FLOWRATE[idx]
    mgrkwh[idx] = grh[idx] * 1000 / power_kw[idx]

v_cum_THC = np.cumsum(grh)/ (3600 * 10)  # divider seconds in hour and frequency 10 that is the integration interval
l_cum_THC = "cum. sum. THC dil."
if np.max(v_cum_THC) > max_emx_cumul:
    max_emx_cumul = np.max(v_cum_THC)
v_spec_THC = np.array(mgrkwh)
l_spec_THC = "specific cum. sum. THC"
if np.max(v_spec_THC) > max_emx_spec:
    max_emx_spec = np.max(v_spec_THC)

del idx, grh, mgrkwh

if max_emx_cumul > 200:
    y_range = [0,250]
    y_ticks = range(0,250,25)
elif max_emx_cumul > 100:
    y_range = [0, 200]
    y_ticks = range(0, 200, 20)
elif max_emx_cumul > 50:
    y_range = [0, 100]
    y_ticks = range(0, 100, 10)
elif max_emx_cumul > 25:
    y_range = [0, 50]
    y_ticks = range(0, 50, 5)
elif max_emx_cumul > 10:
    y_range = [0, 20]
    y_ticks = range(0, 20, 2)
else:
    y_range = [0, 10]
    y_ticks = range(0, 10, 1)

# Calculate the regression analysis
devs_speed = np.empty(len(t_DYNO))
for idx, speed in enumerate(v_DYNO_SPEED):
    if v_DYNO_ESpeedDemand[idx] > 0:
        dev_value_i = (speed - v_DYNO_ESpeedDemand[idx] ) / v_DYNO_ESpeedDemand[idx] * 100
        if dev_value_i > 100:
            dev_value_i = 100
        if dev_value_i < -100:
            dev_value_i = -100

        devs_speed[idx] = dev_value_i
    else:
        devs_speed[idx] = 0
        

devs_torque = np.empty(len(t_DYNO))
for idx, torque in enumerate(v_DYNO_TORQUE):
    if v_DYNO_ETorqueDemand[idx] > 0:
        dev_value_i = (torque - v_DYNO_ETorqueDemand[idx]) / v_DYNO_ETorqueDemand[idx] * 100
        if dev_value_i > 100:
            dev_value_i = 100
        if dev_value_i < -100:
            dev_value_i = -100
        devs_torque[idx] = dev_value_i
    else:
        devs_torque[idx] = 0

# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '


report_path = os.path.join(data_path,report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


# ## Temperatures plus general
if len(t_DYNO)>=5 :
    fig_name = "Full_Test_Temperatures"
    print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=l_MDF_bsRPM)
    ax1.plot(t_DYNO, v_DYNO_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_DYNO_SPEED)
    ax1.plot(t_DYNO,v_DYNO_TORQUE, linestyle='solid',color = '#007F00FF',label= l_DYNO_TORQUE)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax1.set_ylim([0,2250])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
    ax1.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_MDF_zsPTank,v_MDF_zsPTank, linestyle='solid',color = '#ff0087FF',label=l_MDF_zsPTank)
    ax2.set_ylim([0,225000])
    ax2.set_yticks(range(0,225000,25000))
    ax2.legend(shadow=True, loc=(LEGEND_UPPER_C),fontsize ='xx-small')
    ax1.set_title(engine_name + ' - '+report_name+' - Emission and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)


    ax3.plot(t_MDF_zsTExh,v_MDF_zsTExh, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsTExh)
    ax3.plot(t_DYNO,v_DYNO_TC_TURB1, linestyle='solid',color = '#7F0000FF',label=l_DYNO_TC_TURB1)
    ax3.plot(t_DYNO, v_DYNO_TC_BF_CAT, linestyle='solid',color = '#00FF00FF',label=l_DYNO_TC_BF_CAT)
    ax3.plot(t_DYNO, v_DYNO_TC_AF_CAT, linestyle='solid',color = '#0000FFFF',label=l_DYNO_TC_AF_CAT)

    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax3.set_ylim([300,800])
    ax3.set_yticks(range(300,800,50))
    ax3.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.8,2.8])
    ax4.set_yticks([0.8,1.0,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8])
    # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
    ax4.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path,fig_name+'.png'))
    # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
    plt.close('all')

# ## Regression analysis
if len(t_DYNO) >= 5:
    for ETC_segment in ETC_segments:
        fig_name = "Test_segment_{}_{}_seconds_RegressionAnalysis".format(ETC_segment[0],ETC_segment[1])
        # fig_name = "Regression_Analysis"
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_DYNO, v_DYNO_ESpeedDemand, linestyle='solid', color='#FF0000FF', label=l_DYNO_ESpeedDemand)
        ax1.plot(t_DYNO, v_DYNO_SPEED, linestyle='solid', color='#FF7F00FF', label=l_DYNO_SPEED)

        ax1.set_xlim(ETC_segment)
        ax1.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))

        ax1.set_ylim([0, 2500])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_DYNO, v_DYNO_TORQUE, linestyle='solid', color='#007F00FF', label=l_DYNO_TORQUE)
        ax2.plot(t_DYNO, v_DYNO_ETorqueDemand, linestyle='solid', color='#007FFFFF', label=l_DYNO_ETorqueDemand)
        ax2.set_ylim([0, 1000])
        ax2.set_yticks(range(0, 1000, 100))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_name + ' - ' + report_name + ' - Regression Analysis')
        ax1.set_ylabel('Engine speed [rpm]')
        ax2.set_ylabel('Torque [Nm]')

        ax3 = fig.add_subplot(212)

        ax3.plot(t_DYNO, devs_torque, linestyle='solid', color='#00FF008F', label="TORQUE DEV %")
        ax3.plot(t_DYNO, devs_speed, linestyle='solid', color='#FF0000FF', label="SPEES DEV %")

        ax3.set_xlim(ETC_segment)
        ax3.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))
        ax3.set_ylim([-100, 100])
        ax3.set_yticks([-100,-80,-60,-40,-20,0,20,40,60,80,100])
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Devation [%]')
        ax3.grid()

        ax4 = ax3.twinx()
        ax4.plot(t_DYNO, v_DYNO_RT_ETHROTLDMD, linestyle='solid', color='#7F7F00AF', label=l_DYNO_RT_ETHROTLDMD)
        ax4.set_ylim([0, 100])
        ax4.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Alpha req. [%]')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        plt.close('all')

# ## Lean management
if len(t_DYNO) >= 5:
    for ETC_segment in ETC_segments:
        fig_name = "Test_segment_{}_{}_seconds_Autolean".format(ETC_segment[0], ETC_segment[1])
        # fig_name = "Regression_Analysis"
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_DYNO, v_DYNO_SPEED, linestyle='solid', color='#FF7F00FF', label=l_DYNO_SPEED)

        ax1.set_xlim(ETC_segment)
        ax1.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))

        ax1.set_ylim([0, 2500])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_esQAir_Request, v_MDF_esQAir_Request, linestyle='solid', color='#007F00FF', label=l_MDF_esQAir_Request)
        ax2.plot(t_MDF_qsQAirReqLeanIn, v_MDF_qsQAirReqLeanIn, linestyle='solid', color='#7F0000AF', label=l_MDF_qsQAirReqLeanIn)
        ax2.plot(t_MDF_qsQAirReqLeanOut, v_MDF_qsQAirReqLeanOut, linestyle='solid', color='#00007FAF', label=l_MDF_qsQAirReqLeanOut)
        ax2.plot(t_DYNO, v_DYNO_TC_TURB1, linestyle='solid', color='#FF0000FF', label=l_DYNO_TC_TURB1)
        ax2.plot(t_DYNO, v_DYNO_ETorqueDemand, linestyle='solid', color='#007FFFFF', label=l_DYNO_ETorqueDemand)
        ax2.set_ylim([0, 1000])
        ax2.set_yticks(range(0, 1000, 100))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_name + ' - ' + report_name + ' - Lean Management')
        ax1.set_ylabel('Engine speed [rpm]')
        ax2.set_ylabel('QAirs [kg/h] - Torque [Nm]')

        ax3 = fig.add_subplot(212)

        ax3.plot(t_CAL_qsQAIR_INT_THR, v_CAL_qsQAIR_INT_THR, linestyle='solid', color='#00FF008F', label=l_MDF_qsQAIR_INT_THR)
        ax3.plot(t_MDF_qsQAirReqDiff, v_MDF_qsQAirReqDiff, linestyle='solid', color='#FF0000FF', label=l_MDF_qsQAirReqDiff)
        ax3.plot(t_MDF_qsAutoLeanSwitch, v_MDF_qsAutoLeanSwitch * 1000000, linestyle='solid', color='#000000FF', label=l_MDF_qsAutoLeanSwitch)

        ax3.set_xlim(ETC_segment)
        ax3.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))
        ax3.set_ylim([-2000000, 2000000])
        ax3.set_yticks(range(-2000000, 2000000, 200000))
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Integral Qair [kg/h]')
        ax3.grid()

        ax4 = ax3.twinx()
        ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.set_ylim([0.75, 1.75])
        ax4.set_yticks(np.arange(0.75, 1.75, 0.05))
        # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Exhaust Lambda')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        plt.close('all')

# ## Emissions plus general
if len(t_DYNO)>=5 :
    fig_name = "Full_Test_Emissions"
    print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_DYNO, v_DYNO_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_DYNO_SPEED)
    ax1.plot(t_DYNO,v_DYNO_TORQUE, linestyle='solid',color = '#007F00FF',label= l_DYNO_TORQUE)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax1.set_ylim([0,2250])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
    ax1.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_MDF_zsPTank,v_MDF_zsPTank, linestyle='solid',color = '#ff0087FF',label=l_MDF_zsPTank)
    ax2.set_ylim([0,225000])
    ax2.set_yticks(range(0,225000,25000))
    ax2.legend(shadow=True, loc=(LEGEND_UPPER_C),fontsize ='xx-small')
    ax1.set_title(engine_name + ' - '+report_name+' - Emission and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)

    ax3.plot(t_DYNO,v_cum_NOx, linestyle='solid',color = '#FF0000FF',label=l_cum_NOx)
    ax3.plot(t_DYNO,v_cum_CO, linestyle='solid',color = '#0A0A0AFF',label=l_cum_CO)
    ax3.plot(t_DYNO,v_cum_CH4, linestyle='solid',color = '#0F0FFFFF',label=l_cum_CH4)
    ax3.plot(t_DYNO,v_cum_THC, linestyle='solid',color = '#0AFFFFFF',label=l_cum_THC)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax3.set_ylim(y_range)
    ax3.set_yticks(y_ticks)
    ax3.legend(shadow=True, loc=(LEGEND_LOWER_R),fontsize ='xx-small')

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Cumulative emissions [g]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.75, 1.75])
    ax4.set_yticks(np.arange(0.75, 1.75, 0.05))
    # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
    ax4.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path,fig_name+'.png'))
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    plt.close('all')

    for ETC_segment in ETC_segments:
    # ## Emissions plus general segments
        fig_name = "Test_segment_{}_{}_seconds_Emissions".format(ETC_segment[0],ETC_segment[1])
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_DYNO, v_DYNO_SPEED, linestyle='solid', color='#FF7F00FF', label=l_DYNO_SPEED)
        ax1.plot(t_DYNO, v_DYNO_TORQUE, linestyle='solid', color='#007F00FF', label=l_DYNO_TORQUE)
        ax1.set_xlim(ETC_segment)
        ax1.set_xticks(range(ETC_segment[0],ETC_segment[1], 25))
        ax1.set_ylim([0, 2250])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250])
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_zsMap, v_MDF_zsMap, linestyle='solid', color='#ff0087FF', label=l_MDF_zsMap)
        ax2.plot(t_MDF_zsPBoost, v_MDF_zsPBoost, linestyle='solid', color='#00ff87FF', label=l_MDF_zsPBoost)
        ax2.set_ylim([0, 2500])
        ax2.set_yticks(range(0, 2500, 100))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_name + ' - ' + report_name + ' - Emission and temperatures')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('MAP and Boost Pressures [mbar]')

        ax3 = fig.add_subplot(212)


        ax3.plot(t_DYNO, v_cum_NOx, linestyle='solid', color='#FF0000FF', label=l_cum_NOx)
        ax3.plot(t_DYNO, v_cum_CO, linestyle='solid', color='#0A0A0AFF', label=l_cum_CO)
        ax3.plot(t_DYNO, v_cum_CH4, linestyle='solid', color='#0F0FFFFF', label=l_cum_CH4)
        ax3.plot(t_DYNO, v_cum_THC, linestyle='solid', color='#0AFFFFFF', label=l_cum_THC)
        ax3.set_xlim(ETC_segment)
        ax3.set_xticks(range(ETC_segment[0],ETC_segment[1], 25))
        ax3.set_ylim(y_range)
        ax3.set_yticks(y_ticks)
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_R), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Cumulative emissions [g]')
        ax3.grid()
        ax4 = ax3.twinx()
        ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.plot(t_MDF_fsKO2, v_MDF_fsKO2, linestyle='solid', color='#7F7F7FFF', label=l_MDF_fsKO2)

        ax4.set_ylim([0.75, 1.75])
        ax4.set_yticks(np.arange(0.75,1.75,0.05))

        ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Exhaust Lambda')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
        plt.close('all')

    # SPECIFIC EMISSIONS
    for ETC_segment in ETC_segments:
        # ## Emissions plus general segments
        fig_name = "Test_segment_{}_{}_seconds_Specific_EMX".format(ETC_segment[0], ETC_segment[1])
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_DYNO, v_DYNO_SPEED, linestyle='solid', color='#FF7F00FF', label=l_DYNO_SPEED)
        ax1.set_xlim(ETC_segment)
        ax1.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))
        ax1.set_ylim([0, 2250])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250])
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_DYNO, power_kw, linestyle='solid', color='#007F00FF', label=l_DYNO_POWER_obs)
        ax2.set_ylim([0, 250])
        ax2.set_yticks(range(0, 250, 10))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_name + ' - ' + report_name + ' - Specific Emissions')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('Power [kW]')

        ax3 = fig.add_subplot(212)

        ax3.plot(t_DYNO, v_spec_NOx, linestyle='solid', color='#FF0000FF', label=l_spec_NOx)
        ax3.plot(t_DYNO, v_spec_CO, linestyle='solid', color='#0A0A0AFF', label=l_spec_CO)
        ax3.plot(t_DYNO, v_spec_CH4, linestyle='solid', color='#0F0FFFFF', label=l_spec_CH4)
        ax3.plot(t_DYNO, v_spec_THC, linestyle='solid', color='#0AFFFFFF', label=l_spec_THC)
        ax3.set_xlim(ETC_segment)
        ax3.set_xticks(range(ETC_segment[0], ETC_segment[1], 25))
        # ax3.set_ylim(y_range)
        # ax3.set_yticks(y_ticks)
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_R), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Specifc emissions [mg/kWh]')
        ax3.grid()
        ax4 = ax3.twinx()
        ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.plot(t_MDF_fsKO2, v_MDF_fsKO2, linestyle='solid', color='#7F7F7FFF', label=l_MDF_fsKO2)

        ax4.set_ylim([0.75, 1.75])
        ax4.set_yticks(np.arange(0.75, 1.75, 0.05))

        ax3.legend(shadow=False, loc=(4), fontsize='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Exhaust Lambda')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        plt.close('all')

    for ETC_segment in ETC_segments:

        fig_name = "Tseg_{}_{}_Spec_Detailed_EMX".format(ETC_segment[0], ETC_segment[1])
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))

        fig, ax = plt.subplots(figsize=(11.69,8.27 ), dpi=300)
        fig.subplots_adjust(right=0.75)

        twin1 = ax.twinx()
        twin2 = ax.twinx()

        # Offset the right spine of twin2.  The ticks and label have already been
        # placed on the right by twinx above.

        twin2.spines['right'].set_position(("axes", 1.06))

        # twin2.spines.right.set_position(("axes", 1.2))

        p1, = ax.plot(t_DYNO, v_DYNO_SPEED, "b-", label=l_DYNO_SPEED)
        p11, = ax.plot(t_DYNO, v_DYNO_TORQUE, "c-", label=l_DYNO_TORQUE)
        p2, = twin1.plot(t_DYNO, v_spec_CH4, "r-", label=l_spec_CH4)
        p22, = twin1.plot(t_DYNO, v_spec_THC, "r-", label=l_spec_THC)
        p3, = twin2.plot(t_DYNO, v_spec_NOx, "g-", label=l_spec_NOx)
        p33, = twin2.plot(t_DYNO, v_spec_CO, "m-", label=l_spec_CO)

        ax.set_xlim(ETC_segment)
        # ax.set_ylim(0, 2400)
        # ax.set_yticks([0, 400, 800, 1200, 1600, 2000, 2400])
        # twin1.set_ylim(0, 120)
        # twin2.set_ylim(0, 240)
        # twin2.set_yticks([0, 40, 80, 120, 160, 200, 240])

        ax.set_xlabel("time [s]")
        ax.set_ylabel("Engine Speed [rpm]")
        twin1.set_ylabel("CH4 - THC")
        twin2.set_ylabel("NOx - CO")

        ax.yaxis.label.set_color(p1.get_color())
        twin1.yaxis.label.set_color(p2.get_color())
        twin2.yaxis.label.set_color(p3.get_color())

        tkw = dict(size=4, width=1.5)
        ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
        twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        ax.tick_params(axis='x', **tkw)
        ax.grid()

        ax.legend(handles=[p1, p11, p2, p3, p33])

        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        plt.close('all')

print("Exit OK")
