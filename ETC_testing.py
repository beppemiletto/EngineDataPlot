
"""
Import and elaborate ETC cycle
version 02 - TUV_Prague
"""
import numpy as np
import matplotlib.pyplot as plt
import os,errno
import sys
from matplotlib import colors as mcolors
from tuv_data import Tuv_Data
from mdf_data import Mdf_Data
from esc_cycle_detect import ESC_Detect
import datetime
import pickle

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

data_path = "D:\\Application_data\\yamzv8data\\TUV_Prague_Tests\\2019-08-Wisetime"
tuv_filename = "20190808_ETC_1929.txt"
mdf_filename_list = ["MDF_20190808_ETC_1929.txt"]
mdf_time_offsets_list = [18.945-53.25]                        # offset time in seconds (initial points of TUV file)
esc_detect_filename = "ESC_test_MDS_C13_"

x_lim=[0,1800] ; x_tick = 100
ETC_segments=[(0,300),(300,600),(600,900),(900,1200),(1200,1500),(1500,1800)]
report_name = "ETC_1929"

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


tuv_prague_data = Tuv_Data(data_path,tuv_filename)

tuv_prague_data_dict = tuv_prague_data.load_data()

if tuv_prague_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(2)

print('finish')

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))




## Define input signal names
# CANAPE datafile parameters
mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'esTorqueReqExt', 'zsMap', 'zsPBoost',
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
                   "qsTInj", "zsTRail", "fsKO2"]

# TUV_PRAGUE datafile parameters
tuv_signal_list = ["recorder_time", "SPEED", "TORQUE", "ALPHA", "TWO", "T_OIL", "T_AIR", "T_pred_IC", "T_za_IC",
                   "T_EXH", "T_pred_Cat", "T_za_Cat", "P_OIL", "P_AIR", "P_sani", "P_za_IC", "P_EXH", "Sensyflow",
                   "massflow_co_diluted",
                   "massflow_ch4_diluted",
                   "massflow_thc_diluted",
                   "massflow_nox_diluted",
                   "massflow_fuel" ]

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

tuv_sigmap = dict()
for idx,signal in enumerate(tuv_prague_data_dict):
    for idy, name in enumerate(tuv_signal_list):
        if tuv_prague_data_dict['{:03d}'.format(idx)]['name']==name:
            tuv_sigmap[name]= idx
            tuv_signal_list[idy]= "Found"

