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
    file = minidom.parse("districts.taz.xml")
    trip = file.getElementsByTagName('taz')
    f = minidom.parse("parking.add.xml")
    t = f.getElementsByTagName('parkingArea')
    dest = etree.parse('disParking.xml')
    for data in trip:
        val = data.attributes[(str)("edges")].value
        nome = data.attributes[(str)("id")].value
        wl = val.split()
        for d in t:
            string = d.attributes[(str)("lane")].value
            n = d.attributes[(str)("id")].value
            if string[0:-2] in wl:
                #print(n+" in edge "+string[0:-2]+" in dis "+nome)
                for ret in dest.findall("additional"):
                    temporarylocation = etree.Element("parkingArea")
                    temporarylocation.set('id',(str)(n))
                    temporarylocation.set('edge',string[0:-2])
                    temporarylocation.set('district',(str)(nome))
                    ret.insert(1,temporarylocation)
                    indent(ret)
                dest.write("disParking.xml",etree.dump(dest))
    
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()