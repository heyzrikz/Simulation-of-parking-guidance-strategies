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
    file = minidom.parse("parking.add.xml")
    trip = file.getElementsByTagName('parkingArea')
    for data in trip:
        val = (int)(data.attributes[(str)("roadsideCapacity")].value)
        if val==0:
            newval = randint(1,20)
        else:
            newval = (int)((val*2))
        data.attributes["roadsideCapacity"].value = (str)(newval)
    print(file.toxml())
    with open("parking.add.xml","w") as f:
     file.writexml(f)
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()