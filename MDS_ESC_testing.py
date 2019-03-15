
"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import os,errno
import sys
from matplotlib import colors as mcolors
from ada_data import Ada_Data
from mdf_data import Mdf_Data
from esc_cycle_detect import ESC_Detect
import datetime

def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i

# INPUT DATA AND FILES DEFINITIONS

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

data_path = "D:\Application_data\Report_C13\HDS9"
ada_filename = "MDS_test_ESC_20190314_ASCII.csv"
mdf_filename = "Recorder_1903141022.TXT"
AM_toff= -162.70
AE_toff=100
x_lim=[0,8500] ; x_tick = 500
report_name = "MDS_ESC_Testing_report"

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

canape_data = Mdf_Data(data_path,mdf_filename)

canape_data_dict = canape_data.load_data()

if canape_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(1)


adamo_data = Ada_Data(data_path,ada_filename)

adamo_data_dict = adamo_data.load_data()

if adamo_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(2)

print('finish')

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))




## Define input signal names
# CANAPE datafile parameters
mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'esTorqueReqExt', 'zsMap', 'zsPBoost',
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank" ]

# ADAMO datafile parameters
ada_signal_list = [
    "Timestamp","CNG", "Pboost", "P_Intake_Manifold", "P_Inlet_Turbocharger", "P_out_Turbine", "P_out_Turbine",
    "P_Out_Cat", "Brake_speed_F", "Power", "Engine_Torque","CNG", "T_h2o", "T_in_H20_Rid",
    "T_Asp_Cyl_1", "T_Asp_Cyl_4", "T_Asp_Cyl_5", "T_amb_Box", "T_Gas_Out_Rid",
    "T_Gas_In_Rid", "T_Body_Rid","T_Air", "T_Exh_Cyl_1", "T_Exh_Cyl_2", "T_Exh_Cyl_3", "T_Exh_Cyl_4","T_Exh_Cyl_5",
    "T_Exh_Cyl_6", "T_Exh_Cyl_7", "T_Exh_Cyl_8", "T_In_Turbine_Cyl_1234", "T_In_Turbine_Cyl_5678",
    "T_In_Cat", "T_Out_Cat"                   ]

#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets

mdf_sigmap = dict()
for idx,signal in enumerate(canape_data_dict):
    for idy, name in enumerate(mdf_signal_list):
        if canape_data_dict['{:03d}'.format(idx)]['name']==name:
            mdf_sigmap[name]= idx
            mdf_signal_list[idy]= "Found"

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

ada_sigmap = dict()
for idx,signal in enumerate(adamo_data_dict):
    for idy, name in enumerate(ada_signal_list):
        if adamo_data_dict['{:03d}'.format(idx)]['name']==name:
            ada_sigmap[name]= idx
            ada_signal_list[idy]= "Found"

print(ada_sigmap)
ada_sign_lost = False
for idy, name in enumerate(ada_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        ada_sign_lost = True

if not ada_sign_lost:
    print("Found all signals from Adamo datafile")
else:
    print("Missing signals from Adamo datafile! Exit!")
    sys.exit(1)

print("Ready for assigning values and other stuffs")
for name, pos in mdf_sigmap.items():
    statement = "t_MDF_{} = np.array(canape_data_dict['{:03d}']['time'])+AM_toff".format(name,pos)
    print(statement)
    exec(statement)
    statement = "v_MDF_{} = np.array(canape_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_MDF_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del canape_data_dict, canape_data

for name, pos in ada_sigmap.items():
    statement = "v_ADA_{} = np.array(adamo_data_dict['{:03d}']['data'])".format(name,pos)
    print(statement)
    exec(statement)
    statement = "l_ADA_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del adamo_data_dict, adamo_data


t_ADA = v_ADA_Timestamp-v_ADA_Timestamp[0] ## ADAMO datafile time

print("Ready for calcualate other pars ")

# Calculated parameters
cv_ADA_BSFC = v_ADA_CNG/v_ADA_Power*1000
cl_ADA_BSFC = "BSFC gr/kWh"


# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '


# detect ESCs
esc_detector = ESC_Detect(rpm= v_ADA_Brake_speed_F,load = v_ADA_Engine_Torque,time = t_ADA, engine_speeds=[650,1250,1400,1650],loads=[560,1050,1600,2000] , tolerance= 0.15)
esc_seq = esc_detector.detect_subcycles()


report_path = os.path.join(data_path,report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# ## Temperatures plus general
if len(t_ADA)>=5 :
    fig_name = "Full_Test_WorkingPoints_Temperatures"
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)
    ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=l_MDF_bsRPM)
    ax1.plot(t_ADA, v_ADA_Brake_speed_F,linestyle= 'solid',color = '#FF7F00FF',label=l_ADA_Brake_speed_F)
    ax1.plot(t_ADA,v_ADA_Engine_Torque, linestyle='solid',color = '#007F00FF',label= l_ADA_Engine_Torque)
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
    ax1.set_title('PAIER - '+report_name+' - working points and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)


    ax3.plot(t_ADA,v_ADA_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_ADA_T_In_Turbine_Cyl_1234)
    ax3.plot(t_ADA,v_ADA_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_ADA_T_In_Turbine_Cyl_5678)
    ax3.plot(t_ADA,v_ADA_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_ADA_T_In_Cat)
    ax3.plot(t_ADA,v_ADA_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_ADA_T_Out_Cat)
    ax3.plot(t_MDF_zsTExh,v_MDF_zsTExh, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsTExh,)
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
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))

