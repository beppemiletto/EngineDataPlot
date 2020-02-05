
"""
Import and elaborate Aktakom russian oscilloscope data
version 03
"""
import numpy as np
import matplotlib.pyplot as plt
import os,errno
import sys
from matplotlib import colors as mcolors
from aktakom_data import Akta_Data
from mdf_data import Mdf_Data
import datetime
import pickle
from spectrum import Periodogram

import scipy.signal

def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i

# INPUT DATA AND FILES DEFINITIONS

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

data_path = "D:\\projects\\Knocking_data"
akta_filename = "Load_knock_1.txt"


report_name = "test_idle"

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



akta_data = Akta_Data(data_path,akta_filename)

akta_data_dict = akta_data.load_data()

if akta_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(2)

print('finish')

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))






#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets
akta_signal_list = [ 'time', 'CH1', 'CH2', 'CH3', 'CH4']

akta_sigmap = dict()
for idx,signal in enumerate(akta_data_dict):
    for idy, name in enumerate(akta_signal_list):
        try:
            if akta_data_dict['{:03d}'.format(idx)]['name']==name:
                akta_sigmap[name]= idx
                akta_signal_list[idy]= "Found"
        except:
            continue

print(akta_sigmap)
akta_sign_lost = False
for idy, name in enumerate(akta_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        akta_sign_lost = True

if not akta_sign_lost:
    print("Found all signals from akta_prague datafile")
else:
    print("Missing signals from akta_prague datafile! Exit!")
    sys.exit(1)


for name, pos in akta_sigmap.items():
    statement = "v_akta_{} = np.array(akta_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_akta_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

freq = akta_data_dict['f']

del akta_data_dict, akta_data

# p = Periodogram(v_akta_CH1,  sampling=9192)
#
# p.run()
#
#
# p.plot(filename='plot_ch1')
rtime = []
ch1=[]
ch2=[]
ch3=[]
ch4=[]
resample_freq = 50000
resample_period = 1/resample_freq
rt = 0.0
idx = 0
idx_old = 0
for t in v_akta_time:
    if t >= rt+resample_period:
        ch1.append(np.mean(v_akta_CH1[idx_old:idx])/1000)
        ch2.append(np.mean(v_akta_CH2[idx_old:idx])/1000)
        ch3.append(np.mean(v_akta_CH3[idx_old:idx])/1000)
        ch4.append(np.mean(v_akta_CH4[idx_old:idx])/1000)
        rtime.append(rt)
        idx_old= idx
        rt += resample_period
    idx += 1

sig_ch1 = np.array(ch1)
sig_ch2 = np.array(ch2)
sig_ch3 = np.array(ch3)
sig_ch4 = np.array(ch4)

# f, Pper_spec = scipy.signal.periodogram(v_akta_CH1,freq,'flattop', scaling='spectrum')
f, Pwelch_spec = scipy.signal.welch(sig_ch1,resample_freq, scaling='spectrum')

fig = plt.subplot(3,1,1)
plt.semilogy(f, Pwelch_spec,'b')

f, Pwelch_spec = scipy.signal.welch(sig_ch2,resample_freq, scaling='spectrum')

plt.semilogy(f, Pwelch_spec,'r')

plt.xlabel('Frequency Hz')
plt.ylabel('PSD')
# plt.grid()

f, Pwelch_spec = scipy.signal.welch(sig_ch3, resample_freq, scaling='spectrum')
fd, Pwelch_spec_d = scipy.signal.welch(sig_ch3,resample_freq,detrend= 'constant', scaling='spectrum')

plt.subplot(3,1,2)
plt.semilogy(f, Pwelch_spec,'b')
plt.semilogy(fd, Pwelch_spec_d,'b.')


f, Pwelch_spec = scipy.signal.welch(sig_ch4,resample_freq, scaling='spectrum')
fd, Pwelch_spec_d = scipy.signal.welch(sig_ch4,resample_freq, scaling='spectrum')
plt.semilogy(f, Pwelch_spec,'r')

plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
# plt.grid()

plt.subplot(3,1,3)
plt.plot(rtime,sig_ch1)
plt.xlabel('sec')
plt.ylabel('V')
plt.grid()

plt.show()






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

# # mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'esTorqueReqExt', 'zsMap', 'zsPBoost',
# #                    'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
# #                    "qsTInj", "zsTRail"]
# # akta_PRAGUE datafile parameters
# # akta_signal_list = ["recorder_time", "SPEED", "TORQUE", "ALPHA", "TWO", "T_OIL", "T_AIR", "T_pred_IC", "T_za_IC",
# #                    "T_EXH", "T_pred_Cat", "T_za_Cat", "P_OIL", "P_AIR", "P_sani", "P_za_IC", "P_EXH", "Sensyflow",
# #                    "FormulaDevice.Onlinemass_Calculation.massflow_co_diluted",
# #                    "FormulaDevice.Onlinemass_Calculation.massflow_ch4_diluted",
# #                    "FormulaDevice.Onlinemass_Calculation.massflow_thc_diluted",
# #                    "FormulaDevice.Onlinemass_Calculation.massflow_nox_diluted",
# #                    "FormulaDevice.Onlinemass_Calculation.massflow_fuel" ]
# # ## Temperatures plus general
# if len(t_akta)>=5 :
#     fig_name = "Full_Test_Temperatures"
#     print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
#     fig = plt.figure(figsize=(10,8),dpi=200)
#     ax1 = fig.add_subplot(211)
#
#     ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=l_MDF_bsRPM)
#     ax1.plot(t_akta, v_akta_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_akta_SPEED)
#     ax1.plot(t_akta,v_akta_TORQUE, linestyle='solid',color = '#007F00FF',label= l_akta_TORQUE)
#     ax1.set_xlim(x_lim)
#     ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
#     ax1.set_ylim([0,2250])
#     ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
#     ax1.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')
#     ax1.grid()
#     ax2 = ax1.twinx()
#     ax2.plot(t_MDF_zsPTank,v_MDF_zsPTank, linestyle='solid',color = '#ff0087FF',label=l_MDF_zsPTank)
#     ax2.set_ylim([0,225000])
#     ax2.set_yticks(range(0,225000,25000))
#     ax2.legend(shadow=True, loc=(LEGEND_UPPER_C),fontsize ='xx-small')
#     ax1.set_title('YaMZ V8 - '+report_name+' - Emission and temperatures')
#     ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
#     ax2.set_ylabel('Tank Pressure [mbar]')
#
#
#     ax3 = fig.add_subplot(212)
#
#     #
#     # ax3.plot(t_akta,v_akta_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_akta_T_In_Turbine_Cyl_1234)
#     # ax3.plot(t_akta,v_akta_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_akta_T_In_Turbine_Cyl_5678)
#     # ax3.plot(t_akta,v_akta_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_akta_T_In_Cat)
#     # ax3.plot(t_akta,v_akta_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_akta_T_Out_Cat)
#     ax3.plot(t_MDF_zsTExh,v_MDF_zsTExh, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsTExh)
#     ax3.plot(t_akta,v_akta_T_EXH, linestyle='solid',color = '#7F0000FF',label=l_akta_T_EXH)
#     ax3.plot(t_akta, v_akta_T_pred_Cat, linestyle='solid',color = '#00FF00FF',label=l_akta_T_pred_Cat)
#     ax3.plot(t_akta, v_akta_T_za_Cat, linestyle='solid',color = '#0000FFFF',label=l_akta_T_za_Cat)
#
#     ax3.set_xlim(x_lim)
#     ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
#     ax3.set_ylim([300,800])
#     ax3.set_yticks(range(300,800,50))
#     ax3.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')
#
#     ax3.set_xlabel('time (s)')
#     ax3.set_ylabel('Temperatures [degC]')
#     ax3.grid()
#     ax4 = ax3.twinx()
#     ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
#     ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
#     ax4.set_ylim([0.8,2.8])
#     ax4.set_yticks([0.8,1.0,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8])
#     # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
#     ax4.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
#     ax4.set_ylabel('Exhaust Lambda')
#     ax4.grid()
#
#     fig.tight_layout()
#     fig.savefig(os.path.join(report_path,fig_name+'.png'))
#     # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
#     fig.savefig(os.path.join(report_path,fig_name+'.svg'))
#     # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
#     plt.close('all')
#
# # ## Emissions plus general
# if len(t_akta)>=5 :
#     fig_name = "Full_Test_Emissions"
#     print("Generating and writing the chart {} global of ETC test in {}".format(fig_name,data_path))
#     fig = plt.figure(figsize=(10,8),dpi=200)
#     ax1 = fig.add_subplot(211)
#
#     ax1.plot(t_akta, v_akta_SPEED,linestyle= 'solid',color = '#FF7F00FF',label=l_akta_SPEED)
#     ax1.plot(t_akta,v_akta_TORQUE, linestyle='solid',color = '#007F00FF',label= l_akta_TORQUE)
#     ax1.set_xlim(x_lim)
#     ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
#     ax1.set_ylim([0,2250])
#     ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
#     ax1.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')
#     ax1.grid()
#     ax2 = ax1.twinx()
#     ax2.plot(t_MDF_zsPTank,v_MDF_zsPTank, linestyle='solid',color = '#ff0087FF',label=l_MDF_zsPTank)
#     ax2.set_ylim([0,225000])
#     ax2.set_yticks(range(0,225000,25000))
#     ax2.legend(shadow=True, loc=(LEGEND_UPPER_C),fontsize ='xx-small')
#     ax1.set_title('YaMZ V8 - '+report_name+' - Emission and temperatures')
#     ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
#     ax2.set_ylabel('Tank Pressure [mbar]')
#
#
#     ax3 = fig.add_subplot(212)
#
#     #
#     # ax3.plot(t_akta,v_akta_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_akta_T_In_Turbine_Cyl_1234)
#     # ax3.plot(t_akta,v_akta_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_akta_T_In_Turbine_Cyl_5678)
#     # ax3.plot(t_akta,v_akta_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_akta_T_In_Cat)
#     # ax3.plot(t_akta,v_akta_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_akta_T_Out_Cat)
#     ax3.plot(t_akta,v_cum_NOx, linestyle='solid',color = '#FF0000FF',label=l_cum_NOx)
#     ax3.plot(t_akta,v_cum_CO, linestyle='solid',color = '#0A0A0AFF',label=l_cum_CO)
#     ax3.plot(t_akta,v_cum_CH4, linestyle='solid',color = '#0F0FFFFF',label=l_cum_CH4)
#     ax3.plot(t_akta,v_cum_THC, linestyle='solid',color = '#0AFFFFFF',label=l_cum_THC)
#     ax3.set_xlim(x_lim)
#     ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
#     ax3.set_ylim([0, 10])
#     ax3.set_yticks(np.arange(0, 10, 0.5))
#     ax3.legend(shadow=True, loc=(LEGEND_LOWER_R),fontsize ='xx-small')
#
#     ax3.set_xlabel('time (s)')
#     ax3.set_ylabel('Cumulative emissions [g]')
#     ax3.grid()
#     ax4 = ax3.twinx()
#     ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
#     ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
#     ax4.set_ylim([0.75, 1.75])
#     ax4.set_yticks(np.arange(0.75, 1.75, 0.05))
#     # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
#     ax4.legend(shadow=False, loc=(LEGEND_UPPER_R),fontsize ='xx-small')
#     ax4.set_ylabel('Exhaust Lambda')
#     ax4.grid()
#
#     fig.tight_layout()
#     fig.savefig(os.path.join(report_path,fig_name+'.png'))
#     # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
#     fig.savefig(os.path.join(report_path,fig_name+'.svg'))
#     # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
#     plt.close('all')
#
#     for WHTC_segment in ETC_segments:
#     # ## Emissions plus general segments
#         fig_name = "Test_segment_{}_{}_seconds_Emissions".format(WHTC_segment[0],WHTC_segment[1])
#         print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
#         fig = plt.figure(figsize=(10, 8), dpi=200)
#         ax1 = fig.add_subplot(211)
#
#         ax1.plot(t_akta, v_akta_SPEED, linestyle='solid', color='#FF7F00FF', label=l_akta_SPEED)
#         ax1.plot(t_akta, v_akta_TORQUE, linestyle='solid', color='#007F00FF', label=l_akta_TORQUE)
#         ax1.set_xlim(WHTC_segment)
#         ax1.set_xticks(range(WHTC_segment[0],WHTC_segment[1], 25))
#         ax1.set_ylim([0, 2250])
#         ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250])
#         ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
#         ax1.grid()
#         ax2 = ax1.twinx()
#         ax2.plot(t_MDF_zsMap, v_MDF_zsMap, linestyle='solid', color='#ff0087FF', label=l_MDF_zsMap)
#         ax2.plot(t_MDF_zsPBoost, v_MDF_zsPBoost, linestyle='solid', color='#00ff87FF', label=l_MDF_zsPBoost)
#         ax2.set_ylim([0, 2500])
#         ax2.set_yticks(range(0, 2500, 100))
#         ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
#         ax1.set_title('YaMZ V8 - ' + report_name + ' - Emission and temperatures')
#         ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
#         ax2.set_ylabel('MAP and Boost Pressures [mbar]')
#
#         ax3 = fig.add_subplot(212)
#
#
#         ax3.plot(t_akta, v_cum_NOx, linestyle='solid', color='#FF0000FF', label=l_cum_NOx)
#         ax3.plot(t_akta, v_cum_CO, linestyle='solid', color='#0A0A0AFF', label=l_cum_CO)
#         ax3.plot(t_akta, v_cum_CH4, linestyle='solid', color='#0F0FFFFF', label=l_cum_CH4)
#         ax3.plot(t_akta, v_cum_THC, linestyle='solid', color='#0AFFFFFF', label=l_cum_THC)
#         ax3.set_xlim(WHTC_segment)
#         ax3.set_xticks(range(WHTC_segment[0],WHTC_segment[1], 25))
#         ax3.set_ylim([0,10])
#         ax3.set_yticks(np.arange(0,10,0.5))
#         ax3.legend(shadow=True, loc=(LEGEND_LOWER_R), fontsize='xx-small')
#
#         ax3.set_xlabel('time (s)')
#         ax3.set_ylabel('Cumulative emissions [g]')
#         ax3.grid()
#         ax4 = ax3.twinx()
#         ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
#         ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
#         ax4.plot(t_MDF_fsKO2, v_MDF_fsKO2, linestyle='solid', color='#7F7F7FFF', label=l_MDF_fsKO2)
#
#         ax4.set_ylim([0.75, 1.75])
#         ax4.set_yticks(np.arange(0.75,1.75,0.05))
#
#         ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
#         ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
#         ax4.set_ylabel('Exhaust Lambda')
#         ax4.grid()
#
#         fig.tight_layout()
#         fig.savefig(os.path.join(report_path, fig_name + '.png'))
#         # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
#         fig.savefig(os.path.join(report_path, fig_name + '.svg'))
#         # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
#         plt.close('all')
#


print("Exit OK")
