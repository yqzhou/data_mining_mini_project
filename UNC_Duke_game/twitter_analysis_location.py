import json
import time
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import csv
import vincent
import folium
import pandas as pd

#read city file
city_state = {}
states = []
with open('cities.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for item in reader:
        if item[2] not in city_state:
            city_state[item[2]] = item[0]
        if item[0] not in states:
            states.append(item[0])


locations = ["Duke", "UNC"]
#locations = ["total_UNC2.txt"]

for location in locations:
    summary = {}
    filename = "processed_" + location +".txt"
    for line in open(filename, "r"):
        #print summary["location"]
        data = json.loads(line.rstrip())
        temp_location = data['location']
        if temp_location == "":
            continue
        state_name = re.match(",\b([A-Z][A-Z])", temp_location)
        if state_name == None:
            if temp_location in city_state.keys():
                state_name =  city_state[temp_location]
        else:
            state_name = state_name.group(0)
        if state_name != None:
            if state_name in summary.keys():
                summary[state_name] += 1
            else:
                summary[state_name] = 1
    filename = location + ".csv"
    with open(filename, 'wb') as f:
        w = csv.writer(f)
        for key, val in summary.items():
            w.writerow([key, val])
    """
    state_geo = r'us-states.json'
    df = pd.DataFrame(summary.items(), columns = ['State', 'Counts'])
    print df
    map = folium.Map(location=[40, -99], zoom_start =4)
    map.geo_json(geo_path = state_geo, data=df, columns=['State', 'Counts'], key_on='feature.id', fill_color='BuPu', fill_opacity=0.7, line_opacity=0.5, legend_name="# of Tweets", reset=True)
    map.create_map(path='us_states.html')
    """
    #summaries.append(summary)
