"""
Power Curve Data Analysis and Graphics
"""
import bisect
import collections
import csv
import datetime
import errno
import os
import pickle
import sys

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from ada_data import Ada_Data
from mdf_data import Mdf_Data


def row_count(input_data_file):
    with open(input_data_file) as f:
        for i, l in enumerate(f):
            pass
    return i


# INPUT DATA AND FILES DEFINITIONS
now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

engine_name = 'Isuzu 4HK1 NG '
data_path: str = "D:\Application_data\ISUZU_4HK1\WHSC_testing"
ada_filename = "WH_MAPPING_Isuzu_4HK1_01_ADA.ASCII"
mdf_filename = "WH_MAPPING_Isuzu_4HK1_01_MDF.txt"

num_cyls = 4  # conf of cylinders of engine, for plotting the exhaust temperatures of single cylinder

# creating a range of cluster for aggregating on engine speed
PowCurveRPM_min = 800
PowCurveRPM_max = 3000
PowCurveRPM_stp = 100

canape_data = Mdf_Data(data_path, mdf_filename)

canape_data_dict = canape_data.load_data()

if canape_data_dict is None:
    print("Error, control input data")
    sys.exit(1)

adamo_data = Ada_Data(data_path, ada_filename)

adamo_data_dict = adamo_data.load_data()

if adamo_data_dict is None:
    print("Error, control input data")
    sys.exit(2)

print('finish')

EMX_file = ""
LEGEND_BEST = 0
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

AM_toff = -5

x_lim = [0, 360]  # time
x_step = 60
rpm_lim = [PowCurveRPM_min, PowCurveRPM_max]
rpm_step = 200  # rpm for Power Curve
report_name = "FullPower_Curve_report"
PowerCurve = True  # Set True if plotting power Curve is needed, False if only plot f(time) needed

