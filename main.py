import time
from pickle import GLOBAL

from load_cell_library import Load_Cell_Sensor

#Objective 2c: Python Program

#defining variables:

#Gravitational Constant
g = 9.81
#assigned patient data
age = 51 #(years)
mass = 111 #(kg)
#Femoral Bone Morphology
dia_o = 33 #(mm)
dia_i = 19 #(mm)
fem_offset = 47
#Implant Design Parameters
dia_s =  
E_s =

#load cell data
sensor_val = 0
mths_postop = 0

#initialize sensor
load_sensor = Load_Cell_Sensor()
load_sensor.begin()
load_sensor.zero_offset(fem_offset)
load_sensor.set_calibration_factor(None)


def read_load():
    



    global sensor_val, mths_postop #updates global variables

    while True:
        sensor_val = load_sensor.get_virtual_weight(10, 1)
        mths_postop += 1

        time.sleep(0.25)


#calculating resultant tensile stress of implant stem
n = sensor_val/10   #number of 10g weights
applied_load = mass*n*g  #force on femoral head