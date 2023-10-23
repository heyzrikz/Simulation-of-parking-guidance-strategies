#!/usr/bin/env python
# File: traci.py
from itertools import count
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
    file = minidom.parse(r"Results\vehroutes.xml")
    trip = file.getElementsByTagName('vehicle')
    val = 0
    count_200 = 0
    count_200_500 = 0
    count_500 = 0
    header = ['veicolo','secondi']
    with open(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1_abs.csv", 'w',encoding='UTF8',newline='')as f:
        writer = csv.writer(f)
        writer.writerow(header)
    for data in trip:
        val = (data.attributes[(str)("arrival")].value)
        #print(val)
        first = (str)(data.getElementsByTagName('stop'))
        third = (str)(data.getElementsByTagName('routeDistribution'))
        if first != '[]' and third != '[]':
            second = data.getElementsByTagName('route')
            for d in second:
                if d.hasAttribute('replacedAtTime'):
                    v = (d.attributes[(str)("replacedAtTime")].value)
                    break
            res = (float)(val) - (float)(v) 
            #print("cerca posto per : "+(str)(res)) 
            if res < 200:
                count_200 = count_200 + 1
            if res > 500:
                count_500 = count_500 + 1
            if res > 200 and res < 500:
                count_200_500 = count_200_500 + 1
            with open(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1_abs.csv", 'a',encoding='UTF8',newline='')as f:
                writer = csv.writer(f)
                data = [(data.attributes[(str)("id")].value),(float)(res)]
                writer.writerow(data)
    print("meno di 200: "+(str)(count_200))
    print("più di 200 meno di 500: "+(str)(count_200_500))
    print("più di 500: "+(str)(count_500))
    header = ['secondi','numero veicoli']
    with open(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1.csv", 'w',encoding='UTF8',newline='')as f:
        writer = csv.writer(f)
        writer.writerow(header)
    with open(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1.csv", 'a',encoding='UTF8',newline='')as f:
        writer = csv.writer(f)
        data = ["<200",count_200]
        writer.writerow(data)
        data = [">200 && <500",count_200_500]
        writer.writerow(data)
        data = [">500",count_500]
        writer.writerow(data)
    df = pd.read_csv(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1.csv")
    fig = px.pie(df, values='numero veicoli', names='secondi', title='Scenario 1 100%',color='secondi',color_discrete_map={
                                 '<200':'lightblue',
                                 '>200 && <500':'blue',
                                 '>500':'darkblue'
                                 })
    fig.write_image(r"C:\Users\lenovo\Sumo-workspace\SanFrancisco-Scenario1\Scenario1\Outputs\100%\Scenario1.png")
    
    
   
        
        

#main entry point
if __name__ == "__main__":


    run()