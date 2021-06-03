#!/usr/local/bin/python
import sys
import os
import numpy as np


# Distribution2D - make the distribution of y against x
class Distribution2D():
    def __init__(self, x=None, y=None, x_bounds=None, y_bounds=None, mode=None):
        if x:
            self.x = np.array(x)
        else:
            return

        if y:
            self.y = np.array(y)
        else:
            return


        # x parameter have priority on the alignment in case the two vector are not same

        if x_bounds:
            try:
                if len(x_bounds) > 1:
                    self.x_bounds = x_bounds
                    self.x_num_class = len(self.x_bounds) - 1
            except:
                self.x_num_class = x_bounds
                interval = (np.max(self.x) - np.min(self.x)) / (self.x_num_class - 1)
                self.x_bounds = []
                for idx in range(self.x_num_class):
                    if idx == 0:
                        self.x_bounds.append(np.min(self.x))
                    elif idx == self.x_num_class - 1:
                        self.x_bounds.append(np.max(self.x))
                    else:
                        self.x_bounds.append(np.min(self.x) + idx * interval)

        if y_bounds:
            try:
                if len(y_bounds) > 1:
                    self.y_bounds = y_bounds
                    self.y_num_class = len(self.y_bounds) - 1
            except:
                self.y_num_class = y_bounds
                interval = (np.max(self.y) - np.min(self.y)) / (self.y_num_class - 1)
                self.y_bounds = []
                for idy in range(self.y_num_class):
                    if idy == 0:
                        self.y_bounds.append(np.min(self.y))
                    elif idy == self.y_num_class - 1:
                        self.y_bounds.append(np.max(self.y))
                    else:
                        self.y_bounds.append(np.min(self.y) + idy * interval)

            pass
        else:
            if isinstance(y_bounds, int):
                pass

    def dist_abs(self):
        for :