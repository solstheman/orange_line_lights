#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from google.transit import gtfs_realtime_pb2
from urllib.request import urlopen
from protobuf_to_dict import protobuf_to_dict


# In[2]:


stops = pd.read_csv('stops.txt')


# In[3]:


orange_line_stops = stops[(stops['platform_name'] == 'Orange Line') | (stops['platform_name'] == 'Forest Hills') | (stops['platform_name'] == 'Oak Grove') | stops['stop_id'].str.contains('Forest Hills-0') | stops['stop_id'].str.contains('Oak Grove-0')]


# In[4]:


feed = gtfs_realtime_pb2.FeedMessage()
response = urlopen('https://cdn.mbta.com/realtime/VehiclePositions.pb')
feed.ParseFromString(response.read())
feed_dict = protobuf_to_dict(feed)
vehicle_df = pd.json_normalize(feed_dict['entity'])
filtered_vehicles = vehicle_df[vehicle_df['vehicle.trip.route_id'] == 'Orange']
for ind, vehicle in filtered_vehicles.iterrows():
    print('Current Stop: ' + orange_line_stops[orange_line_stops['stop_id'] == vehicle['vehicle.stop_id']]['stop_name'].values[0])

