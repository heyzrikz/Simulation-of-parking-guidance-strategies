#!/usr/bin/env python
# File: traci.py
#from distutils.filelist import findall
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
    file = minidom.parse("appoggio.xml")
    trip = file.getElementsByTagName('rerouter')
    f = etree.parse('trips.trips.xml')
    for data in trip:
        val = data.attributes[(str)("edges")].value
        for d in f.findall('trip'):
            val = val+" "+ d.get('to')
        data.attributes["edges"].value = val
    #print(file.toxml())
    with open("appoggio.xml","w") as fi:
     file.writexml(fi)
        #temporarylocation = etree.Element("param")
        #temporarylocation.set('key','parking.absfreespace.weight')
        #temporarylocation.set('value','100000000')
        #data.insert(1,temporarylocation)
    #file.write("trips.trips.parking.xml",etree.dump(file))
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()