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
    file = minidom.parse("disParking.copy.xml")
    trip = file.getElementsByTagName('parkingAreaReroute')
    w=[]
    for data in trip:
        nome = data.attributes[(str)("id")].value
        w.append(nome)
    for a in w:
        count=0
        for data in trip:
            nome = data.attributes[(str)("id")].value
            if (str)(a)==nome:
                count=count+1
                if count>1:
                    print(nome)
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()