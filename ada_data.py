import csv
import os
import sys
import pickle

class Ada_Data():
    def __init__(self,data_path=None,ada_filename=None):
        if data_path is not None:
            self.data_path = data_path
        else:
            return 1

        if ada_filename is not None:
            self.ada_filename = ada_filename
        else:
            return 2



# data_path = "D:\Application_data\Report_C13\HDS9"
# rasp_filename = "MDS_test_ESC_20190308_ASCII.csv"

        self.ada_filepath = os.path.join(self.data_path, self.ada_filename)

        self.ada_pickle_filename = self.ada_filename.split('.')[0]+'.pickle'
        self.ada_pickle_filepath = os.path.join(self.data_path,self.ada_pickle_filename)

        self.ada_dik = {}

    def load_data(self):
        if not os.path.exists(os.path.join(self.data_path,self.ada_filename)):
            return None
        try:
            s = os.stat(self.ada_pickle_filepath)
            if s.st_size == 0:
                print ( "The file {} is empty. Removing the 0 byte file and proceeding with data import. Wait! It can require long times!".format(self.ada_pickle_filepath))
                os.remove(self.ada_pickle_filepath)
        except OSError as e:
            print("Pickle file {} doesn't exist. Proceeding with data import. Wait! It can require long times!".format(self.ada_pickle_filepath))
        if not os.path.exists(self.ada_pickle_filepath):
            with open(self.ada_filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter ='\t', )
                line_count = 0
                for row in csv_reader:
                    if line_count== 10:
                        col_names= row
                        print(f'Column names are {", ".join(row)}')

                    elif line_count== 11:
                        print(f'Column meas units are {", ".join(row)}')
                        col_um = row

                        for idx,col_name in enumerate(col_names):
                            self.ada_dik['{:03d}'.format(idx)]= {}
                            self.ada_dik['{:03d}'.format(idx)]['name']=col_name.replace(' ','_')
                            self.ada_dik['{:03d}'.format(idx)]['mu']= col_um[idx]
                            self.ada_dik['{:03d}'.format(idx)]['data']=[]
                        data_rows = 0
                    elif line_count> 11:
                        # print(f'Values number  are {", ".join(row)}')

                        data_rows +=1
                        for idx,col_data in enumerate(row):
                            try:
                                self.ada_dik['{:03d}'.format(idx)]['data'].append(float(col_data))
                            except:
                                if idx  < len(col_names):
                                    self.ada_dik['{:03d}'.format(idx)]['data'].append(col_data)
                                else:
                                    break



                    line_count +=1
            print(f'Processed {line_count} lines.')

            with open(self.ada_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.ada_dik,pickle_file,protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.ada_pickle_filepath,mode='rb') as pickle_file:
                self.ada_dik = pickle.load(pickle_file)

        return self.ada_dik

