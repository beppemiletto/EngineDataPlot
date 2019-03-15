import numpy as np
import sys
import os

class ESC_Detect():
    def __init__(self, rpm = None, load = None, time=None, engine_speeds = None, loads = None,  tolerance = None):
        self.rpm = rpm
        self.load = load
        self.t = time
        self.engine_speeds = engine_speeds
        self.loads = loads
        self.tolerance = tolerance

        if len(self.rpm) < 50 or len(self.load) < 50 or len(self.t) < 50:
            return -1

        # if not specified the default values of engine speed are assigned
        if self.engine_speeds == None:
            self.engine_speeds = [650,1250, 1500, 1750]

        if self.loads == None:
            self.loads = [500,1000,1500,2000]

        if self.tolerance == None:
            self.tolerance = 0.1           # set default 10% tolerance

        self.rpm_bounds = []
        for idx, rpm_bound in enumerate(self.engine_speeds):
            self.rpm_bounds.append((rpm_bound*(1-self.tolerance),rpm_bound*(1+self.tolerance)))
        self.load_bounds = []
        for idx, load_bound in enumerate(self.loads):
            self.load_bounds.append((load_bound*(1-self.tolerance),load_bound*(1+self.tolerance)))

    # Detect the subcycle of eventually repeating ESC
    def detect_subcycles(self):
        # looking for beginning checking idle before first acceleration
        esc_seq = []
        mode = 0
        esc_num = 0
        sample = 0
        trigger = False
        esc_complete = False
        for idx, ti  in enumerate(self.t):
            if mode == 0:
                if self.rpm[idx] < self.rpm_bounds[1][0]:
                    if sample == 0:
                        t0 = ti
                    sample += 1
                    trigger = True
                elif self.rpm[idx] > self.rpm_bounds[1][0] and trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue
            elif mode == 1 :
                if self.rpm[idx] >= self.rpm_bounds[1][0] and self.rpm[idx] <= self.rpm_bounds[2][0] and self.load[idx] > self.load_bounds[3][0] and self.load[idx] < self.load_bounds[3][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 2 :
                if self.rpm[idx] >= self.rpm_bounds[1][1] and self.rpm[idx] <= self.rpm_bounds[2][1] and self.load[idx] > self.load_bounds[1][0] and self.load[idx] < self.load_bounds[1][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 3 :
                if self.rpm[idx] >= self.rpm_bounds[1][1] and self.rpm[idx] <= self.rpm_bounds[2][1] and self.load[idx] > self.load_bounds[2][0] and self.load[idx] < self.load_bounds[2][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 4 :
                if self.rpm[idx] >= self.rpm_bounds[1][0] and self.rpm[idx] <= self.rpm_bounds[1][1] and self.load[idx] > self.load_bounds[1][0] and self.load[idx] < self.load_bounds[1][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 5 :
                if self.rpm[idx] >= self.rpm_bounds[1][0] and self.rpm[idx] <= self.rpm_bounds[1][1] and self.load[idx] > self.load_bounds[2][0] and self.load[idx] < self.load_bounds[2][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 6 :
                if self.rpm[idx] >= self.rpm_bounds[1][0] and self.rpm[idx] <= self.rpm_bounds[1][1] and self.load[idx] > self.load_bounds[0][0] and self.load[idx] < self.load_bounds[0][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 7 :
                if self.rpm[idx] >= self.rpm_bounds[2][0] and self.rpm[idx] <= self.rpm_bounds[2][1] and self.load[idx] > self.load_bounds[3][0] and self.load[idx] < self.load_bounds[3][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 8 :
                if self.rpm[idx] >= self.rpm_bounds[2][0] and self.rpm[idx] <= self.rpm_bounds[2][1] and self.load[idx] > self.load_bounds[0][0] and self.load[idx] < self.load_bounds[0][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 9 :
                if self.rpm[idx] >= self.rpm_bounds[3][0] and self.rpm[idx] <= self.rpm_bounds[3][1] and self.load[idx] > self.load_bounds[3][0] and self.load[idx] < self.load_bounds[3][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 10 :
                if self.rpm[idx] >= self.rpm_bounds[3][0] and self.rpm[idx] <= self.rpm_bounds[3][1] and self.load[idx] > self.load_bounds[0][0] and self.load[idx] < self.load_bounds[0][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 11 :
                if self.rpm[idx] >= self.rpm_bounds[3][0] and self.rpm[idx] <= self.rpm_bounds[3][1] and self.load[idx] > self.load_bounds[2][0] and self.load[idx] < self.load_bounds[2][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 12 :
                if self.rpm[idx] >= self.rpm_bounds[3][0] and self.rpm[idx] <= self.rpm_bounds[3][1] and self.load[idx] > self.load_bounds[1][0] and self.load[idx] < self.load_bounds[1][1]:
                    sample += 1
                    trigger = True
                elif trigger :
                    esc_start = t0
                    mode += 1
                    sample = 0
                    trigger = False
                else:
                    continue

            elif mode == 13:
                esc_seq.append((t0,ti))
                mode = 0
                trigger = False
                sample = 0
                esc_num += 1

        return esc_seq
