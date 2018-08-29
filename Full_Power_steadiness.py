
"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import os,errno
import pickle
import sys
from matplotlib import colors as mcolors


def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i
## INPUT DATA AND FILES DEFINITIONS


datafile_path = "D:\\Application_data\\yamzv8data\\"

MDF_file = "Power_Steady_report_MDF.TXT"
ADA_file ="Test_power_steady_20180810.ASCII"
EMX_file =""
AM_toff= 0
AE_toff=100
x_lim=[0,720]
report_name = "Power_Steady_report"

## Define input signal location in columns
## MDF datafile parameters column number assignement
bsRPM=45; zsTExh=18; zsUegoLambda = 57; qsLamObtFin = 39; vsTorqueReqVCM2=31; zsMap = 10; asEtasp = 11; zsLambdaPost =12
zsPAtm = 13; zsPBoost = 14; zsTh2o=64; zsTAir=65; zsTRail=16; jsAdv=42; jsAdvBase=43

## ADAMO datafile parameters column number assignement
ADA_Pboost = 37; ADA_P_Intake_Manifold = 38; ADA_P_Inlet_Turbocharger=39 ; ADA_P_out_Turbine=40; ADA_P_In_Cat =41;
ADA_P_Out_Cat = 42; ADA_Brake_speed=6; ADA_Power_KW=4; ADA_Torque=7;ADA_CNG=9; ADA_T_h2o=25; ADA_T_H2O_Out_Engine=26
ADA_T_Asp_Cyl_1=27; ADA_T_Asp_Cyl_4 = 28; ADA_T_Asp_Cyl_5=29; ADA_T_Asp_Cyl_8=30; ADA_T_Gas_Out_Rid = 31
ADA_T_Gas_In_Rid= 32; ADA_T_Body_Reg = 33;ADA_T_Air_Env=11

