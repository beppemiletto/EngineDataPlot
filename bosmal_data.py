import csv
import os
import sys
import pickle

class Bosmal_Data():
    def __init__(self,data_path=None,bosmal_filename=None) -> object:
        """
        A parser of structured data from test bed
        :rtype: object
        """
        if data_path is not None:
            self.data_path = data_path
        else:
            return 1

        if bosmal_filename is not None:
            self.bosmal_filename = bosmal_filename
        else:
            return 2


        self.bosmal_filepath = os.path.join(self.data_path, self.bosmal_filename)

        self.bosmal_pickle_filename = self.bosmal_filename.split('.')[0]+'.pickle'
        self.bosmal_pickle_filepath = os.path.join(self.data_path,self.bosmal_pickle_filename)

        self.bosmal_dik = {}

    def load_data(self):
        if not os.path.exists(os.path.join(self.data_path,self.bosmal_filename)):
            return None
        try:
            s = os.stat(self.bosmal_pickle_filepath)
            if s.st_size == 0:
                print ( "The file {} is empty. Removing the 0 byte file and proceeding with data import.".format(self.bosmal_pickle_filepath))
                os.remove(self.bosmal_pickle_filepath)
        except OSError as e:
            print("Pickle file {} doesn't exist. Proceeding with data import. Wait! It can require long times!".format(self.bosmal_pickle_filepath))
        if not os.path.exists(self.bosmal_pickle_filepath):
            with open(self.bosmal_filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter ='\t')
                line_count = 0
                buffer_recovery_data = []
                for row in csv_reader:
                    if line_count== 0:
                        col_names= row
                        print(f'Column names are {", ".join(row)}')

                    elif line_count== 1:
                        print(f'Column meas units are {", ".join(row)}')
                        col_um = row

                        for idx,col_name in enumerate(col_names):
                            self.bosmal_dik['{:03d}'.format(idx)]= {}
                            self.bosmal_dik['{:03d}'.format(idx)]['name']=col_name.replace(' ','_').split('.')[-1]
                            self.bosmal_dik['{:03d}'.format(idx)]['mu']= col_um[idx]
                            self.bosmal_dik['{:03d}'.format(idx)]['data']=[]
                            buffer_recovery_data.append(0)
                        data_rows = 0
                    elif line_count> 1:

                        # print(f'Values conf  are {", ".join(row)}')
                        data_rows +=1
                        for idx,col_data in enumerate(row):
                            if col_data == '':
                                col_data = buffer_recovery_data[idx]
                            try:
                                self.bosmal_dik['{:03d}'.format(idx)]['data'].append(float(col_data))
                            except:
                                if idx  < len(col_names):
                                    self.bosmal_dik['{:03d}'.format(idx)]['data'].append(col_data)
                                else:
                                    break
                            buffer_recovery_data[idx]=col_data
                    line_count +=1
            print(f'Processed {line_count} lines.')

            with open(self.bosmal_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.bosmal_dik,pickle_file,protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.bosmal_pickle_filepath,mode='rb') as pickle_file:
                self.bosmal_dik = pickle.load(pickle_file)

        return self.bosmal_dik

