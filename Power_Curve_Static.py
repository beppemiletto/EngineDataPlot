
"""
Simple demo with multiple subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os,errno
import pickle
import sys
import collections
import bisect
import xlrd

from matplotlib import colors as mcolors


def cell2data(col_range):
    data = []
    for cell in col_range:
        data.append(cell.value)

    return data


def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i
## INPUT DATA AND FILES DEFINITIONS


datafile_path = "D:\\Application_data\\Yuchai_K05N\\P20vsP13\\"

EXCEL_file = "K05N_Yuc_P20_vs_P13_vs_Rif.xlsx"

excel_book = xlrd.open_workbook(os.path.join(datafile_path,EXCEL_file))

graph_tile = "Yuchai K05N - Testing configurations"
report_name = "K05N_Yuc_P20_vs_P13_vs_Rif"

report_path = os.path.join(datafile_path,report_name)


if not os.path.exists(report_path):
    os.makedirs(report_path)


color_map = ['#ff0400FF', '#048F04FF', '#0404FFFF', '#040404FF' ]

print ("Nr. {} Sheets found in {}. Names ={}".format(excel_book.nsheets, EXCEL_file, excel_book.sheet_names()))

dsheet = excel_book.sheet_by_index(0)

curves_conf_labels_rows = [(9, 8), (24, 8), (39, 15)]

c_data = {}

for number, rows in enumerate(curves_conf_labels_rows):
    row=rows[0]
    data_rows = rows[1]
    
    c_data[number] = {}
    c_data[number]['conf_txt'] = dsheet.cell(row - 1, 0)
    c_data[number]['rpm'] = {}
    c_data[number]['rpm']['data'] = cell2data(dsheet.col_slice(0, row + 3, row + 3 + data_rows))
    c_data[number]['rpm']['label'] = dsheet.cell(row + 1, 0)
    c_data[number]['rpm']['um'] = dsheet.cell(row + 2, 0)

    c_data[number]['tinturb'] = {}
    c_data[number]['tinturb']['data'] = cell2data(dsheet.col_slice(1, row + 3, row + 3 + data_rows))
    c_data[number]['tinturb']['label'] = dsheet.cell(row + 1, 1)
    c_data[number]['tinturb']['um'] = dsheet.cell(row + 2, 1)

    c_data[number]['power'] = {}
    c_data[number]['power']['data'] = cell2data(dsheet.col_slice(2, row + 3, row + 3 + data_rows))
    c_data[number]['power']['label'] = dsheet.cell(row + 1, 2)
    c_data[number]['power']['um'] = dsheet.cell(row + 2, 2)

    c_data[number]['bsfc'] = {}
    c_data[number]['bsfc']['data'] = cell2data(dsheet.col_slice(3, row + 3, row + 3 + data_rows))
    c_data[number]['bsfc']['label'] = dsheet.cell(row + 1, 3)
    c_data[number]['bsfc']['um'] = dsheet.cell(row + 2, 3)

    c_data[number]['jsadv'] = {}
    c_data[number]['jsadv']['data'] = cell2data(dsheet.col_slice(4, row + 3, row + 3 + data_rows))
    c_data[number]['jsadv']['label'] = dsheet.cell(row + 1, 4)
    c_data[number]['jsadv']['um'] = dsheet.cell(row + 2, 4)


rpm_lim = [600,2400]
rpm_step=200                        #rpm for Power Curve
PowerCurve = True                   # Set True if plotting power Curve is needed, False if only plot f(time) needed

#########################################################
## Report section preparing figures
#########################################################
## preparing arrays for plotting ---------------

## Power Curve Plot f(RPM)
if PowerCurve:



    fig_name = "StatsPicture"

    fig = plt.figure(num=1,figsize=(210/25.4,297/25.4),dpi=300)
    gs1 = gridspec.GridSpec(nrows=60, ncols=1, left=0.15, right=0.85, wspace=0.00,hspace=0.10)
    ax1 = fig.add_subplot(gs1[0:24, :])
    ax2 = fig.add_subplot(gs1[25:36, :])
    ax3 = fig.add_subplot(gs1[37:48, :])
    ax4 = fig.add_subplot(gs1[49:-1, :])
    #
    # gs1 = gridspec.GridSpec(nrows=5, ncols=1, left=0.15, right=0.85, wspace=0.00,hspace=0.00)
    # ax1 = fig.add_subplot(gs1[0:2, :])
    # ax2 = fig.add_subplot(gs1[2, :])
    # ax3 = fig.add_subplot(gs1[3, :])
    # ax4 = fig.add_subplot(gs1[-1, :])

    #Power plot
    for key in c_data:
        ax1.plot(c_data[key]['rpm']['data'], c_data[key]['power']['data'],linestyle='solid',color = color_map[key],label=c_data[key]['conf_txt'])
    ax1.set_xlim(rpm_lim); ax1.set_xticks(range(rpm_lim[0],rpm_lim[-1],rpm_step))
    ax1.set_ylim(0,200);ax1.set_yticks(range(0,200,25),minor=True)
    ax1.set_xticklabels([])
    ax1.set_title(graph_tile)

    # ax1.get_xaxis().set_visible(False)
    ax1.set_ylabel('Engine Power [kW]')
    ax1.grid()


    #Torque plot with + and - 3 sigma
    # ax1r = ax1.twinx()

    #
    # ax1r.plot(PC_rpm,PC_torque,linestyle='solid',color = '#0404FFFF',label="Torque [Nm]")
    # ax1r.plot(PC_rpm,PC_torque_high,linestyle='solid',color = '#0404FF8F',label="+3 std")
    # ax1r.plot(PC_rpm,PC_torque_low,linestyle='solid',color = '#0404FF4F',label="-3 std")
    # ax1r.set_xlim(rpm_lim); ax1r.set_xticks(range(rpm_lim[0],rpm_lim[-1],rpm_step))
    # ax1r.set_ylim(500,2500);ax1r.set_yticks(range(500,2500,250),minor=True)
    # ax1r.set_ylabel('Engine Torque [Nm]')
    ax1.legend(shadow=False, loc=(3),fontsize ='xx-small')
    # ax1r.legend(shadow=False, loc=(4),fontsize ='xx-small')
    #
    # BSFC plot
    for key in c_data:
        ax2.plot(c_data[key]['rpm']['data'], c_data[key]['bsfc']['data'],linestyle='solid',color = color_map[key],label="BSFC [g/kWh]")
    ax2.set_xlim(rpm_lim);
    ax2.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax1.set_xticklabels([])
    ax2.set_ylim(100, 300);
    ax2.set_yticks(range(100, 300, 20), minor=True)
    ax2.set_ylabel("BSFC [g/kWh]")
    ax2.grid()
    # ax2.legend(shadow=False, loc=(3),fontsize ='xx-small')

    #TEXH  plot
    for key in c_data:
        ax3.plot(c_data[key]['rpm']['data'], c_data[key]['tinturb']['data'],linestyle='solid',color = color_map[key],label="Turbine Inlet Temperature [deg]")

    ax3.set_xlim(rpm_lim);
    ax3.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax1.set_xticklabels([])
    ax3.set_ylim(600, 900);
    ax3.set_yticks(range(600, 900, 50), minor=True)
    ax3.set_ylabel("Temperature [deg C]")
    ax3.grid()
    # ax3.legend(shadow=False, loc=(3), fontsize='xx-small')

    # JSADV plot
    for key in c_data:
        ax4.plot(c_data[key]['rpm']['data'], c_data[key]['jsadv']['data'],linestyle='solid',color = color_map[key],label="Spark Advance [deg]")
    ax4.set_xlim(rpm_lim);     ax4.set_xticks(range(rpm_lim[0], rpm_lim[-1], rpm_step))
    ax4.set_ylim(0, 50);     ax4.set_yticks(range(00, 50, 5), minor=True)
    ax4.set_xlabel('Engine speed [rpm]')
    ax4.set_ylabel('Spark ADvance [deg]')
    ax4.grid()
    # ax4r = ax4.twinx()
    # ax4r.plot(PC_rpm, PC_lambda, linestyle='solid', color='#717a36FF', label="Lambda [n]")
    # ax4r.set_xlim(rpm_lim);
    # ax4r.set_xticks(range(rpm_lim[0], rpm_lim[-1],rpm_step), minor=False)
    # ax4r.set_ylim(0.8, 1.6);
    # ax4r.set_yticks([0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6], minor=True)
    # ax4r.set_ylabel('Lambda=AFR/AFRstoich')
    # ax4.legend(shadow=False, loc=(3),fontsize ='xx-small')
    # ax4r.legend(shadow=False, loc=(4),fontsize ='xx-small')
    fig.savefig(os.path.join(report_path, fig_name + '.svg'))
    fig.savefig(os.path.join(report_path, fig_name + '.png'))