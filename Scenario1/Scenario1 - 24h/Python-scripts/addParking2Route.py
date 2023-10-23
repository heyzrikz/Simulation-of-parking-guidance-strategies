#!/usr/bin/env python
# File_trip: traci.py
from logging import root
import os
import sys
import optparse
from tracemalloc import stop
from xml.dom import minidom
import xml.etree.cElementTree as etree
import csv
import pandas as pd
import plotly.express as px
from random import seed
from random import randint

from numpy import double

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def run():
    seed(1)
    file_trip = etree.parse("trip.add.xml")
    file_parking = minidom.parse("parking.add.xml")
    file_dis = minidom.parse("districts.taz.xml")
    parkingArea = file_parking.getElementsByTagName('parkingArea')
    taz = file_dis.getElementsByTagName("taz")
    for data in file_trip.findall('trip'):
        rand = randint(0,10)
        if rand < 5 :
            to = data.get("to")
            temporarylocation = etree.Element("stop")
            temporarylocation.set('duration','7200')
            temporarylocation.set('key','parking.probability.weight')
            for d in taz:
                list_edges = d.attributes[(str)("edges")].value
                if to in list_edges :
                    ret = d.attributes[(str)("id")].value
                    temporarylocation.set('parkingArea',"fakeparking_"+ret)
                    break
            data.insert(1,temporarylocation)
            indent(data)
    file_trip.write("trips.trips.xml",etree.dump(file_trip))
           
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()