
"""
Import and elaborate WHTC cycle
version 02 - Bosmal_Poland
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import errno
import sys
from bosmal_data import Bosmal_Data
from mdf_data import Mdf_Data
import datetime


# Calculate the milligrams in the period T
def ppm2mg(u_gas, ppm, m_exh, T):
    if ppm <= 0:
        ppm = 0.0
    mg = 1000 * u_gas * ppm * m_exh * T
    return mg


def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i


# INPUT DATA AND FILES DEFINITIONS

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))
engine_project_name = 'OM906_NGV_SP - '
data_path = "D:\\Application_data\\Mercedes_NGV"
bosmal_filename = "WHTC_Day7_1_Hot_05022020_10Hz.txt"
mdf_filename_list = ["WHTC_Day7_1_Hot_05022020_10Hz_MDF.txt"]


if bosmal_filename.split('_')[3].upper()=='COLD':
    x_lim=[0, 1800] ; x_tick = 100
    WHTC_segments=[(0, 325), (325, 750), (750, 1200), (1200, 1550), (1500, 1900)]
    mdf_time_offsets_list = [0.816-2.5500]         # offset time in seconds (initial points of Bosmal file - INITIAL MDF)
else:
    x_lim=[0, 1900] ; x_tick = 100
    WHTC_segments=[(50, 375), (375, 825), (800, 1250), (1200, 1625), (1550, 1925)]
    mdf_time_offsets_list = [1568.0-1381.0]         # offset time in seconds (initial points of Bosmal file - INITIAL MDF)
report_name = '_'.join(bosmal_filename.split('_')[0:4])

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
    canape_data = Mdf_Data(data_path, mdf_filename)
    canape_data_dict = canape_data.load_data()
    canape_data_dict_list.append(canape_data_dict)

    if canape_data_dict is None:
        print("Errore, controlla i dati di input")
        sys.exit(1)


bosmal_poland_data = Bosmal_Data(data_path, bosmal_filename)

bosmal_poland_data_dict = bosmal_poland_data.load_data()

if bosmal_poland_data_dict is None:
    print("Errore, controlla i dati di input")
    sys.exit(2)

print('finish')

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

# Define input signal names
# CANAPE datafile parameters
mdf_signal_list = ['bsRPM', 'zsTExh', 'zsUegoLambda', 'qsLamObtFin', 'esTorqueReqExt', 'zsMap', 'zsPBoost',
                   'zsTh2o', 'zsTAir', 'zsTRail', 'jsAdv', 'jsAdvBase', "zsPRail", "zsPTank", "qsInjTemperature",
                   "qsTInj", "zsTRail", "fsKO2"]

# BOSMAL_POLAND datafile parameters
bosmal_signal_list = ["recorder_time", "ACC", "ACC", "ad", "ALPHA", "BLOW_BY", "BLOW_VAL", "BSFC", "CH4_A11", "CO2_A11",
                      "CO_H_A11", "CO_L_A11", "FAIR", "FC_CNG", "FW", "GEXH", "HC_A11", "HUM", "LAMBDA", "NH3",
                      "NO_A11", "NOX_A11", "O2_A11", "P", "P1C", "P1CAT", "P1IC", "P1T", "P1W", "P2CAT", "P2IC", "P2T",
                      "P2W", "PA", "PCNG", "PCRANKC", "pe", "Po", "Po_HP", "Po_PS", "POIL", "PWT", "RPM", "S415_FSN",
                      "SMOKE", "STEP", "STEPTYPE", "T", "T0", "T1A", "T1C", "T1CAT", "T1IC", "T1T", "T1W",
                      "T2CAT", "T2IC", "T2IC_s", "T2T", "T2W", "T2W_s", "TA", "TOILG", "TOILS", "U_BATT"
                      ]
# recorder_time	ACC	ACC	ad	ALPHA	BLOW_BY	BLOW_VAL	BSFC	CH4_A11	CO2_A11	CO_H_A11	CO_L_A11	FAIR
# FC_CNG	FW	GEXH	HC_A11	HUM	LAMBDA	NH3	NO_A11	NOX_A11	O2_A11	P	P1C	P1CAT	P1IC	P1T	P1W	P2CAT	P2IC
# P2T	P2W	PA	PCNG	PCRANKC	pe	Po	Po_HP	Po_PS	POIL	PWT	RPM	S415_FSN	SMOKE	STEP	STEPTYPE	T	T0
# T1A	T1C	T1CAT	T1IC	T1T	T1W	T2CAT	T2IC	T2IC_s	T2T	T2W	T2W_s	TA	TOILG	TOILS	U_BATT	#
#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
# Looking for needed signal from the complete datasets

mdf_sigmap_list = []
mdf_sigmap = dict()
for canape_data_dict in canape_data_dict_list:
    for idx, signal in enumerate(canape_data_dict):
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

bosmal_sigmap = dict()
for idx, signal in enumerate(bosmal_poland_data_dict):
    for idy, name in enumerate(bosmal_signal_list):
        if bosmal_poland_data_dict['{:03d}'.format(idx)]['name']==name:
            bosmal_sigmap[name]= idx
            bosmal_signal_list[idy]= "Found"

print(bosmal_sigmap)
bosmal_sign_lost = False
for idy, name in enumerate(bosmal_signal_list):
    if name != "Found":
        print("The signal {} not found".format(name))
        bosmal_sign_lost = True

if not bosmal_sign_lost:
    print("Found all signals from Bosmal_poland datafile")
else:
    print("Missing signals from Bosmal_poland datafile! Exit!")
    sys.exit(1)

print("Ready for assigning values and other stuffs")
if len(mdf_sigmap_list) < 2:
    mdf_sigmap = mdf_sigmap_list[0]
    mdf_time_offset = mdf_time_offsets_list[0]
    for name, pos in mdf_sigmap.items():
        statement = "t_MDF_{} = np.array(canape_data_dict['{:03d}']['time'])+mdf_time_offset".format(name, pos)
        print(statement)
        exec(statement)
        statement = "v_MDF_{} = np.array(canape_data_dict['{:03d}']['data'])".format(name, pos)
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

for name, pos in bosmal_sigmap.items():
    statement = "v_BOSMAL_{} = np.array(bosmal_poland_data_dict['{:03d}']['data'])".format(name, pos)
    print(statement)
    exec(statement)
    statement = "l_BOSMAL_{} = '{}'".format(name, name)
    print(statement)
    exec(statement)

del bosmal_poland_data_dict, bosmal_poland_data


t_BOSMAL = v_BOSMAL_recorder_time / 1000     # BOSMAL_POLAND datafile time in seconds
del v_BOSMAL_recorder_time

print("Ready for calculate other parameters ")

# Calculation of the mass emission

# Data channel provided by Bosmal Test Bench
# CH4_A11	ppm	CH4 concentration
# CO2_A11	%	CO2 concentration
# CO_H_A11	%	CO high concentration
# CO_L_A11	ppm	CO low concentration
# FAIR	kg/h	Air flow intake
# FC_CNG	kg/h	CNG fuel consumption
# FW	l/min	Water flow
# GEXH	kg/h	Exhaust gases flow
# HC_A11	ppm	HC concentration
# HUM	%	Humidity
# LAMBDA	-	Lambda
# NH3	ppm	NH3 concentration
# NO_A11	ppm	NO concentration
# NOX_A11	ppm	NOX concentration
# O2_A11	%	O2 concentration
# P	kW	Power

# m_gas [mg]= 1000 * u_gas * c_gas * q_m_exh * (1 / f)
# where
# u_gas     =   ratio between density of exhaust component and density of exhaust gas
# c_gas     =   instantaneous concentration of the component in the raw exhaust gas, ppm
# q_m_exh   =   instantaneous exhaust mass flow, kg/s
# f=   data sampling rate, Hz


u_gas = { 'NOx': 0.001621, 'CO':0.000987, 'HC':0.000558, 'CO2':0.001551, 'O2':0.001128, 'CH4':0.000565}
qm_exh = v_BOSMAL_GEXH / 3600        # from kg/h to kg/s
if np.max(np.cumsum(qm_exh)) <= 5:
    qm_exh = v_BOSMAL_FAIR / 3600
t_tot =0
m_NOx = np.empty(len(t_BOSMAL))     # mass mg NOx
m_CO = np.empty(len(t_BOSMAL))     # mass mg CO
m_CH4 = np.empty(len(t_BOSMAL))     # mass mg CH4
m_HC = np.empty(len(t_BOSMAL))     # mass mg HC
m_CO2 = np.empty(len(t_BOSMAL))     # mass mg CO2

for i, t in enumerate(t_BOSMAL):
    if i > 0:
        T = t - t_old
        t_tot += T
        m_NOx[i] = ppm2mg(u_gas['NOx'], v_BOSMAL_NOX_A11[i], qm_exh[i], T)
        m_CO[i] = ppm2mg(u_gas['CO'], v_BOSMAL_CO_L_A11[i], qm_exh[i], T)
        m_CH4[i] = ppm2mg(u_gas['CH4'], v_BOSMAL_CH4_A11[i], qm_exh[i], T)
        m_HC[i] = ppm2mg(u_gas['HC'], v_BOSMAL_HC_A11[i], qm_exh[i], T)
        m_CO2[i] = ppm2mg(u_gas['CO2'], v_BOSMAL_CO2_A11[i], qm_exh[i], T)

    else:
        t_tot = t
        m_NOx[i] = 0.0
        m_CO[i] = 0.0
        m_CH4[i] = 0.0
        m_HC[i] = 0.0
        m_CO2[i] = 0.0

    t_old = t

# Cumulative emission from mass measurement - Not available in Bosmal files by now // 04/02/2020 GM
v_cum_CO = np.cumsum(m_CO)
l_cum_CO = "cum. sum. CO "
v_cum_CH4 = np.cumsum(m_CH4)
l_cum_CH4 = "cum. sum. CH4"
v_cum_NOx = np.cumsum(m_NOx)
l_cum_NOx = "cum. sum. NOx"
v_cum_THC = np.cumsum(m_HC)
l_cum_THC = "cum. sum. HC"

# Autoscale emissions y axis
CO_max = np.max(v_cum_CO)
CH4_max = np.max(v_cum_CH4)
NOx_max = np.max(v_cum_NOx)
THC_max = np.max(v_cum_THC)
MaxOfMax = np.max([CO_max, CH4_max, NOx_max, THC_max])

if MaxOfMax < 10500.0:
    cum_sum_range = [0, 10000]     # mg
elif MaxOfMax < 21000.0:
    cum_sum_range = [0, 20000]     # mg
elif MaxOfMax < 52000.0:
    cum_sum_range = [0, 50000]     # mg
elif MaxOfMax < 110000:
    cum_sum_range = [0, 100000]     # mg
else:
    cum_sum_range = [0, 500000]     # mg


# COLORS   '0        ', '1        ', '2        ', '3        '4          ', '5        ', '6        ', '7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '


report_path = os.path.join(data_path, report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


# ## Temperatures plus general
if len(t_BOSMAL)>=5 :
    fig_name = "Full_Test_Temperatures"
    print("Generating and writing the chart {} global of ETC test in {}".format(fig_name, data_path))
    fig = plt.figure(figsize=(10, 8), dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_MDF_bsRPM, v_MDF_bsRPM, linestyle= 'solid', color = '#FF0000FF', label=l_MDF_bsRPM)
    ax1.plot(t_BOSMAL, v_BOSMAL_RPM, linestyle= 'solid', color = '#FF7F00FF', label=l_BOSMAL_RPM)
    ax1.plot(t_BOSMAL, v_BOSMAL_T, linestyle='solid', color = '#007F00FF', label= l_BOSMAL_T)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0], x_lim[1], x_tick))
    ax1.set_ylim([0, 2500])
    ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
    ax1.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_BOSMAL, v_BOSMAL_Po, linestyle='solid', color = '#ff0087FF', label=l_BOSMAL_Po)
    ax2.set_ylim([0, 250])
    ax2.set_yticks(range(0, 250, 25))
    ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize ='xx-small')
    ax1.set_title(engine_project_name+report_name+' - Full Test - Lambda control and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Corrected Power [kW]')


    ax3 = fig.add_subplot(212)

    #
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_BOSMAL_T_In_Turbine_Cyl_1234)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_BOSMAL_T_In_Turbine_Cyl_5678)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_BOSMAL_T_In_Cat)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_BOSMAL_T_Out_Cat)
    ax3.plot(t_MDF_zsTExh,v_MDF_zsTExh, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsTExh)
    ax3.plot(t_BOSMAL,v_BOSMAL_T1T, linestyle='solid',color = '#7F0000FF',label=l_BOSMAL_T1T)
    ax3.plot(t_BOSMAL, v_BOSMAL_T1CAT, linestyle='solid',color = '#00FF00FF',label=l_BOSMAL_T1CAT)
    ax3.plot(t_BOSMAL, v_BOSMAL_T2CAT, linestyle='solid',color = '#0000FFFF',label=l_BOSMAL_T2CAT)

    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax3.set_ylim([000,800])
    ax3.set_yticks(range(000,800,100))
    ax3.legend(shadow=True, loc=(LEGEND_LOWER_C),fontsize ='xx-small')

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=l_MDF_zsUegoLambda)
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=l_MDF_qsLamObtFin)
    ax4.set_ylim([0.7,1.5])
    ax4.set_yticks([0.70,0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ,1.4 , 1.5])
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
if len(t_BOSMAL)>=5 :
    fig_name = "Full_Test_Emissions"
    print("Generating and writing the chart {} global of WHTC test in {}".format(fig_name,data_path))
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)

    ax1.plot(t_BOSMAL, v_BOSMAL_RPM,linestyle= 'solid',color = '#FF7F00FF',label=l_BOSMAL_RPM)
    ax1.plot(t_BOSMAL,v_BOSMAL_T, linestyle='solid',color = '#007F00FF',label= l_BOSMAL_T)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax1.set_ylim([0,2500])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250,2500])
    ax1.legend(shadow=True, loc=(LEGEND_UPPER_L),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_BOSMAL,v_BOSMAL_FAIR, linestyle='solid',color = '#7F7FFFFF',label=l_BOSMAL_FAIR)
    # ax2.plot(t_BOSMAL,v_BOSMAL_GEXH, linestyle='solid',color = '#FF0000FF',label=l_BOSMAL_GEXH)
    ax2.plot(t_BOSMAL,v_BOSMAL_FC_CNG, linestyle='solid',color = '#00FF00FF',label=l_BOSMAL_FC_CNG)
    ax2.set_ylim([0,1000])
    ax2.set_yticks(range(0,1000,100))
    ax2.legend(shadow=True, loc=(LEGEND_UPPER_C),fontsize ='xx-small')
    ax1.set_title(engine_project_name+report_name+' - Emissions and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Tank Pressure [mbar]')


    ax3 = fig.add_subplot(212)

    #
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Turbine_Cyl_1234, linestyle='solid',color = col_temp[1],label=l_BOSMAL_T_In_Turbine_Cyl_1234)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Turbine_Cyl_5678, linestyle='solid',color = col_temp[3],label=l_BOSMAL_T_In_Turbine_Cyl_5678)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_In_Cat, linestyle='solid',color = col_temp[5],label=l_BOSMAL_T_In_Cat)
    # ax3.plot(t_BOSMAL,v_BOSMAL_T_Out_Cat, linestyle='solid',color = col_temp[7],label=l_BOSMAL_T_Out_Cat)
    ax3.plot(t_BOSMAL,v_cum_NOx, linestyle='solid',color = '#FF0000FF',label=l_cum_NOx)
    ax3.plot(t_BOSMAL,v_cum_CO, linestyle='solid',color = '#0A0A0AFF',label=l_cum_CO)
    ax3.plot(t_BOSMAL,v_cum_CH4, linestyle='solid',color = '#0F0FFFFF',label=l_cum_CH4)
    ax3.plot(t_BOSMAL,v_cum_THC, linestyle='solid',color = '#0AFFFFFF',label=l_cum_THC)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax3.set_ylim(cum_sum_range)
    ax3.set_yticks(np.arange(cum_sum_range[0], cum_sum_range[1], int(cum_sum_range[1] / 10)))
    ax3.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize ='xx-small')

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Cumulative emissions [mg]')
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
    # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
    plt.close('all')

    for WHTC_segment in WHTC_segments:
    # ## Emissions plus general segments
        fig_name = "Test_segment_{}_{}_seconds_Emissions".format(WHTC_segment[0], WHTC_segment[1])
        print("Generating and writing the chart {} segment in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_BOSMAL, v_BOSMAL_RPM, linestyle='solid', color='#FF7F00FF', label=l_BOSMAL_RPM)
        ax1.plot(t_BOSMAL, v_BOSMAL_T, linestyle='solid', color='#007F00FF', label=l_BOSMAL_T)
        ax1.set_xlim(WHTC_segment)
        ax1.set_xticks(range(WHTC_segment[0], WHTC_segment[1], 25))
        ax1.set_ylim([0, 2500])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax1.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_zsMap, v_MDF_zsMap, linestyle='solid', color='#ff0087FF', label=l_MDF_zsMap)
        ax2.plot(t_MDF_zsPBoost, v_MDF_zsPBoost, linestyle='solid', color='#00ff87FF', label=l_MDF_zsPBoost)
        ax2.set_ylim([0, 2500])
        ax2.set_yticks(range(0, 2500, 100))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_project_name + report_name + ' - Emissions and working parameters')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('MAP and Boost Pressures [mbar]')

        ax3 = fig.add_subplot(212)


        ax3.plot(t_BOSMAL, v_cum_NOx, linestyle='solid', color='#FF0000FF', label=l_cum_NOx)
        ax3.plot(t_BOSMAL, v_cum_CO, linestyle='solid', color='#0A0A0AFF', label=l_cum_CO)
        ax3.plot(t_BOSMAL, v_cum_CH4, linestyle='solid', color='#0F0FFFFF', label=l_cum_CH4)
        ax3.plot(t_BOSMAL, v_cum_THC, linestyle='solid', color='#0AFFFFFF', label=l_cum_THC)
        ax3.set_xlim(WHTC_segment)
        ax3.set_xticks(range(WHTC_segment[0], WHTC_segment[1], 25))
        ax3.set_ylim(cum_sum_range)
        ax3.set_yticks(np.arange(cum_sum_range[0], cum_sum_range[1], int(cum_sum_range[1]/10)))
        ax3.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Cumulative emissions [mg]')
        ax3.grid()
        ax4 = ax3.twinx()
        ax4.plot(t_MDF_zsUegoLambda, v_MDF_zsUegoLambda, linestyle='solid', color='#7F7F003F', label=l_MDF_zsUegoLambda)
        ax4.plot(t_MDF_qsLamObtFin, v_MDF_qsLamObtFin, linestyle='solid', color='#bF7F008F', label=l_MDF_qsLamObtFin)
        ax4.plot(t_MDF_fsKO2, v_MDF_fsKO2, linestyle='solid', color='#7F7F7FFF', label=l_MDF_fsKO2)

        ax4.set_ylim([0.75, 1.75])
        ax4.set_yticks(np.arange(0.75,1.75,0.05))

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
