
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

data_path = "D:\Application_data\Report_C13\HDS9"
ada_filename = "MDS_test_ESC_20190314_ASCII.csv"
mdf_filename = "Recorder_1903141022.TXT"
esc_detect_filename = "ESC_test_MDS_C13_"
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
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
                   "qsTInj", "zsTRail"]

# ADAMO datafile parameters
ada_signal_list = [
    "Timestamp","CNG", "Pboost", "P_Intake_Manifold", "P_Inlet_Turbocharger", "P_out_Turbine", "P_out_Turbine",
    "P_Out_Cat", "Brake_speed_F", "Power", "Engine_Torque","CNG", "T_h2o", "T_in_H20_Rid",
    "T_Asp_Cyl_1", "T_Asp_Cyl_4", "T_Asp_Cyl_5", "T_amb_Box", "T_Gas_Out_Rid",
    "T_Gas_In_Rid", "T_Body_Rid","T_Air", "T_Exh_Cyl_1", "T_Exh_Cyl_2", "T_Exh_Cyl_3", "T_Exh_Cyl_4","T_Exh_Cyl_5",
    "T_Exh_Cyl_6", "T_Exh_Cyl_7", "T_Exh_Cyl_8", "T_In_Turbine_Cyl_1234", "T_In_Turbine_Cyl_5678",
    "T_In_Cat", "T_Out_Cat" , "PtankF_BOSCH"]

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

print("Ready for calculate other parameters ")

# Calculated parameters
cv_ADA_BSFC = v_ADA_CNG/v_ADA_Power*1000
cl_ADA_BSFC = "BSFC gr/kWh"


# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '


# detect ESCs

esc_detector = ESC_Detect(rpm= v_ADA_Brake_speed_F,load = v_ADA_Engine_Torque,time = t_ADA, engine_speeds=[650,1250,1400,1650],loads=[560,1050,1600,2000] , tolerance= 0.15 )
esc_seq_dict = esc_detector.detect_subcycles()
esc_seq=[]
esc_completed = []
for key, record in esc_seq_dict.items():
    esc_seq.append(record["segment"])
    esc_completed.append(record["esc_complete"])



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
    print("Generating and writing the chart {} global of ESC test in {}".format(fig_name,data_path))
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
    esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
    plt.close('all')



