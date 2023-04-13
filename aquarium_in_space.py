#imports
import matplotlib.pyplot as plt
from time import sleep
import math
import time

#NOTE This model assumes infinite thermal condutivity as of now 


#Gen Params
time = 0 #time var in sec
dt = 60 #simulation time step size in sec


temperature = 298 #starting temp in K also used to store the current temp
# A day consisits of 1440 time units of a min each
time_unit = 0

#material properties 
water_em = 0.96 #emissivity of water not used since the glass will absorb most of the the water emmision 
glass_em = 0.88 #emissivity of glass(clear)

#all densities in g/cm^3
water_density = 1
glass_density = 2.5 #assuems anniled clear glass
substrate_density = 1.85 #ballpark value
metal_density = 7.85 #assumes metal is steel
plastic_density = 0.95 #assuems plastic is HDPE

#all heat capacities in J*g^−1*K^−1
water_heat_cap = 4.18
glass_heat_cap = 0.84 #assuems anniled clear glass
substrate_heat_cap = 1.00 #ballpark value
metal_heat_cap = 0.46 #assumes metal is steel
plastic_heat_cap = 2.30 #assuems plastic is HDPE



#Heating/lighting regime

#Both heating and lighting are presumed to have only 2 modes | on and off

light_wattage = 200 #wattage of lighting when turned on
light_schedule = 30 #half cycle lenght in mins
light_state = False #stores if the light is on
light_efficiency = 0.2 #percentage 

heat_wattage = 240 #wattage of heating when truned on
heat_schedule = 30 #half cycle lenght in mins
heat_state =  True #stores if the heat is on
#heating system is assumed to have an efficiency of 100% ie all energy from the stated wattage is turned into heat for the system

#Hardware characteristics
liquid_volume = 20 #volume of water in l

substrate_volume = 2 #volume of substrate in l

glass_hight = 26 #in cm 
glass_width = 21 #in cm 
glass_lenght = 42 #in cm 
glass_thickness = 2 #in cm 

plastic_mass = 2 #in kg

metal_mass = 1 #in kg

#Feeding regime
#TODO Implment Nitrogen cycle



#Calculate inferred properties

#glass
def glass_area_cal(h,w,l):
    return (2*h*w)+(2*h*l)+(2*l*w)

glass_area = glass_area_cal(glass_hight,glass_width,glass_lenght)

def glass_volumne_cal(area,thickness):
    return area*thickness

glass_volume = glass_volumne_cal(glass_area,glass_thickness)

glass_mass = glass_volume*glass_density

glass_heat_cap_total = glass_mass*glass_heat_cap

#water
water_mass = liquid_volume*1000*water_density 

water_heat_cap_total = water_mass*water_heat_cap

#substrate

substrate_mass = substrate_volume*substrate_density

substrate_heat_cap_total = substrate_mass*substrate_heat_cap

#plastic
plastic_heat_cap_total = plastic_mass*plastic_heat_cap

#metal
metal_heat_cap_total = metal_mass*metal_heat_cap

#total heat cap
total_heat_cap  = glass_heat_cap_total+water_heat_cap_total+substrate_heat_cap_total+plastic_heat_cap_total+metal_heat_cap_total

def black_body(temp,area,em):
    sigma = 5.67E-8
    return (sigma*(area/10000)*em)*(temp**4)

a=0
b=0
while True:
    
    time += dt 
    time_unit += 1
    if time_unit > 1440:
        #time_unit = 0
        pass

    if time_unit % heat_schedule == 0:
        heat_state = not heat_state

    if time_unit % light_schedule == 0:
        light_state = not light_state       

    energy_delta = -black_body(temperature,glass_area,glass_em)

    if heat_state:
        energy_delta += heat_wattage

    if light_state:
        energy_delta += light_wattage*(1-light_efficiency)


    temperature += (energy_delta*dt)/total_heat_cap
    
    if a==30:
        if b==0:
            plt.scatter(time/60, temperature, color="blue")
            plt.pause(0.01)
            a=0
            b=1
            continue
            #print(heat_state,light_state)
        else:
            plt.scatter(time/60, temperature, color="red")
            plt.pause(0.01)
            a=0
            b=0
            continue
            #print(heat_state,light_state)
    a+=1






