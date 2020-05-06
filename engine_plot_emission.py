
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

MDF_file = "ESC_YAMZ-V8_LeanMixMode_20180809_C.TXT"
ADA_file ="V8_ESC_Testing_012.csv"
EMX_file ="ESC_20180809_C.txt"
AM_toff= -12.5
AE_toff=100

report_name = "ESC_report"

## TREATING MDF FROM CANAPE EXPORTED TO CSV (TXT FORMAT)
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

## Report section preparing figures

report_path = os.path.join(datafile_path,report_name)
if not (os.path.exists(report_path)):
    try:
        os.makedirs(report_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
## Temperatures plus general
fig_name = "ESC_WorkingPoints_Temperatures"

x1 = np.array(MDF_dict[44]['time'])+AM_toff ## bsRPM t
x2 = ADA_dict[0]['values'] ## brake speed t
x3 = np.array(EMX_dict[0]['values'])+AE_toff ## EMX t
x4 = ADA_dict[0]['values'] ## Brake Torque t
x5 = np.array(MDF_dict[17]['time'])+AM_toff ## zsTexh t
x6 = np.array(MDF_dict[56]['time'])+AM_toff  ## zsUegoLambda t


y1 = MDF_dict[44]['values'] ## bsRPM
y2 = ADA_dict[6]['values']  ## brake speed 
y3 = EMX_dict[3]['values'] ## EMX NOx 
y4 = ADA_dict[7]['values'] ## Brake Torque
y5 = np.array(MDF_dict[17]['values']) ## zsTexh
y6 = np.array(MDF_dict[56]['values'])  ## zsUegoLambda

# Contiguous series of exhaust temperature bulk treated
start_column = 12
n_line = 13  # starting column and conf of contiguous columns to be imported
y_temp = np.empty([n_line, len(ADA_dict[start_column]['values'])], dtype=float)
y_temp_label = []
# COLORS   '0        ','1        ','2        ','3        '4          ','5        ','6        ','7         ',
col_temp = ['#FF00FF7F', '#FF00FF9F', '#FF00FFBF', '#FF00FFDF', '#0000FF7F', '#0000FF9F', '#0000FFBF', '#0000FFDF',
            '#FF00FFFF', '#0000FFFF', '#7F007FFF', '#1FFF1F7F', '#1FFF1FEF']
#           '8          ','9        ','10       ','11       ','12        '

for temp in range(start_column, start_column + n_line):
    y_temp[temp - start_column, :] = np.array(ADA_dict[temp]['values'])
    y_temp_label.append(ADA_dict[temp]['name'])

fig = plt.figure(figsize=(10,8),dpi=200)
ax1 = fig.add_subplot(211)
ax1.plot(x1,y1,linestyle= 'solid',color = '#FF0000FF',label=MDF_dict[44]['name'])
ax1.plot(x2, y2,linestyle= 'solid',color = '#FF7F00FF',label=ADA_dict[6]['name'])
ax1.set_xlim([0,2400])
ax1.set_xticks(range(0,2400,120))
ax1.set_ylim([0,2250])
ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
ax1.legend(shadow=True, loc=(8),fontsize ='xx-small')
ax1.grid()
ax2 = ax1.twinx()
ax2.plot(x4,y4, linestyle='solid',color = '#007F00FF',label=ADA_dict[7]['name'])
ax2.set_ylim([0,2250])
ax2.set_yticks([0, 500,1000,1500,2000])
ax2.legend(shadow=True, loc=(9),fontsize ='xx-small')
ax1.set_title('Konzhak - ESC working points and temperatures')
ax1.set_ylabel('Engine speed')
ax2.set_ylabel('Engine torque')


ax3 = fig.add_subplot(212)

for temp in range(n_line):
    ax3.plot(x4,y_temp[temp], linestyle='solid',color = col_temp[temp],label=y_temp_label[temp])
ax3.plot(x5,y5, linestyle='solid',color = '#FF0000FF',label=MDF_dict[17]['name'])
ax3.set_xlim([0,2400])
ax3.set_xticks(range(0,2400,120))
ax3.set_ylim([300,800])
ax3.set_yticks(range(300,800,50))

ax3.set_xlabel('time (s)')
ax3.set_ylabel('Temperatures [degC]')
ax3.grid()
ax4 = ax3.twinx()
ax4.plot(x6,y6, linestyle='solid',color = '#7F7F003F',label=MDF_dict[56]['name'])
ax4.set_xlim([0,2400])
ax4.set_xticks(range(0,2400,120))
ax4.set_ylim([0.8,1.8])
ax4.set_yticks([0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8])
ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
ax4.legend(shadow=False, loc=(6),fontsize ='xx-small')
ax4.set_ylabel('Exhaust Lambda')
ax4.grid()

fig.tight_layout()
fig.savefig(os.path.join(report_path,fig_name+'.svg'))
fig.savefig(os.path.join(report_path,fig_name+'.png'))
del x1,y1,y3,col_temp,y_temp_label,ax1,ax2,ax3,ax4,fig,n_line,fig_name
    
## Emissions plus general
fig_name = "ESC_Emissions_Lambdas"


##x2 = ADA_dict[0]['values'] ## brake speed t
##x3 = np.array(EMX_dict[0]['values'])+AE_toff ## EMX t
##x4 = ADA_dict[0]['values'] ## Brake Torque t
##x5 = np.array(MDF_dict[17]['time'])+AM_toff ## zsTexh t
##x6 = np.array(MDF_dict[56]['time'])+AM_toff  ## zsUegoLambda t
##
##
##
##y2 = ADA_dict[6]['values']  ## brake speed 
##y4 = ADA_dict[7]['values'] ## Brake Torque
##y5 = np.array(MDF_dict[17]['values']) ## zsTexh
##y6 = np.array(MDF_dict[56]['values'])  ## zsUegoLambda

Tempo = x3
CH4 =np.array(EMX_dict[1]['values'])  ##1 CH4 ppm
NOx = np.array(EMX_dict[3]['values']) ##3 NOx ppm
LCO = np.array(EMX_dict[4]['values']) ##4 Basso LCO ppm
HCO = np.array(EMX_dict[5]['values'])/10000 ##5 Alto HCO %
CO2 = np.array(EMX_dict[6]['values'])/10000 ##6 CO2 %
HC  = np.array(EMX_dict[7]['values']) ##7 HC ppm

TOutTurbine= np.array(ADA_dict[22]['values'])
TInCat = np.array(ADA_dict[23]['values'])
TOutCat = np.array(ADA_dict[24]['values'])

fig = plt.figure(figsize=(10,8),dpi=200)
ax1 = fig.add_subplot(211)
ax1.plot(x2, y2,linestyle= 'solid',color = '#FF7F00FF',label=ADA_dict[6]['name'])
ax1.plot(x4,y4, linestyle='solid',color = '#007F00FF',label=ADA_dict[7]['name'])

ax1.set_xlim([0,2400])
ax1.set_xticks(range(0,2400,120))
ax1.set_ylim([0,2250])
ax1.set_yticks([0,250, 500,750,1000,1250,1500,1750,2000,2250])
ax1.legend(shadow=True, loc=(8),fontsize ='xx-small')
ax1.grid()
ax2 = ax1.twinx()
ax2.plot(x4, TOutTurbine,linestyle= 'solid',color = '#FF0F0FFF',label=ADA_dict[22]['name'])
ax2.plot(x4, TInCat,linestyle= 'solid',color = '#0F0F9FFF',label=ADA_dict[23]['name'])
ax2.plot(x4, TOutCat,linestyle= 'solid',color = '#0FCF0FFF',label=ADA_dict[24]['name'])
ax2.set_ylim([300,750])
ax2.set_yticks(range(300,750,50))
ax2.legend(shadow=True, loc=(9),fontsize ='xx-small')
ax1.set_title('Konzhak - ESC Emissions After Catalyst')
ax1.set_ylabel('Engine speed / torque')
ax2.set_ylabel('Catalyst Temperatures')


ax3 = fig.add_subplot(212)

ax3.plot(Tempo,CH4, linestyle='solid',color = '#0000FFFF',label=EMX_dict[1]['name'])
ax3.plot(Tempo,HC, linestyle='solid',color = '#7F7FFFFF',label=EMX_dict[7]['name'])
ax3.plot(Tempo,LCO, linestyle='solid',color = '#6F6F6FFF',label=EMX_dict[4]['name'])
ax3.plot(Tempo,NOx, linestyle='solid',color = '#DF0F0FFF',label=EMX_dict[3]['name'])
ax3.set_xlim([0,2400])
ax3.set_xticks(range(0,2400,120))
ax3.set_ylim([0,2000])
ax3.set_yticks(range(000,2000,200))

ax3.set_xlabel('time (s)')
ax3.set_ylabel('Emission CH4,HC,Low CO, NOx [ppm]')
ax3.grid()
ax4 = ax3.twinx()
ax4.plot(Tempo,HCO, linestyle='solid',color = '#0F0F0FFF',label=EMX_dict[5]['name'])
ax4.plot(Tempo,CO2, linestyle='solid',color = '#7F7F0FFF',label=EMX_dict[6]['name'])
ax4.set_xlim([0,2400])
ax4.set_xticks(range(0,2400,120))
ax4.set_ylim([0,10])
ax4.set_yticks(range(0,10,1))
ax3.legend(shadow=False, loc=(4),fontsize ='xx-small')
ax4.legend(shadow=False, loc=(6),fontsize ='xx-small')
ax4.set_ylabel('Emission HighCO,CO2 [%]')
ax4.grid()

fig.tight_layout()
fig.savefig(os.path.join(report_path,fig_name+'.svg'))
fig.savefig(os.path.join(report_path,fig_name+'.png'))
