
"""
Import and elaborate WHTC cycle
version 02 - Bosmal_Poland
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import errno
import sys
from bosmal_data_notimestamp import Bosmal_Data
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
engine_project_name = 'OM906_NGV_MPI CAL 02_00 - '
data_path = "D:\\Application_data\\Mercedes_NGV"
bosmal_filename = "MPI_WHTC_2137_Hot.txt"
mdf_filename_list = ["MPI_WHTC_2137_Hot_MDF.txt"]


if bosmal_filename.split('_')[3].split('.')[0].upper()=='COLD':
    x_lim=[0, 1800] ; x_tick = 100
    WHTC_segments=[(0, 325), (325, 750), (750, 1200), (1200, 1550), (1500, 1900)]
    mdf_time_offsets_list = [11.2-80]         # offset time in seconds (initial points of Bosmal file - INITIAL MDF)
else:
    x_lim=[0, 1900] ; x_tick = 100
    WHTC_segments=[(50, 375), (375, 825), (800, 1250), (1200, 1625), (1550, 1925)]
    mdf_time_offsets_list = [17.5 - 0]         # offset time in seconds (initial points of Bosmal file - INITIAL MDF)
report_name = '_'.join(bosmal_filename.split('.')[0].split('_')[0:4])

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

DEF_NOX_ANALYSER_DELAY = -12.0
DEF_HC_ANALYSER_DELAY = -12.0
DEF_COL_ANALYSER_DELAY = -12.0
DEF_CH4_ANALYSER_DELAY = -12.0
DEF_NH3_ANALYSER_DELAY = -12.0

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
                   "qsTInj", "zsTRail", "fsKO2", 'asEtasp']
# BOSMAL_POLAND datafile parameters August 04 2020 * one test only
# bosmal_signal_list = ["ACC", "BagAnalysisStatus", "CalibFlagEbench6", "CalibFlagEbench12", "Conc_CH4_TailPipe1",
#                    "Conc_HC_TailPipe1", "Conc_NH3_TailPipe1", "Conc_NO_TailPipe1", "Conc_NOX_TailPipe1",
#                    "Conc_ParticuInteg_DilutedAPC", "ConcDilCorr_ParticuNo_DilutedAPC", "ConcDry_CO2_TailPipe1",
#                    "ConcDry_COH_TailPipe1", "ConcDry_COL_TailPipe1", "ConcDry_N2O_TailPipe1", "ConcDry_O2_TailPipe1",
#                    "DilRatio_Gas_Device1SPC", "DilutionStage_DilutedAPC", "DYSCYCLE", "DYSMODE", "DYSPHASE",
#                    "Flag_PartiCountTime_APC", "Flag_PartiLoadTime_Device1SPC", "FT_TACT", "Lightabsorption_Exh_Opacimeter",
#                    "MassFlow_Back_Device1SPC", "MassFlow_Exh_Device1SPC", "MassFlow_Out_Device1SPC", "MassFlow_Probe_Device1SPC",
#                    "MassFlow_Total_Device1SPC", "PCRFCorr_ParticuInteg_DilutedAPC", "Pressure_Filter_Device1SPC", "Pressure_Fuel_Test",
#                    "SampleRatio_Exh_Device1SPC", "Temp_DilutionAir_Device1SPC", "Temp_EvapTube_APC", "Temp_Exh_Device1SPC",
#                    "Temp_Filter_Device1SPC", "Temp_PND1_APC", "Temp_Probe_Device1SPC", "Velocity_FilterFace_Device1SPC",
#                    "VolFlowProbe_APC"]


# BOSMAL_POLAND datafile parameters July 2020
bosmal_signal_list = ["recorder_time", "ACC", "ALPHA", "ALPHA_d", "CalibFlagEbench6", "Conc_CH4_TailPipe1", "Conc_HC_TailPipe1", "Conc_NH3_TailPipe1", "Conc_NO_TailPipe1", "Conc_NOX_TailPipe1",
                      "ConcDry_CO2_TailPipe1", "ConcDry_COH_TailPipe1", "ConcDry_COL_TailPipe1", "ConcDry_N2O_TailPipe1", "ConcDry_O2_TailPipe1", "Counter_DYS_Test",
                      "DEWTEMP", "DYS_CONT", "DYSCYCLE", "DYSMODE", "DYSPHASE", "FB_RATE", "FB_TEMP", "FB_TEMP_GEM", "FB_VAL", "FB_VAL_GEM", "FT_TACT", "GAH", "HUMIDABS",
                      "Lightabsorption_Exh_Opacimeter", "N_dem_D", "N_dem_E", "N_ENGINE", "P_AIR", "PHI", "Pressure_Air_EngIntake", "Pressure_Fuel_Test", "T_AIR",
                      "T_dem_D", "T_dem_E", "Torque", "T_OIL", "Temp_Air_EngIntake", "TESTTIME", "TWI", "TWO", "Value_ActualCycle_Test", "Value_ActualMode_Test",
                      "Value_AuxiliaryPower_Test", "Value_GemReserve01_Test", "Value_HUMIDREL_DilAir", "Value_HUMIDREL_EngInlet", "Value_PRESSURE_DilAir",
                      "Value_StationaryTmp01_Test", "Value_WaterTempCACIn_Test", "ACC_Delay", "CalibFlagEbench6_Delay", "Conc_CH4_TailPipe1_Delay",
                      "Conc_HC_TailPipe1_Delay", "Conc_NH3_TailPipe1_Delay", "Conc_NO_TailPipe1_Delay",
                      "Conc_NOX_TailPipe1_Delay", "ConcDry_CO2_TailPipe1_Delay", "ConcDry_COH_TailPipe1_Delay", "ConcDry_COL_TailPipe1_Delay",
                      "ConcDry_N2O_TailPipe1_Delay","ConcDry_O2_TailPipe1_Delay", "FT_TACT_Delay", "Pressure_Fuel_Test_Delay"
                      ]
# # BOSMAL_POLAND datafile parameters February 2020
# bosmal_signal_list = ["recorder_time", "ACC", "ACC", "ad", "ALPHA", "BLOW_BY", "BLOW_VAL", "BSFC", "CH4_A11", "CO2_A11",
#                       "CO_H_A11", "CO_L_A11", "FAIR", "FC_CNG", "FW", "GEXH", "HC_A11", "HUM", "LAMBDA", "NH3",
#                       "NO_A11", "NOX_A11", "O2_A11", "P", "P1C", "P1CAT", "P1IC", "P1T", "P1W", "P2CAT", "P2IC", "P2T",
#                       "P2W", "PA", "PCNG", "PCRANKC", "pe", "Po", "Po_HP", "Po_PS", "POIL", "PWT", "RPM", "S415_FSN",
#                       "SMOKE", "STEP", "STEPTYPE", "T", "T0", "T1A", "T1C", "T1CAT", "T1IC", "T1T", "T1W",
#                       "T2CAT", "T2IC", "T2IC_s", "T2T", "T2W", "T2W_s", "TA", "TOILG", "TOILS", "U_BATT"
#                       ]
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
        if bosmal_poland_data_dict['{:03d}'.format(idx)]['name'].upper() == name.upper():
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

for name, pos in mdf_sigmap.items():
    if name == 'bsRPM':
        time_MDF = canape_data_dict['{:03d}'.format(pos)]['time']
        rpm_MDF = canape_data_dict['{:03d}'.format(pos)]['data']
        break

peak_time_MDF, peak_value_MDF = bosmal_poland_data.peak_locator(1800, time_MDF, rpm_MDF, 1, 50)
if peak_time_MDF != 0:
    print("MDF datalog peak fount at second {} with value {}".format(peak_time_MDF,peak_value_MDF))

for name, pos in bosmal_sigmap.items():
    if name == 'N_ENGINE':
        rpm_BOSMAL = bosmal_poland_data_dict['{:03d}'.format(pos)]['data']
    elif name == 'recorder_time':
        time_BOSMAL = bosmal_poland_data_dict['{:03d}'.format(pos)]['data']
    else:
        continue

peak_time_BOSMAL, peak_value_BOSMAL = bosmal_poland_data.peak_locator(1800, time_BOSMAL, rpm_BOSMAL, 1, 3)

if peak_time_BOSMAL != 0 and peak_time_BOSMAL != 0:
    print("BOSMAL datalog peak fount at second {} with value {}".format(peak_time_BOSMAL/1000,peak_value_BOSMAL))
    print("Time GAP between Bosmal - Mdf datalogs = {}".format(peak_time_BOSMAL/1000-peak_time_MDF))
print("Ready for assigning values and other stuffs")

if len(mdf_sigmap_list) < 2:
    mdf_sigmap = mdf_sigmap_list[0]
    mdf_time_offset = peak_time_BOSMAL / 1000 - peak_time_MDF
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



t_BOSMAL = v_BOSMAL_recorder_time / 1000     # BOSMAL_POLAND datafile time in seconds
del v_BOSMAL_recorder_time

v_BOSMAL_Po= np.empty(len(t_BOSMAL))

v_BOSMAL_Po = v_BOSMAL_Torque * v_BOSMAL_N_ENGINE / 9548.8
l_BOSMAL_Po = 'Power'

emx_analysers_delays = {}

try:
    emx_analysers_delays['NOx'] = v_BOSMAL_Conc_NOX_TailPipe1_Delay[0]
except:
    emx_analysers_delays['NOx'] = DEF_NOX_ANALYSER_DELAY

try:
    emx_analysers_delays['HC'] = v_BOSMAL_Conc_HC_TailPipe1_Delay[0]
except:
    emx_analysers_delays['HC'] = DEF_HC_ANALYSER_DELAY

try:
    emx_analysers_delays['COL'] = v_BOSMAL_ConcDry_COL_TailPipe1_Delay[0]
except:
    emx_analysers_delays['COL'] = DEF_COL_ANALYSER_DELAY

try:
    emx_analysers_delays['CH4'] = v_BOSMAL_Conc_CH4_TailPipe1_Delay[0]
except:
    emx_analysers_delays['CH4'] = DEF_CH4_ANALYSER_DELAY

try:
    emx_analysers_delays['NH3'] = v_BOSMAL_Conc_NH3_TailPipe1_Delay[0]
except:
    emx_analysers_delays['NH3'] = DEF_NH3_ANALYSER_DELAY


v_BOSMAL_Conc_NOX_TailPipe1 = bosmal_poland_data.emx_analysers_delays_compensation(v_BOSMAL_Conc_NOX_TailPipe1,emx_analysers_delays['NOx'], 0.1)
v_BOSMAL_Conc_HC_TailPipe1 = bosmal_poland_data.emx_analysers_delays_compensation(v_BOSMAL_Conc_HC_TailPipe1,emx_analysers_delays['HC'], 0.1)
v_BOSMAL_ConcDry_COL_TailPipe1 = bosmal_poland_data.emx_analysers_delays_compensation(v_BOSMAL_ConcDry_COL_TailPipe1,emx_analysers_delays['COL'], 0.1)
v_BOSMAL_Conc_CH4_TailPipe1 = bosmal_poland_data.emx_analysers_delays_compensation(v_BOSMAL_Conc_CH4_TailPipe1,emx_analysers_delays['CH4'], 0.1)
v_BOSMAL_Conc_NH3_TailPipe1 = bosmal_poland_data.emx_analysers_delays_compensation(v_BOSMAL_Conc_NH3_TailPipe1, emx_analysers_delays['NH3'], 0.1)
del bosmal_poland_data_dict, bosmal_poland_data
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
qm_exh = v_BOSMAL_GAH / 3600        # from kg/h to kg/s
# if np.max(np.cumsum(qm_exh)) <= 5:
#     qm_exh = v_BOSMAL_FAIR / 3600
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
        m_NOx[i] = ppm2mg(u_gas['NOx'], v_BOSMAL_Conc_NOX_TailPipe1[i], qm_exh[i], T)
        m_CO[i] = ppm2mg(u_gas['CO'], v_BOSMAL_ConcDry_COL_TailPipe1[i], qm_exh[i], T)
        m_CH4[i] = ppm2mg(u_gas['CH4'], v_BOSMAL_Conc_CH4_TailPipe1[i], qm_exh[i], T)
        m_HC[i] = ppm2mg(u_gas['HC'], v_BOSMAL_Conc_HC_TailPipe1[i], qm_exh[i], T)
        m_CO2[i] = ppm2mg(u_gas['CO2'], v_BOSMAL_ConcDry_CO2_TailPipe1[i], qm_exh[i], T)

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

# Autoscale emissions cumsum y axis
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

# Autoscale emissions concentrations y axis
CO_max = np.max(v_BOSMAL_ConcDry_COL_TailPipe1)
# CH4_max = np.max(v_BOSMAL_Conc_CH4_TailPipe1)
NOx_max = np.max(v_BOSMAL_Conc_NOX_TailPipe1)
# THC_max = np.max(v_BOSMAL_Conc_HC_TailPipe1)
NH3_max = np.max(v_BOSMAL_Conc_NH3_TailPipe1)
MaxOfMax = np.max([CO_max,  NOx_max, NH3_max ])

if MaxOfMax < 2600.0:
    conc_range = [0, 2500]
elif MaxOfMax < 5500.0:
    conc_range = [0, 5000]     # mg
elif MaxOfMax < 10500.0:
    conc_range = [0, 10000]     # mg
elif MaxOfMax < 21000.0:
    conc_range = [0, 20000]     # mg
elif MaxOfMax < 52000.0:
    conc_range = [0, 50000]     # mg
elif MaxOfMax < 110000:
    conc_range = [0, 100000]     # mg
else:
    conc_range = [0, 500000]     # mg



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
    ax1.plot(t_BOSMAL, v_BOSMAL_N_ENGINE, linestyle= 'solid', color = '#FF7F00FF', label=l_BOSMAL_N_ENGINE)
    ax1.plot(t_BOSMAL, v_BOSMAL_Torque, linestyle='solid', color = '#007F00FF', label= l_BOSMAL_Torque)
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
    # ax3.plot(t_BOSMAL,v_BOSMAL_T1T, linestyle='solid',color = '#7F0000FF',label=l_BOSMAL_T1T)
    # ax3.plot(t_BOSMAL, v_BOSMAL_T1CAT, linestyle='solid',color = '#00FF00FF',label=l_BOSMAL_T1CAT)
    # ax3.plot(t_BOSMAL, v_BOSMAL_T2CAT, linestyle='solid',color = '#0000FFFF',label=l_BOSMAL_T2CAT)

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

    ax1.plot(t_BOSMAL, v_BOSMAL_N_ENGINE, linestyle= 'solid', color = '#FF7F00FF', label=l_BOSMAL_N_ENGINE)
    ax1.plot(t_BOSMAL, v_BOSMAL_Torque, linestyle='solid', color = '#007F00FF', label= l_BOSMAL_Torque)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],x_tick))
    ax1.set_ylim([0,2500])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250,2500])
    ax1.legend(shadow=True, loc=(LEGEND_UPPER_L),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_BOSMAL,v_BOSMAL_GAH, linestyle='solid',color = '#7F7FFFFF',label=l_BOSMAL_GAH)
    # ax2.plot(t_BOSMAL,v_BOSMAL_GEXH, linestyle='solid',color = '#FF0000FF',label=l_BOSMAL_GEXH)
    ax2.plot(t_BOSMAL,v_BOSMAL_FB_VAL_GEM, linestyle='solid',color = '#00FF00FF',label=l_BOSMAL_FB_VAL_GEM)
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

    # ## NH3 - CO - NOx concentrations
    if len(t_BOSMAL) >= 5:
        fig_name = "NH3-CO-NOx_Test_Emissions"
        print("Generating and writing the chart {} global of WHTC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_BOSMAL, v_BOSMAL_N_ENGINE, linestyle='solid', color='#FF7F00FF', label=l_BOSMAL_N_ENGINE)
        ax1.plot(t_BOSMAL, v_BOSMAL_Torque, linestyle='solid', color='#007F00FF', label=l_BOSMAL_Torque)
        ax1.set_xlim(x_lim)
        ax1.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax1.set_ylim([0, 2500])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax1.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_asEtasp, v_MDF_asEtasp, linestyle='solid', color='#7F7FFFFF', label=l_MDF_asEtasp)
        # ax2.plot(t_BOSMAL,v_BOSMAL_GEXH, linestyle='solid',color = '#FF0000FF',label=l_BOSMAL_GEXH)
        # ax2.plot(t_BOSMAL, v_BOSMAL_FB_VAL_GEM, linestyle='solid', color='#00FF00FF', label=l_BOSMAL_FB_VAL_GEM)
        ax2.set_ylim([0, 2])
        ax2.set_yticks(range(0, 2, 1))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_project_name + report_name + ' - NH3 concentration emission')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('asEtasp [adm]')

        ax3 = fig.add_subplot(212)

        ax3.plot(t_BOSMAL, v_BOSMAL_Conc_NOX_TailPipe1, linestyle='solid', color='#FF0000FF', label=l_BOSMAL_Conc_NOX_TailPipe1)
        ax3.plot(t_BOSMAL, v_BOSMAL_ConcDry_COL_TailPipe1_Delay, linestyle='solid', color='#0A0A0AFF', label=l_BOSMAL_ConcDry_COL_TailPipe1_Delay)
        ax3.plot(t_BOSMAL, v_BOSMAL_Conc_NH3_TailPipe1, linestyle='solid', color='#0AFFFFFF', label=l_BOSMAL_Conc_NH3_TailPipe1)
        ax3.set_xlim(x_lim)
        ax3.set_xticks(range(x_lim[0], x_lim[1], x_tick))
        ax3.set_ylim(conc_range)
        ax3.set_yticks(np.arange(conc_range[0], conc_range[1], int(conc_range[1] / 10)))
        ax3.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Cumulative emissions [mg]')
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
        # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
        plt.close('all')

    for WHTC_segment in WHTC_segments:
    # ## Emissions plus general segments
        fig_name = "Test_segment_{}_{}_seconds_Emissions".format(WHTC_segment[0], WHTC_segment[1])
        print("Generating and writing the chart {} segment in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_BOSMAL, v_BOSMAL_N_ENGINE, linestyle= 'solid', color = '#FF7F00FF', label=l_BOSMAL_N_ENGINE)
        ax1.plot(t_BOSMAL, v_BOSMAL_Torque, linestyle='solid', color = '#007F00FF', label= l_BOSMAL_Torque)
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

    # ## NH3 - CO - NOx concentrations
        fig_name = "NH3-CO-NOx_Test_Emissions""Test_segment_{}_{}_seconds_NH3-CO-NOx_Concentrations".format(WHTC_segment[0], WHTC_segment[1])
        print("Generating and writing the chart {} segment of WHTC test in {}".format(fig_name, data_path))
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax1 = fig.add_subplot(211)

        ax1.plot(t_BOSMAL, v_BOSMAL_N_ENGINE, linestyle='solid', color='#FF7F00FF', label=l_BOSMAL_N_ENGINE)
        ax1.plot(t_BOSMAL, v_BOSMAL_Torque, linestyle='solid', color='#007F00FF', label=l_BOSMAL_Torque)
        ax1.set_xlim(WHTC_segment)
        ax1.set_xticks(range(WHTC_segment[0], WHTC_segment[1], 25))
        ax1.set_ylim([0, 2500])
        ax1.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax1.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.plot(t_MDF_asEtasp, v_MDF_asEtasp, linestyle='solid', color='#7F7FFFFF', label=l_MDF_asEtasp)
        # ax2.plot(t_BOSMAL,v_BOSMAL_GEXH, linestyle='solid',color = '#FF0000FF',label=l_BOSMAL_GEXH)
        # ax2.plot(t_BOSMAL, v_BOSMAL_FB_VAL_GEM, linestyle='solid', color='#00FF00FF', label=l_BOSMAL_FB_VAL_GEM)
        ax2.set_ylim([0, 2])
        ax2.set_yticks(range(0, 2, 1))
        ax2.legend(shadow=True, loc=(LEGEND_UPPER_C), fontsize='xx-small')
        ax1.set_title(engine_project_name + report_name + ' - NH3 concentration emission')
        ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
        ax2.set_ylabel('asEtasp [adm]')

        ax3 = fig.add_subplot(212)

        ax3.plot(t_BOSMAL, v_BOSMAL_Conc_NOX_TailPipe1, linestyle='solid', color='#FF0000FF',
                 label=l_BOSMAL_Conc_NOX_TailPipe1)
        ax3.plot(t_BOSMAL, v_BOSMAL_ConcDry_COL_TailPipe1_Delay, linestyle='solid', color='#0A0A0AFF',
                 label=l_BOSMAL_ConcDry_COL_TailPipe1_Delay)
        ax3.plot(t_BOSMAL, v_BOSMAL_Conc_NH3_TailPipe1, linestyle='solid', color='#0AFFFFFF',
                 label=l_BOSMAL_Conc_NH3_TailPipe1)
        ax3.set_xlim(WHTC_segment)
        ax3.set_xticks(range(WHTC_segment[0], WHTC_segment[1], 25))
        ax3.set_ylim(conc_range)
        ax3.set_yticks(np.arange(conc_range[0], conc_range[1], int(conc_range[1] / 10)))
        ax3.legend(shadow=True, loc=(LEGEND_UPPER_L), fontsize='xx-small')

        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('Cumulative emissions [mg]')
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
        # esc_seq_dict['000']['gloabl_chart_png']=os.path.join(report_path,fig_name+'.png')
        fig.savefig(os.path.join(report_path, fig_name + '.svg'))
        # esc_seq_dict['000']['gloabl_chart_svg']=os.path.join(report_path,fig_name+'.svg')
        plt.close('all')

if peak_time_MDF != 0:
    print("MDF datalog peak fount at second {} with value {}".format(peak_time_MDF,peak_value_MDF))

if peak_time_BOSMAL != 0 and peak_time_BOSMAL != 0:
    print("BOSMAL datalog peak fount at second {} with value {}".format(peak_time_BOSMAL/1000,peak_value_BOSMAL))
    print("Time GAP between Bosmal - Mdf datalogs = {}".format(peak_time_BOSMAL/1000-peak_time_MDF))



print("Exit OK")