## Environmental plus combustion
# if len(t_ADA)>=5:
#     fig_name = "PowerSteady_Environment_Combustion"
#     fig = plt.figure(figsize=(10,12),dpi=200)
#     ax1 = fig.add_subplot(311)
#     ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=canape_data_dict['{:03d}'.format(mdf_sigmap['bsRPM]['name'])
#     ax1.plot(t_ADA, v_ADA_RPM,linestyle= 'solid',color = '#FF7F00FF',label=ADA_dict[6]['name'])
#     ax1.plot(t_ADA,v_ADA_Torque, linestyle='solid',color = '#007F00FF',label=ADA_dict[7]['name'])
#     ax1.plot(t_MDF_vsTorqueReqVCM2,v_MDF_vsTorqueReqVCM2, linestyle='solid',color = '#2F2F2FFF',label=canape_data_dict['{:03d}'.format(mdf_sigmap['vsTorqueReqVCM2]['name'])
#     ax1.set_xlim(x_lim)
#     ax1.set_xticks(range(x_lim[0],x_lim[1],120))
#     ax1.set_ylim([0,2250])
#     ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
#     ax1.legend(shadow=True, loc=(8),fontsize ='xx-small')
#     ax1.grid()
#     ax2 = ax1.twinx()
#     ax2.plot(t_ADA,v_ADA_PowerKW, linestyle='solid',color = '#ff0087FF',label=ADA_dict[4]['name'])
#     ax2.plot(t_ADA,cv_ADA_BSFC, linestyle='solid',color = '#7e0640FF',label=cl_ADA_BSFC)
#     ax2.set_ylim([0,450])
#     ax2.set_yticks(range(0,450,50))
#     ax2.legend(shadow=True, loc=(9),fontsize ='xx-small')
# ax1.set_title('Konzhak - '+report_name+' - Environmental and Combustion')
#     ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
#     ax2.set_ylabel('Engine Power [kW]/ BSFC [g/kWh]')
#
#
#     ax3 = fig.add_subplot(312)
#
#     ax3.plot(t_MDF_zsPBoost,v_MDF_zsPBoost, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsPBoost)
#     ax3.plot(t_ADA,v_ADA_Pboost, linestyle='solid',color = '#AF0000FF',label=l_ADA_Pboost)
#     ax3.plot(t_MDF_zsMap,v_MDF_zsMap, linestyle='solid',color = '#00007FFF',label=l_MDF_zsMap)
#     ax3.plot(t_ADA,v_ADA_P_Intake_Manifold, linestyle='solid',color = '#00008FFF',label=l_ADA_P_Intake_Manifold)
#     ax3.plot(t_ADA,v_ADA_P_Inlet_Turbocharger, linestyle='solid',color = '#b26f19FF',label=l_ADA_P_Inlet_Turbocharger)
#     ax3.plot(t_ADA,v_ADA_P_out_Turbine, linestyle='solid',color = '#553915FF',label=l_ADA_P_out_Turbine)
#     ax3.plot(t_ADA,v_ADA_P_In_Cat, linestyle='solid',color = '#1e6315FF',label=l_ADA_P_In_Cat)
#     ax3.plot(t_ADA,v_ADA_P_Out_Cat, linestyle='solid',color = '#24a614FF',label=l_ADA_P_Out_Cat)
#
#     ax3.set_xlim(x_lim)
#     ax3.set_xticks(range(x_lim[0],x_lim[1],120))
#     ax3.set_ylim([0,3000])
#     ax3.set_yticks(range(0,3000,250))
#
#     ax3.set_xlabel('time (s)')
#     ax3.set_ylabel('Pressures [mbar]')
#     ax3.grid()
#     ax4 = ax3.twinx()
#     ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=canape_data_dict['{:03d}'.format(mdf_sigmap['zsUegoLambda]['name'])
#     ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=canape_data_dict['{:03d}'.format(mdf_sigmap['qsLamObtFin]['name'])
#     ax4.set_ylim([0.8,2.0])
#     ax4.set_yticks([0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8])
#     ax3.legend(shadow=False, loc=(3),fontsize ='xx-small')
#     ax4.legend(shadow=False, loc=(4),fontsize ='xx-small')
#     ax4.set_ylabel('Exhaust Lambda')
#     ax4.grid()
#
#     ax3 = fig.add_subplot(313)
#
#
#     ax3.plot(t_MDF_zsTAir,v_MDF_zsTAir, linestyle='solid',color = '#0b6eceFF',label=l_MDF_zsTAir)
#     ax3.plot(t_MDF_zsTh2o,v_MDF_zsTh2o, linestyle='solid',color = '#a82c1bFF',label=l_MDF_zsTh2o)
#     ax3.plot(t_MDF_zsTRail,v_MDF_zsTRail, linestyle='solid',color = '#13800dFF',label=l_MDF_zsTRail)
#     ax3.plot(t_ADA,v_ADA_T_Air_Env, linestyle='solid',color = '#878dffFF',label=l_ADA_T_Air_Env)
#     ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_1, linestyle='solid',color = '#ff15ce9F',label=l_ADA_T_Asp_Cyl_1)
#     ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_4, linestyle='solid',color = '#ff15ceCF',label=l_ADA_T_Asp_Cyl_4)
#     ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_1, linestyle='solid',color = '#0d10809F',label=l_ADA_T_Asp_Cyl_5)
#     ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_4, linestyle='solid',color = '#0d1080CF',label=l_ADA_T_Asp_Cyl_8)
#     ax3.plot(t_ADA,v_ADA_T_Body_Reg, linestyle='solid',color = '#31b62bCF',label=l_ADA_T_Body_Reg)
#     ax3.plot(t_ADA,v_ADA_T_Gas_Out_Rid, linestyle='solid',color = '#103b0eCF',label=l_ADA_T_Gas_Out_Rid)
#     ax3.set_xlim(x_lim)
#     ax3.set_xticks(range(x_lim[0],x_lim[1],120))
#     ax3.set_ylim([-40,120])
#     ax3.set_yticks(range(-40,120,10))
#
#     ax3.set_xlabel('time (s)')
#     ax3.set_ylabel('Temperatures [degC]')
#     ax3.grid()
#     ax4 = ax3.twinx()
#     ax4.plot(t_MDF_jsAdv,v_MDF_jsAdv, linestyle='solid',color = '#ff04004F',label=l_MDF_jsAdv)
#     ax4.plot(t_MDF_jsAdvBase,v_MDF_jsAdvBase, linestyle='solid',color = '#bf0400CF',label=l_MDF_jsAdvBase)
#
#     ax4.set_ylim([-20,60])
#     ax4.set_yticks(range(-20,60,10))
#     ax3.legend(shadow=False, loc=(3),fontsize ='xx-small')
#     ax4.legend(shadow=False, loc=(4),fontsize ='xx-small')
#     ax4.set_ylabel('Spark Advance [deg BTDC]')
#     ax4.grid()
#
#     fig.tight_layout()
#     fig.savefig(os.path.join(report_path,fig_name+'.svg'))
#     fig.savefig(os.path.join(report_path,fig_name+'.png'))
#
#
#
print("Exit OK")