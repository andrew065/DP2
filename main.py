from load_cell_library import Load_Cell_Sensor

#Objective 2c: Python Program

#constant global variables

#Gravitational Constant
g = 9.81
#assigned patient data
age = 51
mass = 111
#Femoral Bone Morphology
dia_o = 
dia_i = 
fem_offset = 
#Implant Design Parameters
dia_s = 
E_s = 

#load cell data
sensor_val = 
mths_postop =

#initialize sensor
load_sensor = Load_Cell_Sensor()
load_sensor.begin()
load_sensor.zero_offset(fem_offset)
load_sensor.set_calibration_factor(None)


def read_load():
    weight = load_sensor.get_virtual_weight(10, 1)
