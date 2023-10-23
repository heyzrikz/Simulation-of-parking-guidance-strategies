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
    file = minidom.parse("parking.add.xml")
    trip = file.getElementsByTagName('parkingArea')
    for data in trip:
        val = data.attributes[(str)("lane")].value
        data.attributes["lane"].value = val+"_0"
    print(file.toxml())
    with open("parking.add.xml","w") as f:
     file.writexml(f)
        #temporarylocation = etree.Element("param")
        #temporarylocation.set('key','parking.absfreespace.weight')
        #temporarylocation.set('value','100000000')
        #data.insert(1,temporarylocation)
    #file.write("trips.trips.parking.xml",etree.dump(file))
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()