print(tuv_sigmap)
tuv_sign_lost = False
for idy, name in enumerate(tuv_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        tuv_sign_lost = True

if not tuv_sign_lost:
    print("Found all signals from Tuv_prague datafile")
else:
    print("Missing signals from Tuv_prague datafile! Exit!")
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






del canape_data_dict, canape_data, statement

for name, pos in tuv_sigmap.items():
    statement = "v_TUV_{} = np.array(tuv_prague_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_TUV_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del tuv_prague_data_dict, tuv_prague_data


t_TUV = v_TUV_recorder_time / 1000 ## TUV_PRAGUE datafile time in seconds
del v_TUV_recorder_time

print("Ready for calculate other parameters ")

v_cum_CO = np.cumsum(v_TUV_massflow_co_diluted)/1e+06
l_cum_CO = "cum. sum. CO dil."
v_cum_CH4 = np.cumsum(v_TUV_massflow_ch4_diluted)/1e+06
l_cum_CH4 = "cum. sum. CH4 dil."
v_cum_NOx = np.cumsum(v_TUV_massflow_nox_diluted)/1e+06
l_cum_NOx = "cum. sum. NOx dil."
v_cum_THC = np.cumsum(v_TUV_massflow_thc_diluted)/1e+06
l_cum_THC = "cum. sum. THC dil."


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

# mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'esTorqueReqExt', 'zsMap', 'zsPBoost',
#                    'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
#                    "qsTInj", "zsTRail"]
# TUV_PRAGUE datafile parameters
# tuv_signal_list = ["recorder_time", "SPEED", "TORQUE", "ALPHA", "TWO", "T_OIL", "T_AIR", "T_pred_IC", "T_za_IC",
#                    "T_EXH", "T_pred_Cat", "T_za_Cat", "P_OIL", "P_AIR", "P_sani", "P_za_IC", "P_EXH", "Sensyflow",
#                    "FormulaDevice.Onlinemass_Calculation.massflow_co_diluted",
#                    "FormulaDevice.Onlinemass_Calculation.massflow_ch4_diluted",
#                    "FormulaDevice.Onlinemass_Calculation.massflow_thc_diluted",
#                    "FormulaDevice.Onlinemass_Calculation.massflow_nox_diluted",
#                    "FormulaDevice.Onlinemass_Calculation.massflow_fuel" ]
# ## Temperatures plus general
if len(t_TUV)>=5 :
    fig_name = "Full_Test_Temperatures"
    print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=l_MDF_bsRPM)
    ax1.plot(t_TUV, v_TUV_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_TUV_SPEED)
    ax1.plot(t_TUV,v_TUV_TORQUE, linestyle='solid',color = '#007F00FF',label= l_TUV_TORQUE)
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
    ax1.set_title('YaMZ V8 - '+report_name+' - Emission and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)

    #
    # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_TUV_T_In_Turbine_Cyl_1234)
    # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_TUV_T_In_Turbine_Cyl_5678)
    # ax3.plot(t_TUV,v_TUV_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_TUV_T_In_Cat)
    # ax3.plot(t_TUV,v_TUV_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_TUV_T_Out_Cat)
    ax3.plot(t_MDF_zsTExh,v_MDF_zsTExh, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsTExh)
    ax3.plot(t_TUV,v_TUV_T_EXH, linestyle='solid',color = '#7F0000FF',label=l_TUV_T_EXH)
    ax3.plot(t_TUV, v_TUV_T_pred_Cat, linestyle='solid',color = '#00FF00FF',label=l_TUV_T_pred_Cat)
    ax3.plot(t_TUV, v_TUV_T_za_Cat, linestyle='solid',color = '#0000FFFF',label=l_TUV_T_za_Cat)

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

# ## Emissions plus general
if len(t_TUV)>=5 :
    fig_name = "Full_Test_Emissions"
    print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_TUV, v_TUV_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_TUV_SPEED)
    ax1.plot(t_TUV,v_TUV_TORQUE, linestyle='solid',color = '#007F00FF',label= l_TUV_TORQUE)
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
    ax1.set_title('YaMZ V8 - '+report_name+' - Emission and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)

    #
    # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_TUV_T_In_Turbine_Cyl_1234)
    # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_TUV_T_In_Turbine_Cyl_5678)
    # ax3.plot(t_TUV,v_TUV_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_TUV_T_In_Cat)
    # ax3.plot(t_TUV,v_TUV_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_TUV_T_Out_Cat)
    ax3.plot(t_TUV,v_cum_NOx, linestyle='solid',color = '#FF0000FF',label=l_cum_NOx)
    ax3.plot(t_TUV,v_cum_CO, linestyle='solid',color = '#0A0A0AFF',label=l_cum_CO)
    ax3.plot(t_TUV,v_cum_CH4, linestyle='solid',color = '#0A0A7FFF',label=l_cum_CH4)
    ax3.plot(t_TUV,v_cum_THC, linestyle='solid',color = '#0A0AFFFF',label=l_cum_THC)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    # ax3.set_ylim([300,800])
    # ax3.set_yticks(range(300,800,50))
    ax3.legend(shadow=True, loc=(LEGEND_LOWER_R),fontsize ='xx-small')

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Cumulative emissions [g]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.75,1.75])
    ax4.set_yticks([0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75])
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

    for ETC_segment in ETC_segments:
    # ## Emissions plus general segments
        fig_name = "Test_segment_{}_{}_seconds_Emissions".format(ETC_segment[0],ETC_segment[1])
        print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_TUV, v_TUV_SPEED, linestyle='solid', color='#FF7F00FF', label=l_TUV_SPEED)
        ax1.plot(t_TUV, v_TUV_TORQUE, linestyle='solid', color='#007F00FF', label=l_TUV_TORQUE)
        ax1.set_xlim(ETC_segment)
        ax1.set_xticks(range(ETC_segment[0],ETC_segment[1], 25))
        ax1.set_ylim([0, 2250])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250])
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_zsMap, v_MDF_zsMap, linestyle='solid', color='#ff0087FF', label=l_MDF_zsMap)
        ax2.set_ylim([0, 2500])
        ax2.set_yticks(range(0, 2500, 100))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title('YaMZ V8 - ' + report_name + ' - Emission and temperatures')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('Tank Pressure [mbar]')

        ax3 = fig.add_subplot(212)

        #
        # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_TUV_T_In_Turbine_Cyl_1234)
        # ax3.plot(t_TUV,v_TUV_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_TUV_T_In_Turbine_Cyl_5678)
        # ax3.plot(t_TUV,v_TUV_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_TUV_T_In_Cat)
        # ax3.plot(t_TUV,v_TUV_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_TUV_T_Out_Cat)
        ax3.plot(t_TUV, v_cum_NOx, linestyle='solid', color='#FF0000FF', label=l_cum_NOx)
        ax3.plot(t_TUV, v_cum_CO, linestyle='solid', color='#0A0A0AFF', label=l_cum_CO)
        ax3.plot(t_TUV, v_cum_CH4, linestyle='solid', color='#0A0A7FFF', label=l_cum_CH4)
        ax3.plot(t_TUV, v_cum_THC, linestyle='solid', color='#0A0AFFFF', label=l_cum_THC)
        ax3.set_xlim(ETC_segment)
        ax3.set_xticks(range(ETC_segment[0],ETC_segment[1], 25))
        # ax3.set_ylim([300,800])
        # ax3.set_yticks(range(300,800,50))
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_R), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Cumulative emissions [g]')
        ax3.grid()
        ax4 = ax3.twinx()
        ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.plot(t_MDF_fsKO2, v_MDF_fsKO2, linestyle='solid', color='#7F7F7FFF', label=l_MDF_fsKO2)

        ax4.set_ylim([0.75, 1.75])
        ax4.set_yticks(
            [0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65,
             1.7, 1.75])
        # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Exhaust Lambda')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
        plt.close('all')



print("Exit OK")
