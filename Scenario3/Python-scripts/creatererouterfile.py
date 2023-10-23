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
    file = minidom.parse("disParking.xml")
    trip = file.getElementsByTagName('parkingArea')
    dest = etree.parse('rerouter.xml')
    i=0
    for i in range(45):
        wl=""
        for data in trip:
            district = data.attributes[(str)("district")].value
            nome = data.attributes[(str)("edge")].value
            if (str)(i) == district:
                wl=wl+" "+nome
        for ret in dest.findall("additional"):
            temporarylocation = etree.Element("rerouter")    
            temporarylocation.set('id',(str)(i))
            temporarylocation.set('edges',(str)(wl))
            ret.insert(1,temporarylocation)
            indent(ret)
        dest.write("rerouter.xml",etree.dump(dest))
    
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()