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
    file = etree.parse("reroute_parking.xml")
    f = minidom.parse("parking.add.xml")
    trip = f.getElementsByTagName('parkingArea')
    for data in trip:
        #print(data.attributes[(str)("id")].value)
        for d in file.findall('interval'):
            #print(data.attributes[(str)("id")].value)
            temporarylocation = etree.Element("parkingAreaReroute")
            temporarylocation.set('id',data.attributes[(str)("id")].value)
            temporarylocation.set('visible','false')
            temporarylocation.set('probability','0.5')
            d.insert(1,temporarylocation)
        indent(d)
    file.write("reroute_parking.xml",etree.dump(file))
           
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()