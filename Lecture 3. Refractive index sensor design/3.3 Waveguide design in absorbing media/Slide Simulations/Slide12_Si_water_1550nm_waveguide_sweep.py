# -*- coding: utf-8 -*-
"""

"""
#%% Initialize
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import scipy.constants as const
import imp

#import os, get script directory, import color plot directory, etc.
import sys
import os

#define function that makes new folder to store output
def create_output_directory(output_subfolder = 'Output'):
    dir_script = os.getcwd()

    dir_output = os.path.join(dir_script, output_subfolder)
    
    if not os.path.exists(dir_output):
        os.mkdir(dir_output)
     
    return dir_output

load_file = "Slide12_waveguide_Si_water_1550nm" #lumerical filename without .lms or .fsp part!
output_subfolder =  "output" #output folder name
dir_output = create_output_directory(output_subfolder) #creat output folder

#import plotly and set settings to display figures in spyder
#import plotly.express as px
#import plotly.io as pio
#pio.renderers.default='svg'


#%% open Lumerical
#set-up lumerical
lumapi = imp.load_source("lumapi", "C:\\Program Files\\Lumerical\\v211\\api\\python\\lumapi.py") # load Lumerical API
mode = lumapi.MODE() #open file
mode.load(load_file + ".lms")


#%% set parameters
wavelength= 1550e-9 #wavelength in nm
n_modes = 6 #number of modes to solve for

w_min =0.3 #min waveguide difference
w_max = 1.0 #max waveguide difference
step_size = 0.01 #step_size
num = int((w_max-w_min)/step_size + 1) #number of steps
w = np.linspace(w_max, w_min, num) #array with different dw's
w = w*1e-6 #um

#create empty arrays to collect sweep data
n_TE0 = np.array([])
n_TM0 = np.array([])
n_TE1 = np.array([])
n_TM1 = np.array([])
for i in range(0,num): #set to num for sweep
    # mode.save(os.path.join(dir_output, load_file+"_"+str(round(w[i]*1e9))+"nm.lms")) #save file under new name

    mode.switchtolayout()
    
    mode.select("Si")
    mode.set("x span", w[i])
    
    mode.select("mesh")
    mode.set("x span", w[i]+0.2e-6)
    
    mode.select("SiO2")
    mode.set("y max", 0)
    
    mode.run()
    
    #Set parameters mode solver
    mode.setanalysis("wavelength", wavelength)
    mode.setanalysis("number of trial modes", n_modes)
    mode.setanalysis("search", "near n")
    mode.setanalysis("use max index", 1)

    #Modal analysis
    mode.findmodes(); #find modes
    
    n1 = mode.getdata("FDE::data::mode1","neff")
    n1 = np.squeeze(n1)
    n1 = np.real(n1)
    n2 = mode.getdata("FDE::data::mode2","neff")
    n2 = np.squeeze(n2)
    n2 = np.real(n2)
    n3 = mode.getdata("FDE::data::mode3","neff")
    n3 = np.squeeze(n3)
    n3 = np.real(n3)
    n4 = mode.getdata("FDE::data::mode4","neff")
    n4 = np.squeeze(n4)
    n4 = np.real(n4)
    
    #save data to array
    n_TE0 = np.append(n_TE0,n1)
    n_TM0 = np.append(n_TM0,n2)
    n_TE1 = np.append(n_TE1,n3)
    n_TM1 = np.append(n_TM1,n4)

    
    # mode.save(os.path.join(dir_output, load_file+str(round(dw[i]*1e9))+".lms")) #save file
    
#%%    
# save and plot data
df=pd.DataFrame()
df["w"]=w*1e9
df["n_TE0"]=n_TE0
df["n_TM0"]=n_TM0
df["n_TE1"]=n_TE1
df["n_TM1"]=n_TM1


df.to_excel(os.path.join(dir_output, load_file+"Si_water_1550_neff.xlsx"), na_rep='', columns=df.columns, header=True, index=False)
#%%
#p2 = px.line(df,x='w', y=df.columns[1:3])
#p2.write_image(os.path.join(dir_output, load_file+"_neff_1550nm.png"))
#p2.show()

