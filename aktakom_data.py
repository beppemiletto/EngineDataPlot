import csv
import os
import sys
import pickle

class Akta_Data():
    def __init__(self,data_path=None,akta_filename=None):
        if data_path is not None:
            self.data_path = data_path
        else:
            return 1

        if akta_filename is not None:
            self.akta_filename = akta_filename
        else:
            return 2



# data_path = "D:\Application_data\Report_C13\HDS9"
# rasp_filename = "MDS_test_ESC_20190308_ASCII.csv"

        self.akta_filepath = os.path.join(self.data_path, self.akta_filename)

        self.akta_pickle_filename = self.akta_filename.split('.')[0]+'.pickle'
        self.akta_pickle_filepath = os.path.join(self.data_path,self.akta_pickle_filename)

        self.akta_dik = {}

    def load_data(self):
        if not os.path.exists(os.path.join(self.data_path,self.akta_filename)):
            return None
        try:
            s = os.stat(self.akta_pickle_filepath)
            if s.st_size == 0:
                print ( "The file {} is empty. Removing the 0 byte file and proceeding with data import. Wait! It can require long times!".format(self.akta_pickle_filepath))
                os.remove(self.akta_pickle_filepath)
        except OSError as e:
            print("Pickle file {} doesn't exist. Proceeding with data import. Wait! It can require long times!".format(self.akta_pickle_filepath))
        if not os.path.exists(self.akta_pickle_filepath):
            with open(self.akta_filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter =' ',skipinitialspace=True )
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        um = row[-1].split(':')[-1]

                    elif line_count== 1:
                        col_names= row
                        print(f'Column names are {", ".join(row)}')
                        col_names.append(col_names[-1])
                        time_col_names = []
                        for pos,col in enumerate(col_names):
                            if pos==0:
                                time_col_names.append('time')
                            if pos == len(col_names)-1:
                                continue
                            else:
                                time_col_names.append(col_names[pos])
                        col_names=[]
                        col_um=[]

                        for col in time_col_names:
                            col_names.append(col)
                            if col== 'time':
                                col_um.append('s')
                            else:
                                col_um.append(um)
                        col_names = time_col_names

                        del time_col_names, col
                        for idx,col_name in enumerate(col_names):
                            self.akta_dik['{:03d}'.format(idx)]= {}
                            self.akta_dik['{:03d}'.format(idx)]['name']=col_name.replace(' ','_')
                            self.akta_dik['{:03d}'.format(idx)]['mu']= col_um[idx]
                            self.akta_dik['{:03d}'.format(idx)]['data']=[]
                        data_rows = 0

                    elif line_count == 2:
                        header = row[0]
                        if header == 'Frequency':
                            for i in range (1,len(row)-1,1):
                                try:
                                    freq= float(row[i])*1000
                                except:
                                    continue
                            bt = 1/freq
                            self.akta_dik['f']= freq


                    elif line_count> 2:
                        # print(f'Values number  are {", ".join(row)}')

                        data_rows +=1
                        for idx,col_data in enumerate(row):
                            if idx == 0:
                                self.akta_dik['{:03d}'.format(idx)]['data'].append(float((int(col_data)-1)*bt))
                            else:
                                self.akta_dik['{:03d}'.format(idx)]['data'].append(float(col_data))
                    line_count +=1
            print(f'Processed {line_count} lines.')

            with open(self.akta_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.akta_dik,pickle_file,protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.akta_pickle_filepath,mode='rb') as pickle_file:
                self.akta_dik = pickle.load(pickle_file)

        return self.akta_dik

