import math
import time

from load_cell_library import Load_Cell_Sensor

def read_load():
    global sensor_val, mths_postop #updates global variables

    while True:
        sensor_val = load_sensor.get_virtual_weight(10, 1)
        mths_postop += 1

        time.sleep(0.25)

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
E_b = 17
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


#calculating resultant tensile stress of implant stem and bone:

def applied_load(n):
    n = sensor_val/10   #number of 10g weights
    applied_load = mass*n*g  #force on femoral head
    return applied_load

def result_tens_stress_b(applied_load(n)):
    #properties of bone
    bone_area = math.pi/4*(dia_o**2-dia_i**2)
    moment_of_inertia_bone = math.pi/64*(dia_o**4-dia_i**4)

    #calculating tensile stress on bone 
    axial_stress_bone = -applied_load/bone_area
    bending_stress_bone = (applied_load*fem_offset*dia_o/2)/moment_of_inertia_bone

    tensile_stress_bone = axial_stress_bone + bending_stress_bone
    
    #resultant stress of bone
    resultant_stress_bone = tensile_stress_bone*(3*E_b/(E_b + E_s))**1/4

    return resultant_stress_bone, E_b

    
def result_tens_stress_s(applied_load(n)):
    #properties of stem
    stem_area = math.pi/4*dia_s**2
    moment_of_inertia_stem = math.pi/64*dia_s**4
    
    #calculating tensile stress on stem
    axial_stress_stem = -applied_load/stem_area
    bending_stress_stem = (applied_load*fem_offset*(dia_s/2)/2)/moment_of_inertia_stem #(half stem diameter is neutral axis distance)

    tensile_stress_stem = axial_stress_stem + bending_stress_stem
    
    #resultant stress of stem
    resultant_stress_stem = tensile_stress_stem*(1-(3*E_b/(E_b + E_s)))**1/4

    return resultant_stress_stem