## TREATING MDF FROM CANAPE EXPORTED TO CSV (TXT FORMAT)
if len(MDF_file)>=5:
    MDF_filename = MDF_file.split('.')[0]
    MDF_pickle_file = MDF_filename+'.pickle'

    MDF_pickle = os.path.join(datafile_path,MDF_pickle_file)

    if (os.path.exists(MDF_pickle)):
        print('Found pickle file {} : loading MDF data from it.'.format(MDF_pickle) )
        with open(MDF_pickle, 'rb') as handle:
            MDF_dict = pickle.load(handle)
    else:
        MDF_stream = os.path.join(datafile_path,MDF_file)

        print("MDF file to parse {}".format(MDF_stream))

        MDF_dict={}
        MDF_len_extimation = row_count(MDF_stream)
        print ("Total row approx {}".format(MDF_len_extimation-5))
        with open(MDF_stream, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            idx = 0
            for row in spamreader:
                if idx<1:
                    col_id=0
                    for column in row:
                        if len(column)>3:
                            
                            MDF_dict[col_id]={}
                            MDF_dict[col_id]['name']=column.split('[')[0]
                            MDF_dict[col_id]['mu']=column.split('[')[-1].split(']')[0]
                            MDF_dict[col_id]['time'] = []
                            MDF_dict[col_id]['values'] = []
                            col_id+=1

                    num_cols = col_id
                    print('total column {}'.format(num_cols))
                else:            
                    if len(row) == num_cols +1:
                        col_id=0
                        
                        for value in row:
                            if col_id == 0:
                                time_sample =float(value.replace(',','.'))
                                MDF_dict[0]['time'].append(time_sample)
                                MDF_dict[0]['values'].append(idx)
           
                            else:
                                try:
                                    value_num=float(value.replace(',','.'))
                                    MDF_dict[col_id]['time'].append(time_sample)
                                    MDF_dict[col_id]['values'].append(value_num)
                                except ValueError:
                                    pass
                            col_id+=1
                sys.stdout.write('\rParsed {} rows out of {}.'.format(idx,MDF_len_extimation))
                sys.stdout.flush()
                idx+=1

    ##            if idx > 500:
    ##                break
        print("END parsing")
        with open(MDF_pickle, 'wb') as handle:
            print('Writing pickle file {} : dumping MDF data into it.'.format(MDF_pickle) )
            pickle.dump(MDF_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("MDF data names:")
    for key, value in MDF_dict.items():
        print (key,value['name'])
    print()
## TREATING ADAMO DATAFILE .ASCII OR .CSV

if len(ADA_file)>=5:
    ADA_filename = ADA_file.split('.')[0]
    ADA_pickle_file = ADA_filename+'.pickle'

    ADA_pickle = os.path.join(datafile_path,ADA_pickle_file)

    if (os.path.exists(ADA_pickle)):
        print('Found pickle file {} : loading ADAMO data from it.'.format(ADA_pickle) )
        with open(ADA_pickle, 'rb') as handle:
            ADA_dict = pickle.load(handle)
    else:
        ADA_stream = os.path.join(datafile_path,ADA_file)

        print("ADAMO file to parse {}".format(ADA_stream))

        ADA_dict={}
        ADA_len_extimation = row_count(ADA_stream)
        print ("Total row approx {}".format(ADA_len_extimation-5))
        with open(ADA_stream, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            idx = 0
            for row in spamreader:
                if idx==10:
                    col_id=0
                    for column in row:
                        if len(column)>=1:
                            print (column)
                            ADA_dict[col_id]={}
                            ADA_dict[col_id]['name']=column
                            ADA_dict[col_id]['mu']=''
                            ADA_dict[col_id]['values'] = []
                            col_id+=1

                    num_cols = col_id
                    print('total column {}'.format(num_cols))
                elif idx==11:
                    col_id=0
                    for column in row:
                        if len(column)>=1:
                            print (column)
                            ADA_dict[col_id]['mu']=column
                            col_id+=1
                elif idx > 11:
    ##                print(len(row) ,num_cols)
                    if len(row) >= num_cols:
                        col_id=0
                        
                        for value in row:
                            if col_id == 0:
                                if idx==12:
                                    t0=float(value)
                                time_sample =float(value)-t0
                                ADA_dict[0]['values'].append(time_sample)
    ##                            print(idx, time_sample)
           
                            else:
                                try:
                                    value_num=float(value)
                                    ADA_dict[col_id]['values'].append(value_num)
                                except ValueError:
                                    pass
                                except KeyError:
                                    pass
                            col_id+=1
                sys.stdout.write('\rParsed {} rows out of {}.'.format(idx,ADA_len_extimation))
                sys.stdout.flush()
                idx+=1

        print("END parsing")
        with open(ADA_pickle, 'wb') as handle:
            print('Writing pickle file {} : dumping ADAMO data into it.'.format(ADA_pickle) )
            pickle.dump(ADA_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for key, value in ADA_dict.items():
        print (key,value['name'])
    print()

## TREATING EMISSIONS DATAFILE .txt

if len(EMX_file)>=5:
    EMX_filename = EMX_file.split('.')[0]
    EMX_pickle_file = EMX_filename+'.pickle'

    EMX_pickle = os.path.join(datafile_path,EMX_pickle_file)

    if (os.path.exists(EMX_pickle)):
        print('Found pickle file {} : loading EMISSIONS data from it.'.format(EMX_pickle) )
        with open(EMX_pickle, 'rb') as handle:
            EMX_dict = pickle.load(handle)
    else:
        EMX_stream = os.path.join(datafile_path,EMX_file)

        print("EMISSIONS file to parse {}".format(EMX_stream))

        EMX_dict={}
        EMX_len_extimation = row_count(EMX_stream)
        print ("Total row approx {}".format(EMX_len_extimation-1))
        with open(EMX_stream, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            idx = 0
            for row in spamreader:
                if idx==0:
                    col_id=0
                    for column in row:
                        EMX_dict[col_id]={}
                        EMX_dict[col_id]['name']=column
                        EMX_dict[col_id]['mu']=''
                        EMX_dict[col_id]['values'] = []
                        col_id+=1

                    num_cols = col_id
                    print('total column {}'.format(num_cols))

                else:
    ##                print(len(row) ,num_cols)
                    if len(row) == num_cols+1:
                        col_id=0
                        
                        for value in row:
                            if col_id == 0:
                                time_sample =float(value)
                                EMX_dict[0]['values'].append(time_sample)
    ##                            print(idx, time_sample)
           
                            else:
                                try:
                                    value_num=float(value)
                                    EMX_dict[col_id]['values'].append(value_num)
                                except ValueError:
                                    pass
                                except KeyError:
                                    pass
                            col_id+=1
                sys.stdout.write('\rParsed {} rows out of {}.'.format(idx,EMX_len_extimation))
                sys.stdout.flush()
                idx+=1

        print("END parsing")
        with open(EMX_pickle, 'wb') as handle:
            print('Writing pickle file {} : dumping EMISSIONS data into it.'.format(EMX_pickle) )
            pickle.dump(EMX_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for key, value in EMX_dict.items():
        print (key,value['name'])
    print()

#########################################################
## Report section preparing figures
#########################################################

## preparing arrays for plotting ---------------
t_MDF_bsRPM = np.array(MDF_dict[bsRPM]['time'])+AM_toff ## bsRPM t
v_MDF_bsRPM = MDF_dict[bsRPM]['values'] ## bsRPM
l_MDF_bsRPM = MDF_dict[bsRPM]['name']  ## bsRPM label

t_MDF_zsTExh = np.array(MDF_dict[zsTExh]['time'])+AM_toff ## zsTexh t
v_MDF_zsTexh = np.array(MDF_dict[zsTExh]['values']) ## zsTexh
l_MDF_zsTexh = np.array(MDF_dict[zsTExh]['name'])  ## zsTexh label

t_MDF_zsUegoLambda = np.array(MDF_dict[zsUegoLambda]['time'])+AM_toff  ## zsUegoLambda t
v_MDF_zsUegoLambda = np.array(MDF_dict[zsUegoLambda]['values'])  ## zsUegoLambda
l_MDF_zsUegoLambda = np.array(MDF_dict[zsUegoLambda]['name'])  ## zsUegoLambda label

t_MDF_qsLamObtFin = np.array(MDF_dict[qsLamObtFin]['time']) ## qsLamObtFin t
v_MDF_qsLamObtFin = np.array(MDF_dict[qsLamObtFin]['values'])  ## qsLamObtFin
l_MDF_qsLamObtFin = np.array(MDF_dict[qsLamObtFin]['name'])  ## qsLamObtFin label

t_MDF_vsTorqueReqVCM2 = np.array(MDF_dict[vsTorqueReqVCM2]['time'])+AM_toff ## vsTorqueReqVCM2 t
v_MDF_vsTorqueReqVCM2 = np.array(MDF_dict[vsTorqueReqVCM2]['values'])  ## vsTorqueReqVCM2
l_MDF_vsTorqueReqVCM2 = np.array(MDF_dict[vsTorqueReqVCM2]['name'])  ## vsTorqueReqVCM2 label

t_MDF_zsMap = np.array(MDF_dict[zsMap]['time']) + AM_toff  ## zsMap t
v_MDF_zsMap = np.array(MDF_dict[zsMap]['values'])  ## zsMap
l_MDF_zsMap = np.array(MDF_dict[zsMap]['name'])  ## zsMap label

t_MDF_zsPBoost = np.array(MDF_dict[zsPBoost]['time']) + AM_toff  ## zsPBoost t
v_MDF_zsPBoost = np.array(MDF_dict[zsPBoost]['values'])  ## zsPBoost
l_MDF_zsPBoost = np.array(MDF_dict[zsPBoost]['name'])  ## zsPBoost label

t_MDF_zsTh2o = np.array(MDF_dict[zsTh2o]['time']) + AM_toff  ## zsTh2o t
v_MDF_zsTh2o = np.array(MDF_dict[zsTh2o]['values'])  ## zsTh2o
l_MDF_zsTh2o = np.array(MDF_dict[zsTh2o]['name'])  ## zsTh2o label

t_MDF_zsTAir = np.array(MDF_dict[zsTAir]['time']) + AM_toff  ## zsTAir t
v_MDF_zsTAir = np.array(MDF_dict[zsTAir]['values'])  ## zsTAir
l_MDF_zsTAir = np.array(MDF_dict[zsTAir]['name'])  ## zsTAir label

t_MDF_zsTRail = np.array(MDF_dict[zsTRail]['time']) + AM_toff  ## zsTRail t
v_MDF_zsTRail = np.array(MDF_dict[zsTRail]['values'])  ## zsTRail
l_MDF_zsTRail = np.array(MDF_dict[zsTRail]['name'])  ## zsTRail label

t_MDF_jsAdv = np.array(MDF_dict[jsAdv]['time']) + AM_toff  ## jsAdv t
v_MDF_jsAdv = np.array(MDF_dict[jsAdv]['values'])  ## jsAdv
l_MDF_jsAdv = np.array(MDF_dict[jsAdv]['name'])  ## jsAdv label

t_MDF_jsAdvBase = np.array(MDF_dict[jsAdvBase]['time']) + AM_toff  ## jsAdvBase t
v_MDF_jsAdvBase = np.array(MDF_dict[jsAdvBase]['values'])  ## jsAdvBase
l_MDF_jsAdvBase = np.array(MDF_dict[jsAdvBase]['name'])  ## jsAdvBase label

t_ADA = ADA_dict[0]['values'] ## ADAMO datafile time

v_ADA_RPM = ADA_dict[ADA_Brake_speed]['values']  ## brake speed
l_ADA_RPM = ADA_dict[ADA_Brake_speed]['name']  ## brake speed label

v_ADA_Torque = ADA_dict[ADA_Torque]['values'] ## Brake Torque
l_ADA_Torque = ADA_dict[ADA_Torque]['name'] ## Brake Torque label

v_ADA_PowerKW = ADA_dict[ADA_Power_KW]['values'] ## Engine Power
l_ADA_PowerKW = ADA_dict[ADA_Power_KW]['name'] ## Engine Power label

v_ADA_Pboost = ADA_dict[ADA_Pboost]['values'] ## Pboost
l_ADA_Pboost = ADA_dict[ADA_Pboost]['name'] ## Pboost label

v_ADA_P_Intake_Manifold = ADA_dict[ADA_P_Intake_Manifold]['values'] ## P_Intake_Manifold
l_ADA_P_Intake_Manifold = ADA_dict[ADA_P_Intake_Manifold]['name'] ## P_Intake_Manifold label

v_ADA_P_Inlet_Turbocharger = ADA_dict[ADA_P_Inlet_Turbocharger]['values'] ## P_Inlet_Turbocharger
l_ADA_P_Inlet_Turbocharger = ADA_dict[ADA_P_Inlet_Turbocharger]['name'] ## P_Inlet_Turbocharger label

v_ADA_P_out_Turbine = ADA_dict[ADA_P_out_Turbine]['values'] ## P_out_Turbine
l_ADA_P_out_Turbine = ADA_dict[ADA_P_out_Turbine]['name'] ## P_out_Turbine label

v_ADA_P_In_Cat = ADA_dict[ADA_P_In_Cat]['values']  ## P_In_Cat
l_ADA_P_In_Cat = ADA_dict[ADA_P_In_Cat]['name']  ## P_In_Cat label

v_ADA_P_Out_Cat = ADA_dict[ADA_P_Out_Cat]['values']  ## P_Out_Cat
l_ADA_P_Out_Cat = ADA_dict[ADA_P_Out_Cat]['name']  ## P_Out_Cat label

v_ADA_CNG = ADA_dict[ADA_CNG]['values']  ## CNG
l_ADA_CNG = ADA_dict[ADA_CNG]['name']  ## CNG label

v_ADA_T_Air_Env = ADA_dict[ADA_T_Air_Env]['values']  ## T_Air_Env
l_ADA_T_Air_Env = ADA_dict[ADA_T_Air_Env]['name']  ## T_Air_Env label

v_ADA_T_h2o = ADA_dict[ADA_T_h2o]['values']  ## T_h2o
l_ADA_T_h2o = ADA_dict[ADA_T_h2o]['name']  ## T_h2o label

v_ADA_T_H2O_Out_Engine = ADA_dict[ADA_T_H2O_Out_Engine]['values']  ## T_H2O_Out_Engine
l_ADA_T_H2O_Out_Engine = ADA_dict[ADA_T_H2O_Out_Engine]['name']  ## T_H2O_Out_Engine label

v_ADA_T_Asp_Cyl_1 = ADA_dict[ADA_T_Asp_Cyl_1]['values']  ## T_Asp_Cyl_1
l_ADA_T_Asp_Cyl_1 = ADA_dict[ADA_T_Asp_Cyl_1]['name']  ## T_Asp_Cyl_1 label

v_ADA_T_Asp_Cyl_4 = ADA_dict[ADA_T_Asp_Cyl_4]['values']  ## T_Asp_Cyl_4
l_ADA_T_Asp_Cyl_4 = ADA_dict[ADA_T_Asp_Cyl_4]['name']  ## T_Asp_Cyl_4 label

v_ADA_T_Asp_Cyl_5 = ADA_dict[ADA_T_Asp_Cyl_5]['values']  ## T_Asp_Cyl_5
l_ADA_T_Asp_Cyl_5 = ADA_dict[ADA_T_Asp_Cyl_5]['name']  ## T_Asp_Cyl_5 label

v_ADA_T_Asp_Cyl_8 = ADA_dict[ADA_T_Asp_Cyl_8]['values']  ## T_Asp_Cyl_8
l_ADA_T_Asp_Cyl_8 = ADA_dict[ADA_T_Asp_Cyl_8]['name']  ## T_Asp_Cyl_8 label

v_ADA_T_Gas_Out_Rid = ADA_dict[ADA_T_Gas_Out_Rid]['values']  ## T_Gas_Out_Rid
l_ADA_T_Gas_Out_Rid = ADA_dict[ADA_T_Gas_Out_Rid]['name']  ## T_Gas_Out_Rid label

v_ADA_T_Gas_In_Rid = ADA_dict[ADA_T_Gas_In_Rid]['values']  ## T_Gas_In_Rid
l_ADA_T_Gas_In_Rid = ADA_dict[ADA_T_Gas_In_Rid]['name']  ## T_Gas_In_Rid label

v_ADA_T_Body_Reg = ADA_dict[ADA_T_Body_Reg]['values']  ## T_Body_Reg
l_ADA_T_Body_Reg = ADA_dict[ADA_T_Body_Reg]['name']  ## T_Body_Reg label

# Calculated parameters
cv_ADA_BSFC = np.array(v_ADA_CNG,dtype='float')/np.array(v_ADA_PowerKW,dtype='float')*1000
cl_ADA_BSFC = "BSFC gr/kWh"

# Contiguous series of exhaust temperature bulk treated
start_column = 12
n_line = 13  # starting column and number of contiguous columns to be imported
y_temp = np.empty([n_line, len(ADA_dict[start_column]['values'])], dtype=float)
y_temp_label = []
# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '

for temp in range(start_column, start_column + n_line):
    y_temp[temp - start_column, :] = np.array(ADA_dict[temp]['values'])
    y_temp_label.append(ADA_dict[temp]['name'])



report_path = os.path.join(datafile_path,report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
## Temperatures plus general
if len(ADA_file)>=5 and len(MDF_file)>=5:
    fig_name = "PowerSteady_WorkingPoints_Temperatures"
    fig = plt.figure(figsize=(10,8),dpi=200)
    ax1 = fig.add_subplot(211)
    ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=MDF_dict[bsRPM]['name'])
    ax1.plot(t_ADA, v_ADA_RPM,linestyle= 'solid',color = '#FF7F00FF',label=ADA_dict[6]['name'])
    ax1.plot(t_ADA,v_ADA_Torque, linestyle='solid',color = '#007F00FF',label=ADA_dict[7]['name'])
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],120))
    ax1.set_ylim([0,2250])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
    ax1.legend(shadow=True, loc=(8),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_ADA,v_ADA_PowerKW, linestyle='solid',color = '#ff0087FF',label=ADA_dict[4]['name'])
    ax2.set_ylim([0,450])
    ax2.set_yticks(range(0,450,50))
    ax2.legend(shadow=True, loc=(9),fontsize ='xx-small')
ax1.set_title('Konzhak - '+report_name+' - working points and temperatures')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Engine Power [kW]')


    ax3 = fig.add_subplot(212)

    for temp in range(n_line):
        ax3.plot(t_ADA,y_temp[temp], linestyle='solid',color = col_temp[temp],label=y_temp_label[temp])
    ax3.plot(t_MDF_zsTExh,v_MDF_zsTexh, linestyle='solid',color = '#FF0000FF',label=MDF_dict[zsTExh]['name'])
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],120))
    ax3.set_ylim([300,800])
    ax3.set_yticks(range(300,800,50))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=MDF_dict[zsUegoLambda]['name'])
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=MDF_dict[qsLamObtFin]['name'])
    ax4.set_ylim([0.8,1.8])
    ax4.set_yticks([0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8])
    ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
    ax4.legend(shadow=False, loc=(6),fontsize ='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    fig.savefig(os.path.join(report_path,fig_name+'.png'))


## Environmental plus combustion
if len(ADA_file)>=5 and len(MDF_file)>=5:
    fig_name = "PowerSteady_Environment_Combustion"
    fig = plt.figure(figsize=(10,12),dpi=200)
    ax1 = fig.add_subplot(311)
    ax1.plot(t_MDF_bsRPM,v_MDF_bsRPM,linestyle= 'solid',color = '#FF0000FF',label=MDF_dict[bsRPM]['name'])
    ax1.plot(t_ADA, v_ADA_RPM,linestyle= 'solid',color = '#FF7F00FF',label=ADA_dict[6]['name'])
    ax1.plot(t_ADA,v_ADA_Torque, linestyle='solid',color = '#007F00FF',label=ADA_dict[7]['name'])
    ax1.plot(t_MDF_vsTorqueReqVCM2,v_MDF_vsTorqueReqVCM2, linestyle='solid',color = '#2F2F2FFF',label=MDF_dict[vsTorqueReqVCM2]['name'])
    ax1.set_xlim(x_lim)
    ax1.set_xticks(range(x_lim[0],x_lim[1],120))
    ax1.set_ylim([0,2250])
    ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
    ax1.legend(shadow=True, loc=(8),fontsize ='xx-small')
    ax1.grid()
    ax2 = ax1.twinx()
    ax2.plot(t_ADA,v_ADA_PowerKW, linestyle='solid',color = '#ff0087FF',label=ADA_dict[4]['name'])
    ax2.plot(t_ADA,cv_ADA_BSFC, linestyle='solid',color = '#7e0640FF',label=cl_ADA_BSFC)
    ax2.set_ylim([0,450])
    ax2.set_yticks(range(0,450,50))
    ax2.legend(shadow=True, loc=(9),fontsize ='xx-small')
ax1.set_title('Konzhak - '+report_name+' - Environmental and Combustion')
    ax1.set_ylabel('Engine speed [rpm]/ Torque [Nm]')
    ax2.set_ylabel('Engine Power [kW]/ BSFC [g/kWh]')


    ax3 = fig.add_subplot(312)

    ax3.plot(t_MDF_zsPBoost,v_MDF_zsPBoost, linestyle='solid',color = '#FF0000FF',label=l_MDF_zsPBoost)
    ax3.plot(t_ADA,v_ADA_Pboost, linestyle='solid',color = '#AF0000FF',label=l_ADA_Pboost)
    ax3.plot(t_MDF_zsMap,v_MDF_zsMap, linestyle='solid',color = '#00007FFF',label=l_MDF_zsMap)
    ax3.plot(t_ADA,v_ADA_P_Intake_Manifold, linestyle='solid',color = '#00008FFF',label=l_ADA_P_Intake_Manifold)
    ax3.plot(t_ADA,v_ADA_P_Inlet_Turbocharger, linestyle='solid',color = '#b26f19FF',label=l_ADA_P_Inlet_Turbocharger)
    ax3.plot(t_ADA,v_ADA_P_out_Turbine, linestyle='solid',color = '#553915FF',label=l_ADA_P_out_Turbine)
    ax3.plot(t_ADA,v_ADA_P_In_Cat, linestyle='solid',color = '#1e6315FF',label=l_ADA_P_In_Cat)
    ax3.plot(t_ADA,v_ADA_P_Out_Cat, linestyle='solid',color = '#24a614FF',label=l_ADA_P_Out_Cat)

    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],120))
    ax3.set_ylim([0,3000])
    ax3.set_yticks(range(0,3000,250))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Pressures [mbar]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_zsUegoLambda,v_MDF_zsUegoLambda, linestyle='solid',color = '#7F7F003F',label=MDF_dict[zsUegoLambda]['name'])
    ax4.plot(t_MDF_qsLamObtFin,v_MDF_qsLamObtFin, linestyle='solid',color = '#bF7F008F',label=MDF_dict[qsLamObtFin]['name'])
    ax4.set_ylim([0.8,2.0])
    ax4.set_yticks([0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8])
    ax3.legend(shadow=False, loc=(3),fontsize ='xx-small')
    ax4.legend(shadow=False, loc=(4),fontsize ='xx-small')
    ax4.set_ylabel('Exhaust Lambda')
    ax4.grid()

    ax3 = fig.add_subplot(313)


    ax3.plot(t_MDF_zsTAir,v_MDF_zsTAir, linestyle='solid',color = '#0b6eceFF',label=l_MDF_zsTAir)
    ax3.plot(t_MDF_zsTh2o,v_MDF_zsTh2o, linestyle='solid',color = '#a82c1bFF',label=l_MDF_zsTh2o)
    ax3.plot(t_MDF_zsTRail,v_MDF_zsTRail, linestyle='solid',color = '#13800dFF',label=l_MDF_zsTRail)
    ax3.plot(t_ADA,v_ADA_T_Air_Env, linestyle='solid',color = '#878dffFF',label=l_ADA_T_Air_Env)
    ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_1, linestyle='solid',color = '#ff15ce9F',label=l_ADA_T_Asp_Cyl_1)
    ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_4, linestyle='solid',color = '#ff15ceCF',label=l_ADA_T_Asp_Cyl_4)
    ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_1, linestyle='solid',color = '#0d10809F',label=l_ADA_T_Asp_Cyl_5)
    ax3.plot(t_ADA,v_ADA_T_Asp_Cyl_4, linestyle='solid',color = '#0d1080CF',label=l_ADA_T_Asp_Cyl_8)
    ax3.plot(t_ADA,v_ADA_T_Body_Reg, linestyle='solid',color = '#31b62bCF',label=l_ADA_T_Body_Reg)
    ax3.plot(t_ADA,v_ADA_T_Gas_Out_Rid, linestyle='solid',color = '#103b0eCF',label=l_ADA_T_Gas_Out_Rid)
    ax3.set_xlim(x_lim)
    ax3.set_xticks(range(x_lim[0],x_lim[1],120))
    ax3.set_ylim([-40,120])
    ax3.set_yticks(range(-40,120,10))

    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('Temperatures [degC]')
    ax3.grid()
    ax4 = ax3.twinx()
    ax4.plot(t_MDF_jsAdv,v_MDF_jsAdv, linestyle='solid',color = '#ff04004F',label=l_MDF_jsAdv)
    ax4.plot(t_MDF_jsAdvBase,v_MDF_jsAdvBase, linestyle='solid',color = '#bf0400CF',label=l_MDF_jsAdvBase)

    ax4.set_ylim([-20,60])
    ax4.set_yticks(range(-20,60,10))
    ax3.legend(shadow=False, loc=(3),fontsize ='xx-small')
    ax4.legend(shadow=False, loc=(4),fontsize ='xx-small')
    ax4.set_ylabel('Spark Advance [deg BTDC]')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(os.path.join(report_path,fig_name+'.svg'))
    fig.savefig(os.path.join(report_path,fig_name+'.png'))


    
