#!/usr/bin/env python
# File: traci.py
from logging import root
import os
import sys
import optparse
from tracemalloc import stop
from xml.dom import minidom
import xml.etree.cElementTree as et
import csv
import pandas as pd
import plotly.express as px
from random import seed
from random import randint
import time

from numpy import double

#we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare enviroment variable 'SUMO_HOME' ")


from sumolib import checkBinary #checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                        default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options





        
#contains TraCI control loop
def run():
    
    
    #VARIABILI GLOBALI
    step = 0
    

    #INIZIO SIMULAZIONE
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
        print(step)

    traci.close()
    print("end")
    sys.stdout.flush()


    
   
        
        

#main entry point
if __name__ == "__main__":
    options = get_options()

    #check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c","san_francisco.sumo.cfg",
                            ])
    run()