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
    fi = minidom.parse("reroute_parking.xml")
    tri = fi.getElementsByTagName('parkingAreaReroute')
    f = etree.parse("temptrip.xml")
    l=[]
    for data in trip:
        val = (data.attributes[(str)("id")].value)
        l.append(val)
    for d in f.findall('stop'):
        to = d.get("parkingArea")
        if to in l:
            l.remove(to)
    for data in trip:
        v = (data.attributes[(str)("id")].value)
        for i in l:
            if v==i:
                 newval = "0"
                 data.attributes["id"].value = (str)(newval)
    with open("parking.add.xml","w") as f:
     file.writexml(f)
    for data in tri:
        v = (data.attributes[(str)("id")].value)
        for i in l:
            if v==i:
                 newval = "0"
                 data.attributes["id"].value = (str)(newval)
    with open("reroute_parking.xml","w") as f:
     fi.writexml(f)
                   #  with open("parking.add.xml","w") as f:
     #file.writexml(f)
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()