# Define input signal names
# CANAPE datafile parameters
# missing removed pars :  'zsUegoLambda','qsLamObtFin', 'zsMap',"qsTInj",
mdf_signal_list = ['bsRPM', 'zsTExh', 'esTorqueReqExt', 'zsPBoost', 'zsUegoLambda', 'qsLamObtFin', 'zsMap', "qsTInj",
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank"]

# ADAMO datafile parameters
ada_signal_list = [
    'Timestamp', 'DateTime', 'Test', 'Giri_tastiera', 'Torque_tastiera', 'Power_tasstiera', 'Throttle_tastiera',
    'Pcyl_1', 'Pcyl_2', 'Pcyl_3', 'Pcyl_4', 'Lambda', 'Engine_Torque', 'Brake_Speed', 'CNG', 'PtankF_BOSCH', 'Poil',
    'PETbI', 'PETbO', 'PACmO', 'P_boost', 'P_after_EGR_Cooler', 'PAIM_G', 'PcoolinPR', 'PcooloutPR', 'Pincomp', 'Patm',
    'T_Ex_Cyl_1', 'T_Ex_Cyl_2', 'T_Ex_Cyl_3', 'T_Ex_Cyl_4', 'TETbI', 'TETbO', 'T_EGR_cooler_out', 'T_Oil', 'T_Air',
    'TACmO', 'TAIcO', 'TAIM', 'T_coolant_in', 'T_coolant_out', 'TcoolinPR', 'TcooloutPR', 'T_CNG', 'QcoolPR_Hz',
    'CH4_Manifold', 'CH4_Up', 'CO_Up', 'CO2_Manifold', 'CO2_Up', 'CO_Manifold', 'HC_Manifold', 'HC_Up', 'NOx_Manifold',
    'NOx_Up', 'Tincat', 'Toutcat']
#
# "Timestamp","CNG", "P_boost", "P_Intake_Manifold", "P_Inlet_Turbocharger", "P_out_Turbine", "P_out_Turbine",
# "P_Out_Cat", "Brake_speed_F", "Power", "Engine_Torque","CNG",  "T_in_H20_Rid",
# "T_Asp_Cyl_1", "T_Asp_Cyl_4", "T_Asp_Cyl_5", "T_Asp_Cyl_8", "T_amb_Box",
# "T_Gas_In_Rid", "T_Body_Rid","T_Air", "T_Exh_Cyl_1", "T_Exh_Cyl_2", "T_Exh_Cyl_3", "T_Exh_Cyl_4","T_Exh_Cyl_5",
# "T_Exh_Cyl_6", "T_Exh_Cyl_7", "T_Exh_Cyl_8", "TETbI", "TETbI",
# "T_In_Cat", "T_Out_Cat" , "PtankF_BOSCH"]
#

#########################################################
# Report section preparing figures
#########################################################

# preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets

mdf_sigmap = dict()
for idx, signal in enumerate(canape_data_dict):
    for idy, name in enumerate(mdf_signal_list):
        if canape_data_dict['{:03d}'.format(idx)]['name'] == name:
            mdf_sigmap[name] = idx
            mdf_signal_list[idy] = "Found"

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
for idx, signal in enumerate(adamo_data_dict):
    for idy, name in enumerate(ada_signal_list):
        if adamo_data_dict['{:03d}'.format(idx)]['name'] == name:
            ada_sigmap[name] = idx
            ada_signal_list[idy] = "Found"

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
    statement = "t_MDF_{} = np.array(canape_data_dict['{:03d}']['time'])+AM_toff".format(name, pos)
    print(statement)
    exec(statement)
    statement = "v_MDF_{} = np.array(canape_data_dict['{:03d}']['data'])".format(name, pos)
    print(statement)
    exec(statement)
    statement = "l_MDF_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del canape_data_dict, canape_data

for name, pos in ada_sigmap.items():
    statement = "v_ADA_{} = np.array(adamo_data_dict['{:03d}']['data'])".format(name, pos)
    print(statement)
    exec(statement)
    statement = "l_ADA_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del adamo_data_dict, adamo_data

t_ADA = v_ADA_Timestamp - v_ADA_Timestamp[0]    # ADAMO datafile time

print("Ready for calculate other parameters ")

# Calculated parameters

cv_ADA_Power = v_ADA_Brake_Speed * v_ADA_Engine_Torque / 9548.8
cl_ADA_Power = 'Power kW'

cv_ADA_BSFC = v_ADA_CNG / cv_ADA_Power * 1000
cl_ADA_BSFC = "BSFC gr/kWh"

v_ADA_P_Intake_Manifold = v_ADA_Patm + v_ADA_PAIM_G
l_ADA_P_Intake_Manifold = 'MAP mbara'

cv_ADA_P_Boost = v_ADA_Patm + v_ADA_P_boost * 1000
cl_ADA_P_Boost = 'P_Boost [mbarA]'

# single Exhaust Temperature signal configuration
single_t_exhaust_signals = []
single_t_exhaust_labels = []
if num_cyls >= 1:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_1")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_1")
if num_cyls >= 2:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_2")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_2")
if num_cyls >= 3:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_3")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_3")
if num_cyls >= 4:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_4")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_4")
if num_cyls >= 5:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_5")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_5")
if num_cyls >= 6:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_6")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_6")
if num_cyls >= 7:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_7")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_7")
if num_cyls >= 8:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_8")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_8")
if num_cyls >= 9:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_9")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_9")
if num_cyls >= 10:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_10")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_10")
if num_cyls >= 11:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_11")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_11")
if num_cyls == 12:
    single_t_exhaust_signals.append("v_ADA_T_Ex_Cyl_12")
    single_t_exhaust_labels.append("l_ADA_T_Ex_Cyl_12")

# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '


# TREATING EMISSIONS DATAFILE .txt

