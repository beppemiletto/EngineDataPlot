import sys
import numpy as np
from aktakom_data import Akta_Data
from mdf_data import Mdf_Data
from rasp_data import Rasp_Data

import datetime

data_path = "D:\\projects\\Knocking_data"
enable_mdf  = False
mdf_filename = "MDF_wu_20190502.TXT"
enable_akta  = True
akta_filename = "Load_knock_1.txt"
enable_rasp = False
rasp_filename = "MDS_snP051_20190430_164334.csv"

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

if enable_rasp:
    print("Calling Raspberry data file parser with {} data file.".format(rasp_filename))
    rasp_data = Rasp_Data(data_path,rasp_filename)
    rasp_data_dict = rasp_data.load_data()
    if rasp_data_dict is None:
        print("Errore, controlla i dati di input for Raspberry datafile")
        sys.exit(2)
    else:
        print("Found {} columns in {} data file.".format(len(rasp_data_dict),rasp_filename))


if enable_akta:
    print("Calling AKTAKOM data file parser with {} data file.".format(akta_filename))
    aktakom_data = Akta_Data(data_path, akta_filename)
    aktakom_data_dict = aktakom_data.load_data()
    if aktakom_data_dict is None:
        print("Errore, controlla i dati di input of AKTAM datafile")
        sys.exit(2)
    else:
        print("Found {} data rows in {} data file.".format(len(aktakom_data_dict),akta_filename))





if enable_mdf:
    print("Calling CANAPE data file parser with {} data file.".format(mdf_filename))
    canape_data = Mdf_Data(data_path,mdf_filename)
    canape_data_dict = canape_data.load_data()
    if canape_data_dict is None:
        print("Errore, controlla i dati di input for MDF datafile")
        sys.exit(2)
    else:
        print("Found {} data rows in {} data file.".format(len(canape_data_dict),mdf_filename))






print('finish')

now = datetime.datetime.now()

print("Current date and time using isoformat: {}".format(now.isoformat()))