for esc_num in range(len(esc_seq_dict)):
    segment = esc_seq_dict['{:03d}'.format(esc_num)]['segment']
    esc_completed = esc_seq_dict['{:03d}'.format(esc_num)]['esc_complete']
    figure_1 = True
    figure_2 = True
    # Figure for General Data of performance and temperatures
    if figure_1:
        fig_name = "WorkingPoints_Temperatures_ESC_num_{}".format(esc_num+1)
        print("Generating and writing the chart 1 {} for segment {} on total {} of ESC test in {}".format(fig_name,esc_num+1,len(esc_seq_dict),data_path))
        title = "{}\n{}".format(fig_name,
                                "Simplified ESC complete" if esc_completed else "Simplified ESC NOT completed")
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)
        [x,y] =  esc_seq_segment(t_MDF_bsRPM, v_MDF_bsRPM, segment )
        ax1.plot(x,y,linestyle='solid', color='#FF0000FF', label=l_MDF_bsRPM)
        [x,y] =  esc_seq_segment(t_ADA, v_ADA_Brake_speed_F, segment)
        ax1.plot(x, y, linestyle='solid', color='#FF7F00FF', label=l_ADA_Brake_speed_F)
        [x,y] =  esc_seq_segment(t_ADA, v_ADA_Engine_Torque, segment)
        ax1.plot(x, y, linestyle='solid', color='#007F00FF', label=l_ADA_Engine_Torque)
        # ax1.set_xlim(x_lim)
        # ax1.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax1.set_ylim([0, 2500])
        ax1.set_yticks(range(0,2500,250))
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        [x,y] =  esc_seq_segment(t_MDF_zsPTank, v_MDF_zsPTank, segment)
        ax2.plot(x,y, linestyle='solid', color='#ff0087FF', label=l_MDF_zsPTank)
        ax2.set_ylim([0, 250000])
        ax2.set_yticks(range(0, 250000, 25000))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(title)
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('Tank Pressure [mbar]')

        ax3 = fig.add_subplot(212)


        [x,y] =  esc_seq_segment(t_ADA, v_ADA_T_In_Turbine_Cyl_1234, segment)
        ax3.plot(x, y, linestyle='solid', color=col_temp[1], label=l_ADA_T_In_Turbine_Cyl_1234)
        [x,y] =  esc_seq_segment(t_ADA, v_ADA_T_In_Turbine_Cyl_5678, segment)
        ax3.plot(x, y, linestyle='solid', color=col_temp[3], label=l_ADA_T_In_Turbine_Cyl_5678)
        [x,y] =  esc_seq_segment(t_ADA, v_ADA_T_In_Cat, segment)
        ax3.plot(x, y, linestyle='solid', color=col_temp[5], label=l_ADA_T_In_Cat)
        [x,y] =  esc_seq_segment(t_ADA, v_ADA_T_Out_Cat, segment)
        ax3.plot(x, y, linestyle='solid', color=col_temp[7], label=l_ADA_T_Out_Cat)
        [x,y] =  esc_seq_segment(t_MDF_zsTExh, v_MDF_zsTExh, segment)
        ax3.plot(x, y, linestyle='solid', color='#FF0000FF', label=l_MDF_zsTExh, )
        # ax3.set_xlim(x_lim)
        # ax3.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax3.set_ylim([300, 800])
        ax3.set_yticks(range(300, 800, 50))
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Temperatures [degC]')
        ax3.grid()
        ax4 = ax3.twinx()
        [x,y] =  esc_seq_segment(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, segment)
        ax4.plot(x, y, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        [x,y] =  esc_seq_segment(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, segment)
        ax4.plot(x, y, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.set_ylim([0.8, 2.8])
        ax4.set_yticks([0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8])
        # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Exhaust Lambda')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        esc_seq_dict['{:03d}'.format(esc_num)]['chart1_segment_png'] = os.path.join(report_path, fig_name + '.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        esc_seq_dict['{:03d}'.format(esc_num)]['chart1_segment_svg'] = os.path.join(report_path, fig_name + '.svg')



    if figure_2:
        fig_name = "Fuel_System_Pressure_and_Injection_ESC_num_{}".format(esc_num+1)
        print("Generating and writing the chart 2 {} for segment {} on total {} of ESC test in {}".format(fig_name,esc_num+1,len(esc_seq_dict),data_path))
        title = "{}\n{}".format(fig_name,"Simplified ESC complete" if esc_completed else "Simplified ESC NOT completed" )
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)
        [x, y] = esc_seq_segment(t_MDF_bsRPM, v_MDF_bsRPM, segment)
        ax1.plot(x, y, linestyle='solid', color='#FF0000FF', label=l_MDF_bsRPM)
        [x, y] = esc_seq_segment(t_ADA, v_ADA_Engine_Torque, segment)
        ax1.plot(x, y, linestyle='solid', color='#007F00FF', label=l_ADA_Engine_Torque)
        # ax1.set_xlim(x_lim)
        # ax1.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax1.set_ylim([0, 2500])
        ax1.set_yticks(range(0,2500,250))
        ax1.legend(shadow=True, loc=(LEGEND_LOWER_C), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        [x, y] = esc_seq_segment(t_MDF_zsTRail, v_MDF_zsTRail, segment)
        ax2.plot(x, y, linestyle='solid', color='#ff0087FF', label=l_MDF_zsTRail)
        ax2.set_ylim([-40, 60])
        ax2.set_yticks(range(-40, 60, 10))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(title)
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('Fuel Rail GAS Temperature [degC]')

        ax3 = fig.add_subplot(212)

        [x, y] = esc_seq_segment(t_ADA, v_ADA_PtankF_BOSCH, segment)
        ax3.plot(x, y*1000, linestyle='solid', color=col_temp[1], label=l_ADA_PtankF_BOSCH)
        [x, y] = esc_seq_segment(t_MDF_zsPTank, v_MDF_zsPTank, segment)
        ax3.plot(x, y, linestyle='solid', color=col_temp[3], label=l_MDF_zsPTank)
        [x, y] = esc_seq_segment(t_MDF_qsTInj, v_MDF_qsTInj, segment)
        ax3.plot(x, y, linestyle='solid', color='#FF0000FF', label=l_MDF_qsTInj, )
        # ax3.set_xlim(x_lim)
        # ax3.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax3.set_ylim([0, 225000])
        ax3.set_yticks(range(0, 225000, 25000))
        ax3.legend(shadow=True, loc=(LEGEND_LOWER_L), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('High Pressure [mbar] - Injection time [usec]')
        ax3.grid()
        ax4 = ax3.twinx()
        [x, y] = esc_seq_segment(t_MDF_zsPRail, v_MDF_zsPRail, segment)
        ax4.plot(x, y, linestyle='solid', color='#007F00FF', label=l_MDF_zsPRail)
        ax4.set_ylim([0,9000 ])
        ax4.set_yticks(range(0,9000,1000))
        # ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
        ax4.legend(shadow=False, loc=(LEGEND_UPPER_R), fontsize='xx-small')
        ax4.set_ylabel('Fuel Rail GAS Pressure [mbarA]')
        ax4.grid()

        fig.tight_layout()
        fig.savefig(os.path.join(report_path, fig_name + '.png'))
        esc_seq_dict['{:03d}'.format(esc_num)]['chart2_segment_png'] = os.path.join(report_path, fig_name + '.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        esc_seq_dict['{:03d}'.format(esc_num)]['chart2_segment_svg'] = os.path.join(report_path, fig_name + '.svg')

    plt.close('all')
esc_output_file_prefix = os.path.join(report_path,esc_detect_filename)
pickle_filename = "{}_sequence.pickle".format(esc_output_file_prefix)

with open(pickle_filename, 'wb') as pickle_file:
    pickle.dump(esc_seq_dict, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
print("Exit OK")
