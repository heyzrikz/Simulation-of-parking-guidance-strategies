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

def run():
    file = etree.parse("reroute_parking.xml")
    root = file.getroot()
    for child in root:
        for interval in child:
            for parkingAreaReroute in interval:
                parkingAreaReroute.set("probability","0.5")
                parkingAreaReroute.set("visible","false")
                #print((str)(parkingAreaReroute.get("probability")))
    file.write("reroute_parking.xml",etree.dump(file))
  
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()