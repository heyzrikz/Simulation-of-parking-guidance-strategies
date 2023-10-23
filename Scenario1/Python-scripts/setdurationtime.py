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
        i = randint(600,9000)
        f = etree.parse("trip.add.xml")
        for data in f.findall("trip"):
            for d in data.findall("stop"):
                d.set("duration",(str)(i))
                i=randint(600,9000)

        f.write("trip.add.xml",etree.dump(f))

            
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()