if len(EMX_file) >= 5:
    EMX_filename = EMX_file.split('.')[0]
    EMX_pickle_file = EMX_filename + '.pickle'

    EMX_pickle = os.path.join(datafile_path, EMX_pickle_file)

    if os.path.exists(EMX_pickle):
        print('Found pickle file {} : loading EMISSIONS data from it.'.format(EMX_pickle))
        with open(EMX_pickle, 'rb') as handle:
            EMX_dict = pickle.load(handle)
    else:
        EMX_stream = os.path.join(datafile_path, EMX_file)

        print("EMISSIONS file to parse {}".format(EMX_stream))

        EMX_dict = {}
        EMX_len_extimation = row_count(EMX_stream)
        print("Total row approx {}".format(EMX_len_extimation - 1))
        with open(EMX_stream, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            idx = 0
            for row in spamreader:
                if idx == 0:
                    col_id = 0
                    for column in row:
                        EMX_dict[col_id] = {}
                        EMX_dict[col_id]['name'] = column
                        EMX_dict[col_id]['mu'] = ''
                        EMX_dict[col_id]['values'] = []
                        col_id += 1

                    num_cols = col_id
                    print('total column {}'.format(num_cols))

                else:
                    if len(row) == num_cols + 1:
                        col_id = 0

                        for value in row:
                            if col_id == 0:
                                time_sample = float(value)
                                EMX_dict[0]['values'].append(time_sample)
                            else:
                                try:
                                    value_num = float(value)
                                    EMX_dict[col_id]['values'].append(value_num)
                                except ValueError:
                                    pass
                                except KeyError:
                                    pass
                            col_id += 1
                sys.stdout.write('\rParsed {} rows out of {}.'.format(idx, EMX_len_extimation))
                sys.stdout.flush()
                idx += 1

        print("END parsing")
        with open(EMX_pickle, 'wb') as handle:
            print('Writing pickle file {} : dumping EMISSIONS data into it.'.format(EMX_pickle))
            pickle.dump(EMX_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for key, value in EMX_dict.items():
        print(key, value['name'])
    print()

#########################################################
# Report section preparing figures
#########################################################
# preparing arrays for plotting ---------------
# TODO here we are with debug

# Calculated parameters
# iidx_old=0
# for idx,sample in enumerate(v_ADA_Brake_Speed):
#     time_sample = t_ADA[idx]
#     for iidx, t_bsRPM in enumerate(t_MDF_bsRPM[iidx_old:]):
#         if t_bsRPM >= time_sample:
#             v_ADA_Brake_Speed[idx] = v_MDF_bsRPM[iidx_old+iidx]
#             iidx_old += iidx
#             break


cv_ADA_BSFC = np.array(v_ADA_CNG / cv_ADA_Power * 1000)
cl_ADA_BSFC = "BSFC gr/kWh"

# Preparing Power Curve Aggregations
if PowerCurve:
    PowerCurve_data_file = report_name + '_PowerCurve.pickle'
    PowerCurve_pickle = os.path.join(data_path, PowerCurve_data_file)

    if os.path.exists(PowerCurve_pickle):
        print('Found pickle file {} : loading Power Curve aggregated data data from it.'.format(PowerCurve_pickle))
        with open(PowerCurve_pickle, 'rb') as handle:
            PowerCurve_dict = pickle.load(handle)
    else:
        print("Starting Power Curve Aggregation")

        PowCurveRPM_Points = range(PowCurveRPM_min, PowCurveRPM_max, PowCurveRPM_stp)
        PowerCurve_dict = collections.OrderedDict()
        for point in PowCurveRPM_Points:
            PowerCurve_dict[point] = {}
            PowerCurve_dict[point]['rpm'] = []
            PowerCurve_dict[point]['torque'] = []
            PowerCurve_dict[point]['power'] = []
            PowerCurve_dict[point]['BSFC'] = []
            PowerCurve_dict[point]['texhInTC'] = []
            PowerCurve_dict[point]['texhOutTC'] = []
            PowerCurve_dict[point]['map'] = []
            PowerCurve_dict[point]['boost'] = []
            PowerCurve_dict[point]['lambda'] = []
            PowerCurve_dict[point]['adv'] = []

        # MAIN LOOP for creating clusters on Power Curve Parameters
        iidx_old = 0
        adv_idx_old = 0
        lambda_idx_old = 0

        for idx, sample in enumerate(v_ADA_Brake_Speed):
            time_sample = t_ADA[idx]

            for iidx, t_request in enumerate(t_MDF_esTorqueReqExt[iidx_old:]):
                if t_request >= time_sample:
                    v_request = v_MDF_esTorqueReqExt[iidx_old + iidx]
                    iidx_old += iidx
                    break
            valid = False
            if v_request >= 95:
                # print(idx,time_sample,sample,t_request,v_request,end=';')
                valid = True

            if valid:
                ind = bisect.bisect_left(list(PowerCurve_dict.keys()), sample)
                # print(sample,ind)
                # RPM cluster
                try:
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['rpm'].append(sample)
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['torque'].append(v_ADA_Engine_Torque[idx])
                    # change the power from measure from Adamo to calculated RPM ECU * measured torque
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['power'].append(sample * v_ADA_Engine_Torque[idx] / 9548.8)
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['BSFC'].append(cv_ADA_BSFC[idx])
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['texhInTC'].append(v_ADA_TETbI[idx])
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['texhOutTC'].append(v_ADA_TETbO[idx])
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['map'].append(v_ADA_P_Intake_Manifold[idx])
                    PowerCurve_dict[PowCurveRPM_Points[ind]]['boost'].append(cv_ADA_P_Boost[idx])
                except IndexError:
                    print("sample {}, idx {}, ind {}".format(sample, idx, ind))
                    # exit(2)
                    break

                for lambda_idx, t_MDF in enumerate(t_MDF_zsUegoLambda[lambda_idx_old:]):
                    if t_MDF >= time_sample:
                        PowerCurve_dict[PowCurveRPM_Points[ind]]['lambda'].append(
                            v_MDF_zsUegoLambda[lambda_idx_old + lambda_idx])
                        lambda_idx_old += lambda_idx
                        break
                for adv_idx, t_MDF in enumerate(t_MDF_jsAdv[adv_idx_old:]):
                    if t_MDF >= time_sample:
                        PowerCurve_dict[PowCurveRPM_Points[ind]]['adv'].append(v_MDF_jsAdv[adv_idx_old + adv_idx])
                        adv_idx_old += adv_idx
                        break
        print("END Aggregation")
        with open(PowerCurve_pickle, 'wb') as handle:
            print('Writing pickle file {} : dumping Power Curve Aggregated data into it.'.format(PowerCurve_pickle))
            pickle.dump(PowerCurve_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

report_path = os.path.join(data_path, report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# Temperatures plus general
if len(PowerCurve_dict) >= 5:
    fig_name = "PowerSteady_WorkingPoints_Temperatures"
    fig = plt.figure(figsize=(10, 8), dpi=200)
    ax1 = fig.add_subplot(211)
    ax1.plot(t_MDF_bsRPM, v_MDF_bsRPM, linestyle='solid', color='#FF0000FF', label=l_MDF_bsRPM)
    ax1.plot(t_ADA, v_ADA_Brake_Speed, linestyle='solid', color='#FF7F00FF', label=l_ADA_Brake_Speed)
    ax1.plot(t_ADA, v_ADA_Engine_Torque, linestyle='solid', color='#007F00FF', label=l_ADA_Engine_Torque)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0], x_lim[1], x_step))
    ax1.set_ylim([0, 3000])
    ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000])
    ax1.legend(shadow=True, loc=8, fontsize='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_ADA, cv_ADA_Power, linestyle='solid', color='#ff0087FF', label=cl_ADA_Power)
    ax2.set_ylim([0, 300])
    ax2.set_yticks(range(0, 300, 25))
    ax2.legend(shadow=True, loc=9, fontsize='xx-small')
    ax1.set_title(engine_name + ' - ' + report_name + ' - working points and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Engine Power [kW]')

    ax3 = fig.add_subplot(212)

    for temp in range(num_cyls):
        # for name, pos in mdf_sigmap.items():
        statement = "ax3.plot(t_ADA,{}, linestyle='solid',color = '{}',label={})".format(single_t_exhaust_signals[temp],
                                                                                         col_temp[temp],
                                                                                         single_t_exhaust_labels[temp])
        print(statement)
        exec(statement)
        # ax3.plot(t_ADA,y_temp[temp], linestyle='solid',color = col_temp[temp],label=y_temp_label[temp])
    ax3.plot(t_MDF_zsTExh, v_MDF_zsTExh, linestyle='solid', color='#FF0000FF', label=l_MDF_zsTExh)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0], x_lim[1], x_step))
    ax3.set_ylim([400, 900])
    ax3.set_yticks(range(400, 900, 50))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.8, 1.8])
    ax4.set_yticks([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8])
    ax3.legend(shadow=False, loc=4, fontsize='xx-small')
    ax4.legend(shadow=False, loc=6, fontsize='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path, fig_name + '.svg'))
    fig.savefig(os.path.join(report_path, fig_name + '.png'))

# Environmental plus combustion
if len(PowerCurve_dict) >= 5:
    fig_name = "PowerSteady_Environment_Combustion"
    fig = plt.figure(figsize=(10, 12), dpi=200)
    ax1 = fig.add_subplot(311)
    ax1.plot(t_MDF_bsRPM, v_MDF_bsRPM, linestyle='solid', color='#FF0000FF', label=l_MDF_bsRPM)
    ax1.plot(t_ADA, v_ADA_Brake_Speed, linestyle='solid', color='#FF7F00FF', label=l_ADA_Brake_Speed)
    ax1.plot(t_ADA, v_ADA_Engine_Torque, linestyle='solid', color='#007F00FF', label=l_ADA_Engine_Torque)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0], x_lim[1], x_step))
    ax1.set_ylim([0, 3000])
    ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000])
    ax1.legend(shadow=True, loc=8, fontsize='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_ADA, cv_ADA_Power, linestyle='solid', color='#ff0087FF', label=cl_ADA_Power)
    ax2.plot(t_ADA, cv_ADA_BSFC, linestyle='solid', color='#7e0640FF', label=cl_ADA_BSFC)
    ax2.plot(t_MDF_esTorqueReqExt, v_MDF_esTorqueReqExt, linestyle='solid', color='#2F2F2FFF',
             label=l_MDF_esTorqueReqExt)
    ax2.set_ylim([0, 450])
    ax2.set_yticks(range(0, 450, 50))
    ax2.legend(shadow=True, loc=9, fontsize='xx-small')
    ax1.set_title(engine_name + ' - ' + report_name + ' - Environmental and Combustion')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Engine Power [kW]/ BSFC [g/kWh]')

    ax3 = fig.add_subplot(312)

    ax3.plot(t_MDF_zsPBoost, v_MDF_zsPBoost, linestyle='solid', color='#FF0000FF', label=l_MDF_zsPBoost)
    ax3.plot(t_ADA, cv_ADA_P_Boost, linestyle='solid', color='#AF0000FF', label=cl_ADA_P_Boost)
    ax3.plot(t_MDF_zsMap, v_MDF_zsMap, linestyle='solid', color='#00007FFF', label=l_MDF_zsMap)
    ax3.plot(t_ADA, v_ADA_P_Intake_Manifold, linestyle='solid', color='#00008FFF', label=l_ADA_P_Intake_Manifold)
    ax3.plot(t_ADA, v_ADA_PETbI, linestyle='solid', color='#b26f19FF', label=l_ADA_PETbI)
    ax3.plot(t_ADA, v_ADA_PETbO, linestyle='solid', color='#553915FF', label=l_ADA_PETbO)
    # ax3.plot(t_ADA,v_ADA_P_In_Cat, linestyle='solid',color = '#1e6315FF',label=l_ADA_P_In_Cat)
    # ax3.plot(t_ADA,v_ADA_PETbO, linestyle='solid',color = '#24a614FF',label=l_ADA_PETbO)

    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0], x_lim[1], x_step))
    ax3.set_ylim([0, 3000])
    ax3.set_yticks(range(0, 3000, 250))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Pressures [mbar]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.8, 2.0])
    ax4.set_yticks([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8])
    ax3.legend(shadow=False, loc=3, fontsize='xx-small')
    ax4.legend(shadow=False, loc=4, fontsize='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    ax3 = fig.add_subplot(313)

    ax3.plot(t_MDF_zsTAir, v_MDF_zsTAir, linestyle='solid', color='#0b6eceFF', label=l_MDF_zsTAir)
    ax3.plot(t_MDF_zsTh2o, v_MDF_zsTh2o, linestyle='solid', color='#a82c1bFF', label=l_MDF_zsTh2o)
    ax3.plot(t_MDF_zsTRail, v_MDF_zsTRail, linestyle='solid', color='#13800dFF', label=l_MDF_zsTRail)
    ax3.plot(t_ADA, v_ADA_T_Air, linestyle='solid', color='#878dffFF', label=l_ADA_T_Air)
    # ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_1, linestyle='solid',color = '#ff15ce9F',label=l_ADA_T_Asp_Cyl_1)
    # ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_4, linestyle='solid',color = '#ff15ceCF',label=l_ADA_T_Asp_Cyl_4)
    # ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_5, linestyle='solid',color = '#0d10809F',label=l_ADA_T_Asp_Cyl_5)
    # ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_8, linestyle='solid',color = '#0d1080CF',label=l_ADA_T_Asp_Cyl_8)
    # ax3.plot(t_ADA,v_ADA_T_Body_Reg, linestyle='solid',color = '#31b62bCF',label=l_ADA_T_Body_Reg)
    # ax3.plot(t_ADA,v_ADA_T_Gas_Out_Rid, linestyle='solid',color = '#103b0eCF',label=l_ADA_T_Gas_Out_Rid)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0], x_lim[1], x_step))
    ax3.set_ylim([-20, 60])
    ax3.set_yticks(range(-20, 60, 10))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_jsAdv, v_MDF_jsAdv, linestyle='solid', color='#ff04004F', label=l_MDF_jsAdv)
    ax4.plot(t_MDF_jsAdvBase, v_MDF_jsAdvBase, linestyle='solid', color='#bf0400CF', label=l_MDF_jsAdvBase)

    ax4.set_ylim([0, 40])
    ax4.set_yticks(range(0, 40, 5))
    ax3.legend(shadow=False, loc=3, fontsize='xx-small')
    ax4.legend(shadow=False, loc=4, fontsize='xx-small')
    ax4.set_ylabel('Spark Advance [deg BTDC]')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path, fig_name + '.svg'))
    fig.savefig(os.path.join(report_path, fig_name + '.png'))

