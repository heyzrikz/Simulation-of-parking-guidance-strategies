#!/usr/bin/env python
# File: traci.py
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
    file = minidom.parse("distmp.taz.xml")
    trip = file.getElementsByTagName('taz')
    id = 0
    for data in trip:
        val = data.attributes[(str)("edges")].value
        parking_file = etree.parse("parking.add.xml")
        for data_parking in parking_file.findall('additional'):
            temporarylocation = etree.Element("parkingArea")
            temporarylocation.set('id','fakeparking_'+(str)(id))
            temporarylocation.set('lane',val)
            temporarylocation.set('roadsideCapacity','0')
            temporarylocation.set('startPos','0')
            temporarylocation.set('endPos','1')
            data_parking.insert(1,temporarylocation)
            indent(data_parking)
        id = id + 1
        parking_file.write("parking.add.xml",etree.dump(parking_file))
    
        #temporarylocation = etree.Element("param")
        #temporarylocation.set('key','parking.absfreespace.weight')
        #temporarylocation.set('value','100000000')
        #data.insert(1,temporarylocation)
    #file.write("trips.trips.parking.xml",etree.dump(file))
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()