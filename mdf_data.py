import csv
import os
import sys
import pickle

class Mdf_Data():
    def __init__(self,data_path=None,mdf_filename=None):
        if data_path is not None:
            self.data_path = data_path
        else:
            return 1

        if mdf_filename is not None:
            self.mdf_filename = mdf_filename
        else:
            return 2



# data_path = "D:\Application_data\Report_C13\HDS9"
# mdf_filename = "MDS_test_ESC_20190308_ASCII.csv"

        self.mdf_filepath = os.path.join(self.data_path, self.mdf_filename)

        self.mdf_pickle_filename = self.mdf_filename.split('.')[0]+'.pickle'
        self.mdf_pickle_filepath = os.path.join(self.data_path,self.mdf_pickle_filename)

        self.mdf_dik = {}

    def load_data(self):
        if not os.path.exists(os.path.join(self.data_path,self.mdf_filename)):
            return None
        try:
            s = os.stat(self.mdf_pickle_filepath)
            if s.st_size == 0:
                print ( "The file {} is empty. Removing the 0 byte file and proceeding with data import. Wait! It can require long times!".format(self.mdf_pickle_filepath))
                os.remove(self.mdf_pickle_filepath)
        except OSError as e:
            print("Pickle file {} doesn't exist. Proceeding with data import. Wait! It can require long times!".format(self.mdf_pickle_filepath))
        if not os.path.exists(self.mdf_pickle_filepath):
            with open(self.mdf_filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter =';', )
                line_count = 0
                for row in csv_reader:
                    if line_count== 0:
                        col_names= row
                        print(f'Column names are {", ".join(row)}')
                        for idx,col_name in enumerate(col_names):
                            name= col_name.split('[')[0]
                            um = col_name.split('[')[-1].split(']')[0]
                            if name != '':
                                self.mdf_dik['{:03d}'.format(idx)]= {}
                                self.mdf_dik['{:03d}'.format(idx)]['name']=name
                                self.mdf_dik['{:03d}'.format(idx)]['mu']= um
                                self.mdf_dik['{:03d}'.format(idx)]['data']=[]
                                self.mdf_dik['{:03d}'.format(idx)]['time']=[]
                        data_rows = 0
                        ts = 0.0

                    else :
                        # print(f'Values conf  are {", ".join(row)}')
                        if len(row)< len(self.mdf_dik):
                            break
                        data_rows +=1
                        for idx,col_data in enumerate(row):
                            if idx < len(self.mdf_dik):
                                if self.mdf_dik['{:03d}'.format(idx)]['name'] == 't':
                                    if data_rows == 1:
                                        # check if time start with some offset
                                        if float(col_data.replace(',','.'))> 0.0:
                                            mdf_t_offset = float(col_data.replace(',','.'))
                                        else:
                                            mdf_t_offset = 0.0
                                    ts = float(col_data.replace(',','.')) - mdf_t_offset
                                if col_data != ' ' and col_data != '':
                                    try:
                                        self.mdf_dik['{:03d}'.format(idx)]['data'].append(float(col_data.replace(',','.')))
                                        self.mdf_dik['{:03d}'.format(idx)]['time'].append(ts)
                                    except:
                                        if idx  < len(col_names):
                                            self.mdf_dik['{:03d}'.format(idx)]['data'].append(col_data)
                                            self.mdf_dik['{:03d}'.format(idx)]['time'].append(ts)
                                        else:
                                            break



                    line_count +=1
            print(f'Processed {line_count} lines.')
            del col_data, col_name, col_names, csv_reader, csv_file, idx, row, name, um, data_rows, line_count,ts
            with open(self.mdf_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.mdf_dik,pickle_file, protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.mdf_pickle_filepath,mode='rb') as pickle_file:
                self.mdf_dik = pickle.load(pickle_file)

        return self.mdf_dik