######################################################################################################################
# Power Curve Plot f(RPM)
######################################################################################################################
if PowerCurve:
    PC_rpm = []
    PC_torque = []
    PC_torque_std = []
    PC_torque_high = []
    PC_torque_low = []
    PC_power = []
    PC_power_std = []
    PC_BSFC = []
    PC_BSFC_std = []
    PC_texhInTC = []
    PC_texhInTC_std = []
    PC_texhOutTC = []
    PC_texhOutTC_std = []
    PC_map = []
    PC_map_std = []
    PC_boost = []
    PC_boost_std = []
    PC_lambda = []
    PC_lambda_std = []
    PC_adv = []
    PC_adv_std = []
    for idx, point in enumerate(list(PowerCurve_dict.keys())):
        PC_rpm.append(np.mean(PowerCurve_dict[point]['rpm']))
        PC_torque.append(np.mean(PowerCurve_dict[point]['torque']))
        PC_torque_std.append(np.std(PowerCurve_dict[point]['torque']))
        PC_power.append(np.mean(PowerCurve_dict[point]['power']))
        PC_power_std.append(np.std(PowerCurve_dict[point]['power']))
        PC_BSFC.append(np.mean(PowerCurve_dict[point]['BSFC']))
        PC_BSFC_std.append(np.std(PowerCurve_dict[point]['BSFC']))
        PC_texhInTC.append(np.mean(PowerCurve_dict[point]['texhInTC']))
        PC_texhInTC_std.append(np.std(PowerCurve_dict[point]['texhInTC']))
        PC_texhOutTC.append(np.mean(PowerCurve_dict[point]['texhOutTC']))
        PC_texhOutTC_std.append(np.std(PowerCurve_dict[point]['texhOutTC']))
        PC_map.append(np.mean(PowerCurve_dict[point]['map']))
        PC_map_std.append(np.std(PowerCurve_dict[point]['map']))
        PC_boost.append(np.mean(PowerCurve_dict[point]['boost']))
        PC_boost_std.append(np.std(PowerCurve_dict[point]['boost']))
        PC_lambda.append(np.mean(PowerCurve_dict[point]['lambda']))
        PC_lambda_std.append(np.std(PowerCurve_dict[point]['lambda']))
        PC_adv.append(np.mean(PowerCurve_dict[point]['adv']))
        PC_adv_std.append(np.std(PowerCurve_dict[point]['adv']))
    PC_rpm = np.array(PC_rpm, dtype='float')
    PC_torque = np.array(PC_torque, dtype='float')
    PC_torque_std = np.array(PC_torque_std, dtype='float')
    PC_torque_high = PC_torque + 3 * PC_torque_std
    PC_torque_low = PC_torque - 3 * PC_torque_std
    PC_power = np.array(PC_power, dtype='float')
    PC_power_std = np.array(PC_power_std, dtype='float')
    PC_power_high = PC_power + 3 * PC_power_std
    PC_power_low = PC_power - 3 * PC_power_std
    PC_BSFC = np.array(PC_BSFC, dtype='float')
    PC_BSFC_std = np.array(PC_BSFC_std, dtype='float')
    PC_BSFC_high = PC_BSFC + 3 * PC_BSFC_std
    PC_BSFC_low = PC_BSFC - 3 * PC_BSFC_std

    fig_name = "StatsPicture"

    fig = plt.figure(num=4, figsize=(int(210 / 25.4), int(297 / 25.4)), dpi=200)
    gs1 = gridspec.GridSpec(nrows=5, ncols=1, left=0.15, right=0.85, wspace=0.00, hspace=0.00)
    ax1 = fig.add_subplot(gs1[0:2, :])
    ax2 = fig.add_subplot(gs1[2, :])
    ax3 = fig.add_subplot(gs1[3, :])
    ax4 = fig.add_subplot(gs1[-1, :])

    # Power plot with + and - 3 sigma
    ax1.plot(PC_rpm, PC_power, linestyle='solid', color='#ff0400FF', label="Power [kW]")
    # ax1.plot(PC_rpm,PC_power_high,linestyle='solid',color = '#ff04008F',label="+3 std")
    # ax1.plot(PC_rpm,PC_power_low,linestyle='solid',color = '#ff04004F',label="-3 std")
    ax1.set_xlim(rpm_lim)
    ax1.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax1.set_ylim(0, 200)
    ax1.set_yticks(range(0, 200, 25), minor=True)

    ax1.set_title(engine_name + ' - WH Mapping Power Curve')
    # ax1.get_xaxis().set_visible(False)
    ax1.set_ylabel('Engine Power [kW]')
    ax1.grid()
    # Torque plot with + and - 3 sigma
    ax1r = ax1.twinx()
    ax1r.plot(PC_rpm, PC_torque, linestyle='solid', color='#0404FFFF', label="Torque [Nm]")
    # ax1r.plot(PC_rpm,PC_torque_high,linestyle='solid',color = '#0404FF8F',label="+3 std")
    # ax1r.plot(PC_rpm,PC_torque_low,linestyle='solid',color = '#0404FF4F',label="-3 std")
    ax1r.set_xlim(rpm_lim)
    ax1r.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax1r.set_ylim(0, 800)
    ax1r.set_yticks(range(0, 800, 100), minor=True)
    ax1r.set_ylabel('Engine Torque [Nm]')
    ax1.legend(shadow=False, loc=3, fontsize='xx-small')
    ax1r.legend(shadow=False, loc=4, fontsize='xx-small')

    # BSFC plot with + and - 3 sigma
    ax2.plot(PC_rpm, PC_BSFC, linestyle='solid', color='#37874dFF', label="BSFC [g/kWh]")
    # ax2.plot(PC_rpm, PC_BSFC_high, linestyle='solid', color='#37874d8F', label="+3 std")
    # ax2.plot(PC_rpm, PC_BSFC_low, linestyle='solid', color='#37874d4F', label="-3 std")
    ax2.set_xlim(rpm_lim)
    ax2.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax2.set_ylim(170, 270)
    ax2.set_yticks(range(170, 260, 10), minor=True)
    ax2.set_ylabel("BSFC [g/kWh]")
    ax2.grid()
    ax2.legend(shadow=False, loc=3, fontsize='xx-small')
    # BSFC plot with + and - 3 sigma
    ax3.plot(PC_rpm, PC_texhInTC, linestyle='solid', color='#9d177fFF', label=l_ADA_TETbI)
    ax3.plot(PC_rpm, PC_texhOutTC, linestyle='solid', color='#17269dFF', label=l_ADA_TETbO)
    ax3.set_xlim(rpm_lim)
    ax3.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax3.set_ylim(500, 800)
    ax3.set_yticks(range(500, 800, 50), minor=True)
    ax3.set_ylabel("Temperature [deg C]")
    ax3.grid()
    ax3.legend(shadow=False, loc=3, fontsize='xx-small')
    ax4.plot(PC_rpm, PC_boost, linestyle='solid', color='#ff0400FF', label="P Boost [mbar]")
    ax4.plot(PC_rpm, PC_map, linestyle='solid', color='#0404FFFF', label="MAP [mbar]")
    ax4.set_xlim(rpm_lim)
    ax4.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax4.set_ylim(1000, 3000)
    ax4.set_yticks(range(1000, 3000, 250), minor=True)
    ax4.set_xlabel('Engine speed [rpm]')
    ax4.set_ylabel('Pressure [mbar A]')
    ax4.grid()
    ax4r = ax4.twinx()
    ax4r.plot(PC_rpm, PC_lambda, linestyle='solid', color='#717a36FF', label="Lambda [n]")
    ax4r.set_xlim(rpm_lim)
    ax4r.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step), minor=False)
    ax4r.set_ylim(0.8, 1.6)
    ax4r.set_yticks([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6], minor=True)
    ax4r.set_ylabel('Lambda=AFR/AFRstoich')
    ax4.legend(shadow=False, loc=3, fontsize='xx-small')
    ax4r.legend(shadow=False, loc=4, fontsize='xx-small')
    fig.savefig(os.path.join(report_path, fig_name + '.svg'))
    fig.savefig(os.path.join(report_path, fig_name + '.png'))
