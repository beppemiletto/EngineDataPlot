import csv
import os
import sys
import pickle

class Rasp_Data():
    def __init__(self, data_path=None, rasp_filename=None):
        if data_path is not None:
            self.data_path = data_path
        else:
            return 1

        if rasp_filename is not None:
            self.rasp_filename = rasp_filename
        else:
            return 2



# data_path = "D:\Application_data\Report_C13\HDS9"
# rasp_filename = "MDS_test_ESC_20190308_ASCII.csv"

        self.rasp_filepath = os.path.join(self.data_path, self.rasp_filename)

        self.rasp_pickle_filename = self.rasp_filename.split('.')[0] + '.pickle'
        self.rasp_pickle_filepath = os.path.join(self.data_path,self.rasp_pickle_filename)

        self.rasp_dik = {}

    def load_data(self):
        if not os.path.exists(os.path.join(self.data_path, self.rasp_filename)):
            return None
        try:
            s = os.stat(self.rasp_pickle_filepath)
            if s.st_size == 0:
                print ( "The file {} is empty. Removing the 0 byte file and proceeding with data import. Wait! It can require long times!".format(self.rasp_pickle_filepath))
                os.remove(self.rasp_pickle_filepath)
        except OSError as e:
            print("Pickle file {} doesn't exist. Proceeding with data import. Wait! It can require long times!".format(self.rasp_pickle_filepath))
        if not os.path.exists(self.rasp_pickle_filepath):
            with open(self.rasp_filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter =',', )
                line_count = 0
                try:
                    for row in csv_reader:
                        if line_count== 0:
                            col_names= row
                            # print(f'Column names are {", ".join(row)}')
                            # print(f'Column meas units are {", ".join(row)}')
                            col_um = row

                            for idx,col_name in enumerate(col_names):
                                self.rasp_dik['{:03d}'.format(idx)]= {}
                                self.rasp_dik['{:03d}'.format(idx)]['name']=col_name.split(' ')[0].replace('-','_').replace(')','').replace('(','_')
                                self.rasp_dik['{:03d}'.format(idx)]['mu']= col_name.split(' ')[-1].replace('[','').replace(']','')
                                self.rasp_dik['{:03d}'.format(idx)]['data']=[]
                                print(self.rasp_dik['{:03d}'.format(idx)])
                            data_rows = 0
                        elif line_count>= 1:
                            # print(f'Values number  are {", ".join(row)}')

                            data_rows +=1
                            for idx,col_data in enumerate(row):
                                try:
                                    self.rasp_dik['{:03d}'.format(idx)]['data'].append(float(col_data))
                                except:

                                    if idx  < len(col_names):
                                        self.rasp_dik['{:03d}'.format(idx)]['data'].append(0.0)
                                    else:
                                        break
                            print("Data row = {}\r".format(data_rows),end='',flush=True)
                        line_count +=1
                except:
                    csv_file.close()



            print(f'Processed {line_count} lines.')

            print("\nChecking the UNIX timestamp integrity")
            tgap = 0.0
            t_old = 0.0
            for idx,t in enumerate(self.rasp_dik['000']['data']):
                if idx > 0:
                    dt=t-t_old
                    if dt > 30.0:
                        tgap +=(dt-1.0)
                        print("found a gap of {} for a total t gap {} ".format(dt-1.0,tgap))
                    tnew= t-tgap
                    self.rasp_dik['000']['data'][idx] = tnew
                    t_old = t
                else:
                    t_old=t



            with open(self.rasp_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.rasp_dik,pickle_file,protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.rasp_pickle_filepath,mode='rb') as pickle_file:
                self.rasp_dik = pickle.load(pickle_file)

        return self.rasp_dik

