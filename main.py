from matplotlib import pyplot as plt
from load_cell_library import Load_Cell_Sensor
import time
import math
#from gpiozero import LED


#calculating resultant tensile stress of implant stem and bone:
def applied_load(s_val):
    n = s_val*3/10   #number of 10g weights TODO: remove theoretical load being placed (3 plates)
    load = mass*n*g  #force on femoral head
    return round(load, 1)


#calculating elastic modulus of bone
def em_b(a):
    modulus_b = -0.123 * (a - 40) + 17
    return round(modulus_b, 1) #TODO: double check rounding


def result_tens_stress_b(load, e_b):
    #properties of bone
    bone_area = (math.pi/4)*(dia_o**2-dia_i**2) # A
    moment_of_inertia_bone = (math.pi/64)*(dia_o**4-dia_i**4) # I

    #calculating tensile stress on bone 
    axial_stress_bone = -load / bone_area
    bending_stress_bone = (load * fem_offset * dia_o / 2) / moment_of_inertia_bone

    tensile_stress_bone = axial_stress_bone + bending_stress_bone

    #calculating resultant stress on bone
    resultant_stress_bone = tensile_stress_bone * ((3 * e_b) / (e_b + E_s)) ** (1 / 4)

    return round(resultant_stress_bone, 1) 


def result_tens_stress_s(load, e_b):
    #properties of stem
    stem_area = (math.pi/4)*(dia_s**2)
    moment_of_inertia_stem = (math.pi/64)*(dia_s**4)
    
    #calculating tensile stress on stem
    axial_stress_stem = -load / stem_area
    bending_stress_stem = (load * fem_offset * (dia_s / 2)) / moment_of_inertia_stem #(half stem diameter is neutral axis distance)

    tensile_stress_stem = axial_stress_stem + bending_stress_stem
    
    #resultant stress of stem
    resultant_stress_stem = tensile_stress_stem * (1 - (3 * e_b / (e_b + E_s))) ** 1 / 4

    return round(resultant_stress_stem, 1)


def uts(mths, e_implant, e_bone):
    e_ratio = math.sqrt(e_implant/e_bone)
    tensile_strength = 175/(1+0.05*math.e**(0.06*(mths/12)*e_ratio))

    return round(tensile_strength, 1)


def plot_chart(t_post_op, r_stress, ultimate_strength):
    fig, axes = plt.subplots(figsize=(8, 4))

    axes.plot(t_post_op, ultimate_strength, label='Ultimate tensile strength in bone (UTSb)')
    axes.plot(t_post_op, r_stress, label='Resultant tensile stress in bone (σ resb)')

    axes.set(xlabel='Time (Years Post-Surgery)', ylabel='Stress (MPa)')
    axes.legend(loc='upper right')

    plt.title('Stress vs Time Post Surgery')
    plt.minorticks_on()
    plt.grid(which='both', axis='both')
    plt.show()


def read_load():
    global sensor_val, mths_postop #updates global variables

    print('\t'.join(key for key in ['mths', 'applied load', 'Res. stress, bone', 'Res. stress, stem', 'E, bone', 'UTS, bone']))


    while True:
        sensor_val = load_sensor.get_virtual_weight(10, 1) #TODO: update to check from actual sensor
        load = applied_load(sensor_val)
        # sensor_val = load_sensor.get_weight()

        if sensor_val > 0:
            mths_postop += 1
            e_b = em_b(age + mths_postop/12)

            dataset[0].append(round(mths_postop, 1))
            dataset[1].append(load)
            dataset[2].append(result_tens_stress_b(load, e_b))
            dataset[3].append(result_tens_stress_s(load, e_b))
            dataset[4].append(e_b)
            dataset[5].append(uts(mths_postop/12, E_s, e_b))

            print('\t\t\t'.join(map(str, [*map(lambda data: data[-1], dataset)])))
        
        #LED outputs

        #if datset[2] < 0.1 * dataset[5]:
            #green_led.on()
            #yellow_led.off()
            #red_led.off()

        #if datset[2] >= 0.1 * dataset[5] and dataset[2] < 0.5 * dataset[5]:
            #green_led.off()
            #yellow_led.on()
            #red_led.off()

        #elif datset[2] >= 0.5 * dataset[5] and dataset[2] < dataset[5]:
            #green_led.off()
            #yellow_led.off()
            #red_led.on()

        #else:     #if resultant stress of bone is >= to UTS
            #red_led.blink(0.5,0.5)
            #green_led.off()
            #yellow_led.off()



        if len(dataset[0]) == 360:
            plot_chart(dataset[0], dataset[2], dataset[5])
            break

        time.sleep(0)

#defining variables:

#Gravitational Constant
g = 9.81
#assigned patient data
age = 51 #(years)
mass = 111 #(kg)
s = 'male'
#Femoral Bone Morphology
dia_o = 33 #(mm)
dia_i = 19 #(mm)
fem_offset = 47

#Implant Design Parameters TODO: insert actual values
dia_s = 33
E_s = 105

#load cell data
sensor_val = 0
mths_postop = 0

dataset = [[], [], [], [], [], []]

#initialize sensor
load_sensor = Load_Cell_Sensor()
#load_sensor.begin()
#load_sensor.zero_offset(fem_offset)
#load_sensor.set_calibration_factor(None)

#setting LED pins of each colour
#green_led = LED()
#yellow_led = LED()
#red_led = LED()


read_load()




