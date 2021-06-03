import csv
import os
import sys
import pickle

base_time = 100

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
                        self.bosmal_dik['{:03d}'.format(0)]= {}
                        self.bosmal_dik['{:03d}'.format(0)]['name'] = 'recorder_time'
                        self.bosmal_dik['{:03d}'.format(0)]['mu'] = 's'
                        self.bosmal_dik['{:03d}'.format(0)]['data'] = []
                        buffer_recovery_data.append(0)
                        for idx,col_name in enumerate(col_names):
                            self.bosmal_dik['{:03d}'.format(idx+1)]= {}
                            self.bosmal_dik['{:03d}'.format(idx+1)]['name']=col_name.replace(' ','_').replace('§','').split('.')[-1]
                            self.bosmal_dik['{:03d}'.format(idx+1)]['mu']= col_um[idx]
                            self.bosmal_dik['{:03d}'.format(idx+1)]['data']=[]
                            buffer_recovery_data.append(0)
                        data_rows = 0
                    elif line_count> 1:

                        # print(f'Values conf  are {", ".join(row)}')

                        self.bosmal_dik['{:03d}'.format(0)]['data'].append(data_rows*base_time)
                        data_rows +=1

                        for idx,col_data in enumerate(row):
                            if col_data == '':
                                col_data = buffer_recovery_data[idx+1]
                            try:
                                self.bosmal_dik['{:03d}'.format(idx+1)]['data'].append(float(col_data))
                            except:
                                if idx+1  < len(col_names):
                                    self.bosmal_dik['{:03d}'.format(idx+1)]['data'].append(col_data)
                                else:
                                    break
                            buffer_recovery_data[idx+1]=col_data
                    line_count +=1
            print(f'Processed {line_count} lines.')

            with open(self.bosmal_pickle_filepath,mode='wb') as pickle_file:
                pickle.dump(self.bosmal_dik,pickle_file,protocol= pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.bosmal_pickle_filepath,mode='rb') as pickle_file:
                self.bosmal_dik = pickle.load(pickle_file)

        return self.bosmal_dik

    def peak_locator(self, sig_edges_threshold, time,  signal, peak_number = 1 , denoise_samples = 5):
        self.time = time
        self.signal = signal
        self.sig_edges_threshold = sig_edges_threshold
        self.peak_number = peak_number
        self.denoise_samples = denoise_samples

        self.peak_time = 0
        self.peak_value = self.sig_edges_threshold
        self.peak_count = 0
        idx = 0
        done = False
        while not done:
            if self.signal[idx] >= self.sig_edges_threshold:
                if self.signal[idx+self.denoise_samples] >= self.sig_edges_threshold:
                    idx += self.denoise_samples
                    self.peak_count += 1
                    self.peak_time = self.time[idx]
                    self.peak_value = self.signal[idx]
                    done = False
                    while not done:
                        idx += 1
                        if self.signal[idx]>= self.peak_value:
                            self.peak_time = self.time[idx]
                            self.peak_value = self.signal[idx]
                        elif self.signal[idx] <= self.sig_edges_threshold:
                            if self.peak_count >= self.peak_number:
                                return [self.peak_time, self.peak_value]
                            else:
                                done = True
                        else:
                            continue

                else:
                    continue

            else:
                idx += 1
                if idx == len(self.signal):
                    return [0,0]

    def emx_analysers_delays_compensation(self,signal, delay, timebase = 0.1):
        done = False
        idx = 0
        self.modified_signal = signal
        self.gap_sample_n = int(abs(delay) / timebase)
        while not done:
            if idx < self.gap_sample_n:
                pass
            elif idx >= len(signal) - self.gap_sample_n:
                done = True
            else:
                self.modified_signal[idx-self.gap_sample_n]=signal[idx]

            idx += 1

        return(self.modified_signal)
