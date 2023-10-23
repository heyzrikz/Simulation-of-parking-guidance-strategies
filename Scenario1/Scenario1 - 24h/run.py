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

def getEdgeDistrict(file_name,edge):
    file = minidom.parse(file_name)
    taz = file.getElementsByTagName('taz')
    for data in taz:
        id = data.attributes[(str)("id")].value
        edges = data.attributes[(str)("edges")].value
        if edge in edges:
            return id
    return "0"

def getParkingDistrict(file_name,parking):
    file = minidom.parse(file_name)
    parkingArea = file.getElementsByTagName('parkingArea')
    for data in parkingArea:
        id = data.attributes[(str)("id")].value
        district = data.attributes[(str)("district")].value
        if parking == id:
            return district
    return "0"


def existsDetector(file_name,id):
    file = minidom.parse(file_name)
    inductionLoop = file.getElementsByTagName('inductionLoop')
    for data in inductionLoop:
        detector = data.attributes[(str)("id")].value
        if detector == id:
            return 0
    return 1    

def createParkingMap(file_name):
    parking = my_map()
    file = minidom.parse(file_name)
    parkingArea = file.getElementsByTagName('parkingArea')
    for data in parkingArea:
        detector = data.attributes[(str)("id")].value
        parking.add(detector,getParkingDistrict("districts.taz.xml",detector)) #0=distretto
    return parking

def createEdgesMap(file_name):
    edges = my_map()
    file = minidom.parse(file_name)
    parkingArea = file.getElementsByTagName('edge')
    i=2241
    for data in parkingArea:
        i=i-1
        detector = data.attributes[(str)("id")].value
        #if existsDetector("detectors.add.xml",detector) == 0:
        edges.add(detector,getEdgeDistrict("districts.taz.xml",detector)) #0=distretto
        print((str)(i)+" s")
    return edges


class my_map(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

        
#contains TraCI control loop
def run():
    
    
    #VARIABILI GLOBALI
    step = 0
    veicoli_cerca = my_map() # map: id veicolo - cerca parcheggio (true,false)
    veicoli_destinazione = my_map() # map: id veicolo - edge di destinazione
    all_parking = createParkingMap("parking.add.xml") # map: id parcheggio con detector - distretto
    print("Caricamento dei dati mancano:")
    all_edges = createEdgesMap("san_francisco.net.xml") # map: edge con detector - distretto
    print("create edges V")
    all_edges_keys = list(all_edges.keys()) # list: edge con detector

    #INIZIO SIMULAZIONE
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
        print(step)

        #Aggiungiamo tutti i veicoli generati in quello step alle mappe dei veicoli
        for id in traci.simulation.getDepartedIDList():
            veicoli_cerca.add(id,'true')
            routes = traci.vehicle.getRoute(id)
            veicoli_destinazione.add(id,routes[len(routes) - 1])

        #Reroting dei parcheggi    
        for parking in all_parking.keys():
            det_vehs = traci.inductionloop.getLastStepVehicleIDs(parking)
            for veh in det_vehs:
                if veicoli_cerca.get(veh)=='true' and getEdgeDistrict("districts.taz.xml",veicoli_destinazione.get(veh)) == getParkingDistrict("disParking.xml",parking):
                    if (int)(traci.simulation.getParameter(parking,'parkingArea.capacity')) - (int)(traci.simulation.getParameter(parking,'parkingArea.occupancy')) > 0:
                        traci.vehicle.setParkingAreaStop(veh,parking,100,0,1)
                        veicoli_cerca.add(veh,'false')
                        traci.vehicle.changeTarget(veh,veicoli_destinazione.get(veh))
                    else: 
                        if veicoli_cerca.get(veh)=='false' and getEdgeDistrict("districts.taz.xml",veicoli_destinazione.get(veh)) == getParkingDistrict("districts.taz.xml",parking):
                            seed(step)
                            index = randint(0,7)
                            while all_edges_keys[index]+'_0' == traci.simulation.getParameter(parking,'parkingArea.lane') or getEdgeDistrict("districts.taz.xml",veicoli_destinazione.get(veh)) != all_edges.get(all_edges_keys[index]):
                                index = randint(0,7)
                            print("nuova des per veicolo n."+veh+": "+all_edges_keys[index])
                            traci.vehicle.changeTarget(veh,all_edges_keys[index])
                            print("va avanti")
        
        #Rerouting delle edges
        #for edge in all_edges_keys:
         #   det_vehs = traci.inductionloop.getLastStepVehicleIDs(edge)
          #  for veh in det_vehs:
           #     if veicoli_cerca.get(veh)=='true' and getEdgeDistrict("districts.taz.xml",veicoli_destinazione.get(veh)) == getEdgeDistrict("districts.taz.xml",edge):
            #        seed(step)
             #       index = randint(0,7)
              #      print("index: "+(str)(index))
               #     while all_edges_keys[index] == edge or len(traci.simulation.findRoute(edge,all_edges_keys[index],"DEFAULT_VEHTYPE",-1,0).edges) == 0 or getEdgeDistrict("districts.taz.xml",veicoli_destinazione.get(veh)) != all_edges.get(all_edges_keys[index]):
                #            index = randint(0,7)
                 #   traci.vehicle.changeTarget(veh,all_edges_keys[index])
                  #  print("nuova des per veicolo n."+veh+": "+all_edges_keys[index]+" index: "+(str)(index))
                    

       

        
        
        

    traci.close()
    print("end")
    print(veicoli_cerca)
    print(veicoli_destinazione)
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