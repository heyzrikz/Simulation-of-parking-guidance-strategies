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
    file = minidom.parse("detectors.add.xml")
    trip = file.getElementsByTagName('inductionLoop')
    for data in trip:
        val = data.attributes[(str)("pos")].value
        v = (float)(val)
        if v >= 30:
            v = v - 30
            data.attributes["pos"].value = (str)(v)
        else:
            if v != 0:
                data.attributes["pos"].value = "1"
    print(file.toxml())
    with open("detectors.add.xml","w") as f:
     file.writexml(f)
       
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()